#!/usr/bin/env python3
"""Serve this isolated lab and optional measured fixed-LIF bridge on localhost."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from live_brain import BrainError, LiveBrain

class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.mjs': 'text/javascript'}
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def list_directory(self, path):
        self.send_error(404)
        return None
    def json_response(self, status, value):
        raw = json.dumps(value, ensure_ascii=False, allow_nan=False).encode('utf8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
    def do_POST(self):
        try:
            if self.path != '/api/brain/step':
                raise BrainError('Unknown endpoint', 404)
            port = self.server.server_port
            hosts = {f'127.0.0.1:{port}', f'localhost:{port}'}
            host = self.headers.get('Host')
            if host not in hosts:
                raise BrainError('Local host required', 403)
            origin = self.headers.get('Origin')
            if origin is not None and origin != 'http://' + host:
                raise BrainError('Same-origin request required', 403)
            if self.headers.get('Sec-Fetch-Site') == 'cross-site':
                raise BrainError('Cross-site request denied', 403)
            lengths = self.headers.get_all('Content-Length', [])
            if self.headers.get('Transfer-Encoding') or len(lengths) != 1 or not lengths[0].isdigit():
                raise BrainError('A single Content-Length is required', 411)
            size = int(lengths[0])
            if not 0 < size <= 4096:
                raise BrainError('Request must be between 1 and 4096 bytes', 413)
            if self.headers.get_content_type() != 'application/json':
                raise BrainError('application/json required', 415)
            self.connection.settimeout(5)
            raw = self.rfile.read(size)
            if len(raw) != size:
                raise BrainError('Incomplete request body', 400)
            try:
                payload = json.loads(raw)
            except (ValueError, UnicodeError, RecursionError):
                raise BrainError('Invalid JSON', 400)
            self.json_response(200, self.server.brain.step(payload))
        except BrainError as exc:
            self.close_connection = True
            self.json_response(exc.status, {'source': 'live_fixed_lif_error', 'error': str(exc)})
        except TimeoutError:
            self.close_connection = True
            self.json_response(408, {'source': 'live_fixed_lif_error', 'error': 'Request body timed out'})

class LabServer(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address, handler, brain):
        self.brain = brain
        super().__init__(address, handler)
    def server_close(self):
        super().server_close()
        self.brain.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8767)
    parser.add_argument('--brain-upstream', type=Path)
    parser.add_argument('--brain-cache', type=Path)
    parser.add_argument('--brain-model', type=Path)
    parser.add_argument('--java', type=Path)
    parser.add_argument('--javac', type=Path)
    args = parser.parse_args()
    brain = LiveBrain(upstream=args.brain_upstream, cache=args.brain_cache, model=args.brain_model,
                      java=args.java, javac=args.javac)
    server = LabServer(('127.0.0.1', args.port), partial(Handler, directory=str(Path(__file__).resolve().parent)), brain)
    print(f'ドギドの飛行ラボ: http://127.0.0.1:{server.server_port}  終了: Control+C', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
