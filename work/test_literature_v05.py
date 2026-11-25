"""Structural tests for the v0.5 literature-grounded extension."""
import math
import unittest

import employer_model_v04 as v04
import employer_model_v05 as v05
import panel_v05 as P


class LiteratureTests(unittest.TestCase):
    def test_reproduces_v04_at_old_settings(self):
        for name, p in v05.CASES:
            for size in (10, 100):
                for sd in (0, .05):
                    shock = v04.shock_series(sd, 3, f'{name}-t-{size}')
                    for intervention in (True, False):
                        self.assertEqual(v05.simulate({**p, 'size': size}, intervention, shock),
                                         v04.simulate({**p, 'size': size}, intervention, shock))

    def test_shared_new_work_grows_no_ai_path(self):
        p = dict(new_value=40, shared_new_work=True)
        actual, no_ai = v05.potential_paths(p)
        self.assertEqual((actual[-1]['headcount'], no_ai[-1]['headcount']), (10, 14))
        private = v05.potential_paths(dict(new_value=40))
        self.assertEqual((private[0][-1]['headcount'], private[1][-1]['headcount']), (10, 10))

    def test_small_saving_depends_on_size(self):
        small = v05.potential_paths(dict(ai_efficiency=.05))
        large = v05.potential_paths(dict(ai_efficiency=.05, size=100))
        self.assertEqual(small[0][-1]['headcount'], small[1][-1]['headcount'])
        self.assertLess(large[0][-1]['headcount'], large[1][-1]['headcount'])

    def test_cohort_stationary_without_ai_and_total_preserved(self):
        no_ai = v05.cohort_simulate(intervention=False)
        ai = v05.cohort_simulate()
        self.assertTrue(all((s['junior'], s['experienced']) == (10, 10) for s in no_ai))
        self.assertEqual([s['headcount'] for s in ai], [s['headcount'] for s in no_ai])
        self.assertEqual((ai[-1]['junior'], ai[-1]['experienced']), (5, 15))

    def test_accounting_with_pre_review(self):
        for condition in P.CONDITIONS:
            for path in P.treated_paths({}, condition, 1, 'acct'):
                for i, s in enumerate(path[1:], 1):
                    self.assertEqual(s['headcount'], path[i-1]['headcount']+s['hiring']-
                                     s['layoffs']-s['natural_departures'])

    def test_simplex_projection_and_weights(self):
        w = P.project_simplex([.7, .6, -.2])
        self.assertAlmostEqual(sum(w), 1)
        self.assertTrue(all(x >= 0 for x in w))
        donors = P.donor_panel('flat', 2)
        weights = P.synthetic_weights(donors[4], donors)
        self.assertAlmostEqual(sum(weights), 1, places=9)
        self.assertGreater(weights[4], .9)  # a donor reproduces itself

    def test_estimators_zero_when_treated_equals_control(self):
        donors = P.donor_panel('flat', 3)
        same = [list(donors[10]) for _ in range(5)]
        est, _ = P.estimates(donors[10], same)
        for v in est.values():
            self.assertAlmostEqual(v, 0, places=12)

    def test_spillover_borrowed_path(self):
        s = P.spillover_path()
        self.assertEqual(s[:P.ADOPT-1], [1.0]*(P.ADOPT-1))
        self.assertTrue(math.isclose(s[-1], 1.125805))

    def test_estimators_never_see_truth(self):
        # Only the published hours arrays are arguments; no global names that
        # carry loadings, conditions, cases or counterfactual paths are read.
        code = P.estimates.__code__
        self.assertEqual(code.co_varnames[:code.co_argcount], ('treated', 'donors'))
        used = set(code.co_names)
        for forbidden in ('DONOR_LOADINGS', 'TREATED_LOADING', 'CONDITIONS', 'treated_paths',
                          'demand', 'cycle', 'spillover_path', 'simulate'):
            self.assertNotIn(forbidden, used)


if __name__ == '__main__':
    unittest.main()
