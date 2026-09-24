import math
import unittest
from evaluate_saved_retrieval import metrics


class MetricTests(unittest.TestCase):
    def test_three_of_four_in_five(self):
        r = metrics(['a', 'x', 'b', 'y', 'c'], {'a', 'b', 'c', 'd'})
        self.assertEqual(r['Precision@5'], .6)
        self.assertEqual(r['PooledRecall@5'], .75)
        self.assertEqual(r['Hit@5'], 1)
        self.assertEqual(r['MRR@5'], 1)
        self.assertAlmostEqual(r['PooledNDCG@5'], (1 + 1/math.log2(4) + 1/math.log2(6)) / sum(1/math.log2(i+2) for i in range(4)))

    def test_short_list_keeps_fixed_denominator(self):
        r = metrics(['a'], {'a'})
        self.assertEqual(r['Precision@5'], .2)
        self.assertEqual(r['PooledRecall@5'], 1)
        self.assertEqual(r['PooledNDCG@5'], 1)

    def test_no_relevance_not_fabricated_zero(self):
        self.assertIsNone(metrics(['a'], set()))

    def test_empty_output(self):
        self.assertTrue(all(v == 0 for v in metrics([], {'a'}).values()))

    def test_cutoff(self):
        self.assertTrue(all(v == 0 for v in metrics(['b', 'c', 'd', 'e', 'f', 'a'], {'a'}).values()))

    def test_first_relevant_at_three(self):
        self.assertAlmostEqual(metrics(['x', 'y', 'a'], {'a'})['MRR@5'], 1/3)

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(AssertionError):
            metrics(['a', 'a'], {'a'})


if __name__ == '__main__':
    unittest.main()
