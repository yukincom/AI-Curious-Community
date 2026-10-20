"""Serialized, persistent fixed-LIF bridge. No network calls or synthetic fallback."""
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import select
import shutil
import subprocess
import sys
import threading
import time

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB / 'brain-readout'))
from infer_readout import infer
from train_readout import DATA_SHA, FEATURES, SHA
READOUT_SHA = 'bb6448586e4132590adebef36c1f8f2f073548bcadde24be280b35b7d83ffff3'

class BrainError(Exception):
    def __init__(self, message, status=503):
        super().__init__(message)
        self.status = status


def validate_request(value):
    required = {'session', 'sequence', 'odor_strength', 'body_time', 'body_position'}
    if not isinstance(value, dict) or set(value) != required:
        raise BrainError('Expected exactly session, sequence, odor_strength, body_time, body_position', 400)
    session = value['session']
    if not isinstance(session, str) or not 1 <= len(session) <= 64 or any(ord(c)<32 for c in session):
        raise BrainError('session must be a nonempty string of at most 64 characters without control characters', 400)
    try:
        session.encode('utf8')
    except UnicodeError:
        raise BrainError('session must be valid UTF-8', 400)
    sequence = value['sequence']
    if isinstance(sequence, bool) or not isinstance(sequence, int) or not 0 < sequence <= 9007199254740991:
        raise BrainError('sequence must be a positive safe integer', 400)
    def number(v):
        try:
            return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)
        except OverflowError:
            return False
    if not number(value['odor_strength']) or not 0 <= value['odor_strength'] <= 1:
        raise BrainError('odor_strength must be finite and between 0 and 1', 400)
    if not number(value['body_time']) or value['body_time'] < 0:
        raise BrainError('body_time must be finite and nonnegative', 400)
    p = value['body_position']
    if not isinstance(p, dict) or set(p) != {'x', 'y', 'z'} or not all(number(v) for v in p.values()):
        raise BrainError('body_position must contain three finite x/y/z coordinates', 400)
    return value


