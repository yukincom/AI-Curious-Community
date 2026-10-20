import copy
from functools import partial
import http.client
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from live_brain import BrainError, LiveBrain, validate_request
from serve import Handler, LabServer

PAYLOAD = {'session':'test','sequence':1,'odor_strength':.2,'body_time':0,'body_position':{'x':0,'y':3.2,'z':0}}

class ValidationTests(unittest.TestCase):
    def test_valid_and_invalid_inputs(self):
        self.assertEqual(validate_request(copy.deepcopy(PAYLOAD)), PAYLOAD)
        cases = [('sequence',True),('sequence',0),('sequence',1.1),('odor_strength',float('nan')),
                 ('odor_strength',1.1),('body_time',-1),('body_time',10**400),('session','x'*65),
                 ('session',''),('body_position',{'x':0,'y':0,'z':float('inf')})]
        for key,value in cases:
            with self.subTest(key=key,value=value):
                p=copy.deepcopy(PAYLOAD);p[key]=value
                with self.assertRaises(BrainError):validate_request(p)

    def test_no_same_session_silent_restart_after_failure(self):
        brain=LiveBrain()
        with patch.object(brain,'_start',side_effect=OSError('unavailable')) as start:
            for _ in range(2):
                with self.assertRaises(BrainError):brain.step(PAYLOAD)
            self.assertEqual(start.call_count,1)
            with self.assertRaises(BrainError):brain.step({**PAYLOAD,'session':'next'})
            self.assertEqual(start.call_count,2)
        brain.close()

    def test_busy_duplicate_and_closed_requests(self):
        brain=LiveBrain();brain.lock.acquire()
        try:
            with self.assertRaises(BrainError) as err:brain.step(PAYLOAD)
            self.assertEqual(err.exception.status,409)
        finally:brain.lock.release()
        brain.session='test';brain.sequence=1;brain.body_time=0
        with self.assertRaises(BrainError) as err:brain.step(PAYLOAD)
        self.assertEqual(err.exception.status,409)
        brain.close()
        with self.assertRaises(BrainError):brain.step({**PAYLOAD,'session':'new'})

    def test_timeout_stops_real_child(self):
        brain=LiveBrain(timeout=.05)
        brain.process=subprocess.Popen([sys.executable,'-c','import time; time.sleep(10)'],
                                       stdin=subprocess.PIPE,stdout=subprocess.PIPE,bufsize=0)
        process=brain.process
        try:
            with self.assertRaises(BrainError):brain.step(PAYLOAD)
            self.assertIsNotNone(process.poll())
            self.assertIsNone(brain.process)
        finally:brain.close()

class FakeBrain:
    def __init__(self):self.calls=[];self.closed=False
    def step(self,value):validate_request(value);self.calls.append(value);return {'source':'test_only'}
    def close(self):self.closed=True

class HttpTests(unittest.TestCase):
    def setUp(self):
        self.brain=FakeBrain();self.tmp=tempfile.TemporaryDirectory()
        self.server=LabServer(('127.0.0.1',0),partial(Handler,directory=self.tmp.name),self.brain)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join();self.tmp.cleanup()
        self.assertTrue(self.brain.closed)
    def request(self,headers=None,body=None):
        connection=http.client.HTTPConnection('127.0.0.1',self.server.server_port,timeout=3)
        try:
            connection.request('POST','/api/brain/step',body=json.dumps(PAYLOAD) if body is None else body,
                               headers={'Content-Type':'application/json',**(headers or {})})
            response=connection.getresponse();return response.status,json.loads(response.read()),response.headers
        finally:connection.close()
    def test_same_origin_and_missing_origin_local_client(self):
        status,_,headers=self.request({'Origin':f'http://127.0.0.1:{self.server.server_port}'})
        self.assertEqual(status,200);self.assertIsNone(headers.get('Access-Control-Allow-Origin'))
        self.assertEqual(self.request()[0],200);self.assertEqual(len(self.brain.calls),2)
    def test_foreign_origin_and_host_blocked_without_worker(self):
        self.assertEqual(self.request({'Origin':'https://unrelated.example'})[0],403)
        self.assertEqual(self.request({'Host':'unrelated.example'})[0],403)
        self.assertEqual(self.request({'Sec-Fetch-Site':'cross-site'})[0],403)
        self.assertFalse(self.brain.calls)
    def test_bad_json_oversized_type_and_schema(self):
        self.assertEqual(self.request(body='{broken')[0],400)
        self.assertEqual(self.request(body=' '*4097)[0],413)
        self.assertEqual(self.request({'Content-Type':'text/plain'})[0],415)
        self.assertEqual(self.request(body='{"sequence":1}')[0],400)
        self.assertFalse(self.brain.calls)

if __name__=='__main__':unittest.main()
