import unittest
from evaluate import evaluate, token_f1

def row():
    return {'id': '1', 'question': 'Deadline?', 'answer': '60 days', 'expected_answer': '30 days', 'retrieved_sources': ['wrong'], 'expected_sources': ['right']}

class EvaluationTests(unittest.TestCase):
    def test_wrong_number_still_has_lexical_overlap(self):
        result = evaluate([row()])
        self.assertEqual(result['mean_exact_match'], 0)
        self.assertEqual(result['mean_answer_token_f1'], 0.5)
        self.assertEqual(result['mean_source_recall'], 0)
    def test_repeated_tokens_do_not_overcount(self):
        self.assertAlmostEqual(token_f1('days days days', 'days'), 0.5)
    def test_no_expected_sources_is_not_perfect_recall(self):
        item = row()
        item['expected_sources'] = []
        self.assertIsNone(evaluate([item])['mean_source_recall'])
    def test_bad_input(self):
        for value in ([], {}, [row(), row()], [{'id': 'bad'}]):
            with self.assertRaises(ValueError):
                evaluate(value)

if __name__ == '__main__':
    unittest.main()