class LiveBrain:
    def __init__(self, *, upstream=None, cache=None, model=None, java=None, javac=None, timeout=10):
        root = LAB.parents[1]
        self.upstream = Path(upstream) if upstream else root / '.fly-research/upstream/blendi-remade--fly-brain-minecraft'
        self.cache = Path(cache) if cache else root / '.fly-research/live-brain'
        self.model_path = Path(model) if model else LAB / 'brain-readout/results/model.json'
        self.java, self.javac = java, javac
        self.timeout = timeout
        self.lock = threading.Lock()
        self.process = None
        self.log = None
        self.buffer = b''
        self.session = None
        self.sequence = 0
        self.body_time = 0
        self.failed_session = None
        self.closed = False

    def _tool(self, explicit, name):
        if explicit:
            return str(explicit)
        known = Path('/Library/Java/JavaVirtualMachines/temurin-25.jdk/Contents/Home/bin') / name
        found = str(known) if known.is_file() else shutil.which(name)
        if not found:
            raise BrainError('JDK with java and javac is required; no automatic download')
        return found

    def _start(self):
        def run(args):
            return subprocess.check_output(args, stderr=subprocess.PIPE, timeout=30)
        root = self.upstream.resolve()
        if run(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip() != SHA:
            raise BrainError('Upstream revision mismatch')
        sources = []
        for name in ('Connectome', 'PopulationIndex', 'LifConfig', 'LifNetwork'):
            relative = Path('src/main/java/com/fruitfly/brain') / (name + '.java')
            source = root / relative
            raw = source.read_bytes()
            if raw != run(['git', '-C', str(root), 'show', f'HEAD:{relative}']):
                raise BrainError('Upstream source bytes modified: ' + name)
            sources.append((source.name, raw))
        data = root / 'src/main/resources/connectome/malecns-v1.0.flyb.gz'
        with data.open('rb') as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        if digest != DATA_SHA:
            raise BrainError('Connectome checksum mismatch')
        model_bytes = self.model_path.read_bytes()
        if hashlib.sha256(model_bytes).hexdigest() != READOUT_SHA:
            raise BrainError('Frozen readout model checksum mismatch')
        self.model = json.loads(model_bytes)
        expected_config = {'dt_ms': .5, 'global_gain': .65, 'kenyon_input_gain': .25, 'threads': 1}
        if (self.model.get('upstream_sha') != SHA or self.model.get('connectome_sha256') != DATA_SHA
                or self.model.get('network_config') != expected_config):
            raise BrainError('Readout model provenance/config mismatch')
        infer(dict.fromkeys(FEATURES, 0), self.model)
        wrapper = LAB / 'brain-readout/LiveBrainWorker.java'
        sources.append((wrapper.name, wrapper.read_bytes()))
        java, javac = self._tool(self.java, 'java'), self._tool(self.javac, 'javac')
        self.cache.mkdir(parents=True, exist_ok=True)
        source_dir = self.cache / 'sources'
        classes = self.cache / 'classes'
        source_dir.mkdir(exist_ok=True); classes.mkdir(exist_ok=True)
        # Compile only the verified bytes; do not modify upstream source files.
        paths = []
        for name, raw in sources:
            path = source_dir / name; path.write_bytes(raw); paths.append(str(path))
        subprocess.run([javac, '-d', str(classes), *paths], check=True, capture_output=True, timeout=30)
        self.log = (self.cache / 'worker.log').open('ab', buffering=0)
        self.process = subprocess.Popen([java, '-Xmx512m', '-cp', str(classes), 'LiveBrainWorker', str(data)],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.log, bufsize=0)
        self.buffer = b''
        fields = self._line().split('\t')
        if len(fields) != 3 or fields[0] != 'READY':
            raise BrainError('Invalid worker startup response')
        self.neurons, self.edges = int(fields[1]), int(fields[2])
        if self.neurons != 176422 or self.edges != 6287749:
            raise BrainError('Unexpected circuit dimensions')

    def _line(self):
        deadline = time.monotonic() + self.timeout
        while b'\n' not in self.buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([self.process.stdout], [], [], max(0, remaining))[0]:
                raise BrainError('Live neural worker timed out')
            chunk = os.read(self.process.stdout.fileno(), 4096)
            if not chunk:
                raise BrainError('Live neural worker exited unexpectedly')
            self.buffer += chunk
            if len(self.buffer) > 8192:
                raise BrainError('Oversized worker response')
        line, self.buffer = self.buffer.split(b'\n', 1)
        return line.decode('ascii')

    def _stop(self):
        process, self.process = self.process, None
        if process is not None:
            if process.poll() is None:
                process.terminate()
                try: process.wait(timeout=2)
                except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=2)
            for stream in (process.stdin, process.stdout):
                if stream: stream.close()
        if self.log: self.log.close(); self.log = None
        self.buffer = b''

    def step(self, payload):
        p = validate_request(payload)
        if not self.lock.acquire(blocking=False):
            raise BrainError('Live neural worker is busy; keep only one request in flight', 409)
        try:
            if self.closed: raise BrainError('Live neural worker is closed')
            if p['session'] == self.failed_session:
                raise BrainError('This neural session failed; start a new session explicitly')
            if p['session'] == self.session and (p['sequence'] <= self.sequence or p['body_time'] < self.body_time):
                raise BrainError('Sequence must increase and body_time must not go backwards', 409)
            try:
                if self.process is None: self._start()
                rate = min(180.0, p['odor_strength'] * 600.0)
                session_token = base64.b64encode(p['session'].encode('utf8')).decode('ascii')
                self.process.stdin.write(f"{session_token}\t{p['sequence']}\t{rate}\n".encode('ascii'))
                self.process.stdin.flush()
                values = self._line().split('\t')
                if len(values) != 12 or int(values[0]) != p['sequence']:
                    raise BrainError('Invalid neural response sequence or field count')
                brain_ms, wall_ms, bad = float(values[1]), float(values[2]), int(values[3])
                rates = dict(zip(FEATURES, map(float, values[4:])))
                expected_ms = self.brain_ms + 50 if p['session'] == self.session else 50
                if brain_ms != expected_ms or not math.isfinite(wall_ms) or wall_ms < 0 or bad != 0:
                    raise BrainError('Invalid neural time or nonfinite membrane state')
                result = {'source': 'live_fixed_lif', **p, 'input_hz': rate, 'brain_ms': brain_ms,
                          'window_ms': 50, 'wall_ms': wall_ms, 'rates_hz': rates, 'readout': infer(rates, self.model),
                          'neuron_count': self.neurons, 'edge_count': self.edges, 'nonfinite_membranes': bad,
                          'upstream_sha': SHA, 'connectome_sha256': DATA_SHA}
                self.session, self.sequence, self.body_time, self.brain_ms = p['session'], p['sequence'], p['body_time'], brain_ms
                self.failed_session = None
                return result
            except Exception as exc:
                self.failed_session = p['session']
                self._stop()
                if isinstance(exc, BrainError): raise
                raise BrainError('Live neural worker unavailable: ' + type(exc).__name__) from exc
        finally:
            self.lock.release()

    def close(self):
        with self.lock:
            self.closed = True
            self._stop()
