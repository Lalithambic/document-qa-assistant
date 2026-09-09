import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from app import ask, load_chunks

DATA = Path(__file__).parent/'data'
class RetrievalTests(unittest.TestCase):
    def test_relevant_source_ranks_first(self):
        result = ask('How many days of annual leave?', DATA)
        self.assertEqual(result['sources'][0]['source'], 'leave-policy.txt#chunk-1')
        self.assertIsNone(result['answer'])
    def test_absent_topic_does_not_invent_answer(self):
        self.assertEqual(ask('Volcanic magma', DATA)['mode'], 'no_match')
    def test_empty_input_and_folder(self):
        with self.assertRaises(ValueError):
            ask(' ', DATA)
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                load_chunks(directory)
    def test_generation_request_contract(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({'response': '18 days [leave-policy.txt#chunk-1]'}).encode()
        opener = MagicMock()
        opener.open.return_value = response
        with patch('app.urllib.request.build_opener', return_value=opener):
            result = ask('annual leave', DATA, 'test-model')
        request = opener.open.call_args.args[0]
        payload = json.loads(request.data)
        self.assertFalse(payload['stream'])
        self.assertIn('18 days', payload['prompt'])
        self.assertEqual(result['mode'], 'generated')
    def test_generation_failure_is_explicit(self):
        opener = MagicMock()
        opener.open.side_effect = OSError('offline')
        with patch('app.urllib.request.build_opener', return_value=opener):
            with self.assertRaises(RuntimeError):
                ask('annual leave', DATA, 'test-model')

if __name__ == '__main__':
    unittest.main()
