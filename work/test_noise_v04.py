"""Structural tests for v0.4 noise and firm-size extension."""
import copy
import unittest

import employer_model_v03 as v03
import employer_model_v04 as v04
from employer_measurement_v03 import observe
from employer_measurement_v04 import assess, observe_noisy


class NoiseTests(unittest.TestCase):
    def test_size10_noise_free_reproduces_v03_exactly(self):
        for name, p in v04.CASES:
            self.assertEqual(v04.paired(p, size=10, case=name), v03.paired(p), name)

    def test_size100_noise_free_scales_linearly_except_integer_case(self):
        # Finding recorded during development (prediction P2 partly failed):
        # under the AI demand slump, core work needs 4.2 workers at size 10.
        # Whole-worker staffing gives 8 (2,100 core + 1,900 idle hours), while
        # size 100 matches 42 core + 40 retained = 82, not 80. Every other
        # case and path scales exactly. Kept as a test so the exception stays
        # visible rather than silently changing.
        broken = set()
        for name, p in v04.CASES:
            small = v04.paired(p, size=10, case=name)
            large = v04.paired(p, size=100, case=name)
            for label, s_path, l_path in zip(('actual', 'no_ai', 'comparator'), small, large):
                for s, l in zip(s_path, l_path):
                    for key in ('headcount', 'hiring', 'layoffs', 'natural_departures'):
                        if l[key] != 10*s[key]:
                            broken.add((name, label))
        self.assertEqual(broken, {('external_demand_slump', 'actual')})
        a10 = v04.paired(dict(v04.CASES)['external_demand_slump'], size=10)[0]
        a100 = v04.paired(dict(v04.CASES)['external_demand_slump'], size=100)[0]
        self.assertEqual((a10[12]['headcount'], a100[12]['headcount']), (8, 82))

    def test_accounting_holds_under_shocks(self):
        for name, p in v04.CASES:
            for size in (10, 100):
                for path in v04.paired(p, size=size, sigma_demand=.06, seed=3, case=name):
                    for i, s in enumerate(path):
                        self.assertAlmostEqual(s['hours'], s['used_hours']+s['idle_hours'])
                        self.assertEqual(s['hours'], 500*s['headcount'])
                        if i:
                            self.assertEqual(s['headcount'], path[i-1]['headcount']+s['hiring']-
                                             s['layoffs']-s['natural_departures'])

    def test_potential_paths_share_shocks_comparator_does_not(self):
        p = dict(ai=False)
        actual, no_ai, comparator = v04.paired(p, size=100, sigma_demand=.06, seed=1, case='no_adoption')
        self.assertEqual(actual, no_ai)  # no AI: identical potential outcomes
        self.assertNotEqual([s['output'] for s in actual], [s['output'] for s in comparator])
        self.assertNotEqual(v04.shock_series(.06, 1, 'no_adoption-treated-100'),
                            v04.shock_series(.06, 1, 'no_adoption-comparator-100'))

    def test_shocks_deterministic_and_truncated(self):
        a = v04.shock_series(.06, 7, 'x')
        self.assertEqual(a, v04.shock_series(.06, 7, 'x'))
        self.assertNotEqual(a, v04.shock_series(.06, 8, 'x'))
        self.assertEqual(a[0], 1.0)
        self.assertTrue(all(abs(x-1) <= .18+1e-12 for x in a))

    def test_reporting_error_only_touches_hours(self):
        a, _, c = v04.paired({}, size=100, case='immediate_review')
        clean = observe(a, c, {}, 'immediate')
        self.assertEqual(observe_noisy(a, c, {}, 0), clean)
        noisy = observe_noisy(a, c, {}, .03, seed=2)
        self.assertEqual(observe_noisy(a, c, {}, .03, seed=2), noisy)
        for x, y in zip(clean, noisy):
            if x['kind'] != 'workforce':
                self.assertEqual(x, y)
                continue
            for side in ('actual', 'comparator'):
                for key in ('headcount', 'hiring', 'layoffs'):
                    self.assertEqual(x['value'][side][key], y['value'][side][key])
        self.assertNotEqual(clean, noisy)

    def test_indicator_unchanged_and_blind_to_future(self):
        a, _, c = v04.paired({}, size=100, sigma_demand=.03, seed=5, case='immediate_review')
        r = observe_noisy(a, c, {}, .03, seed=5)
        for q in range(13):
            self.assertEqual(assess(r, q), assess([x for x in r if x['available'] <= q], q))
        modified = copy.deepcopy(r)
        for x in modified:
            if x['available'] > 6:
                x['value'] = {}
        self.assertEqual(assess(r, 6), assess(modified, 6))


if __name__ == '__main__':
    unittest.main()
