"""Additional structural checks; does not write benchmark output."""
import copy
import json
import unittest

import longitudinal_indicator_v02 as model


class BenchmarkChecks(unittest.TestCase):
    def packet(self, index, delay=0, mask='complete'):
        spec = model.CASES[index]
        actual, _, comparator = model.economics(spec)
        return model.observations(spec, actual, comparator, delay, mask)

    def test_stock_flow_accounting_and_nonnegative_quantities(self):
        for spec in model.CASES:
            for path in model.economics(spec):
                for previous, current in zip(path, path[1:]):
                    self.assertAlmostEqual(current['headcount'], previous['headcount']+
                                           current['hiring']-current['separations'])
                    for key in ('headcount', 'hours', 'hiring', 'separations', 'pay'):
                        self.assertGreaterEqual(current[key], 0)

    def test_identical_inputs_opposite_truths(self):
        self.assertEqual(self.packet(20), self.packet(21))
        a, cf, _ = model.economics(model.CASES[20])
        x, xcf, _ = model.economics(model.CASES[21])
        self.assertNotEqual(model.truth_at(a, cf, 10), model.truth_at(x, xcf, 10))

    def test_future_mutation_cannot_change_past(self):
        records = self.packet(2, delay=2)
        altered = copy.deepcopy(records)
        for r in altered:
            if r['available'] > 4:
                r['payload']['actual']['hours'] = 1
                r['payload']['task_minutes'] = 0
        self.assertEqual(model.assess(records, 4, .1), model.assess(altered, 4, .1))

    def test_missing_pay_is_not_zero_loss(self):
        result = model.assess(self.packet(9, mask='pay_panel'), 10, .1)
        self.assertEqual(result['outcomes']['pay']['signal'], 'unknown')
        self.assertIsNone(result['outcomes']['pay']['gap'])

    def test_strict_boundary(self):
        records = self.packet(2)
        records[-1]['payload']['actual']['hours'] = 90
        self.assertEqual(model.assess(records, 10, .1)['outcomes']['hours']['signal'], 'below cutoff')

    def test_saved_assessments_reproduce(self):
        root = model.ROOT/'outputs/longitudinal-v02/run-001'
        packets = json.loads((root/'observations.json').read_text())
        lookup = {(p['id'], p['delay'], p['mask']): p['records'] for p in packets}
        for run in json.loads((root/'assessments.json').read_text()):
            records = lookup[run['id'], run['delay'], run['mask']]
            self.assertEqual(run['assessments'], [model.assess(records, q, run['threshold']) for q in range(11)])


if __name__ == '__main__':
    unittest.main()
