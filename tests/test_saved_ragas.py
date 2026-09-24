import unittest
from scripts.evaluate_saved_ragas import load_rows, response_text


class FrozenEvaluationTests(unittest.TestCase):
    def test_same_questions_and_configuration(self):
        rows = load_rows()
        self.assertEqual(len(rows['simple']), 30)
        self.assertEqual(len(rows['civic']), 30)

    def test_strip_only_source_footer(self):
        self.assertEqual(response_text('Answer\n\nSources: id'), 'Answer')
        self.assertEqual(response_text('Answer with Sources: in prose'), 'Answer with Sources: in prose')


if __name__ == '__main__':
    unittest.main()
