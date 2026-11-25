"""Structural and information-boundary tests for v0.3."""
import copy
import unittest

from employer_model_v03 import CASES, DEFAULTS, choose, environment, paired, production, simulate
from employer_measurement_v03 import PROFILES, assess, observe


class EmployerTests(unittest.TestCase):
    def test_accounting_and_capacity(self):
        for _,p in CASES:
            for path in paired(p):
                for i,s in enumerate(path):
                    self.assertAlmostEqual(s['hours'],s['used_hours']+s['idle_hours'])
                    self.assertAlmostEqual(s['realised_surplus'],s['revenue']+s['option_payoff']-
                                           s['payroll']-s['ai_cost']-s['adjustment_cost'])
                    self.assertEqual(s['hours'],500*s['headcount'])
                    if i:
                        self.assertEqual(s['headcount'],path[i-1]['headcount']+s['hiring']-
                                         s['layoffs']-s['natural_departures'])

    def test_choice_maximises_stated_score(self):
        for _,parameters in CASES:
            p={**DEFAULTS,**parameters}
            e=environment(p,3,True)
            choice=choose(10,9,e,p,True)
            for n in range(9 if p['attrition_only'] else 0,21):
                score=4*production(n,e,p)['operating_surplus']-max(0,n-9)*p['hire_cost']-max(0,9-n)*p['layoff_cost']
                self.assertGreaterEqual(choice[0]+1e-9,score)

    def test_no_ai_equivalence(self):
        a,c,_=paired(dict(ai=False))
        self.assertEqual(a,c)

    def test_mechanism_distinctions(self):
        self.assertEqual(simulate({})[-1]['headcount'],6)
        self.assertEqual(simulate(dict(option_value=30))[-1]['headcount'],10)
        self.assertEqual(simulate(dict(new_value=40))[-1]['headcount'],10)
        pursuit=simulate(dict(new_value=40,pursue=True))
        self.assertEqual(pursuit[6]['headcount'],10)
        self.assertEqual(pursuit[12]['headcount'],7)
        attrition=simulate(dict(attrition_only=True))
        self.assertTrue(all(s['layoffs']==0 for s in attrition))
        self.assertEqual(attrition[3]['headcount'],9)
        self.assertEqual(attrition[6]['headcount'],6)

    def test_identical_observations_opposite_causes(self):
        p1=dict(no_comparison=True)
        p2=dict(no_comparison=True,external_efficiency=.4)
        a,c,k=paired(p1)
        x,xc,xk=paired(p2)
        self.assertNotEqual(c,xc)
        for profile in PROFILES:
            r=observe(a,k,p1,profile)
            s=observe(x,xk,p2,profile)
            self.assertEqual(r,s)
            self.assertEqual(assess(r,12),assess(s,12))

    def test_future_evidence_and_truth_not_inputs(self):
        a,_,c=paired({})
        r=observe(a,c,{},'staggered')
        for q in range(13):
            self.assertEqual(assess(r,q),assess([x for x in r if x['available']<=q],q))
        modified=copy.deepcopy(r)
        for x in modified:
            if x['available']>4:
                x['value']={}
        self.assertEqual(assess(r,4),assess(modified,4))

    def test_delayed_and_missing_evidence(self):
        a,_,c=paired({})
        lagged=assess(observe(a,c,{},'staggered'),12)['outcomes']['hours']
        self.assertTrue(lagged['alert'])
        self.assertFalse(lagged['current_alert'])
        self.assertEqual(lagged['observed_period'],10)
        missing=assess(observe(a,c,{},'missing_scope'),12)['outcomes']['hours']
        self.assertEqual(missing['signal'],'unknown')
        self.assertIsNone(missing['gap'])

    def test_fixed_window_and_no_zero_division(self):
        a,_,c=paired(dict(attrition_only=True))
        records=observe(a,c,{},'immediate')
        self.assertEqual(assess(records,6,flow_rule='fixed_event')['outcomes']['hiring']['gap'],
                         assess(records,12,flow_rule='fixed_event')['outcomes']['hiring']['gap'])
        for r in records:
            if r['kind']=='workforce':
                r['value']['comparator']['hiring']=0
        self.assertEqual(assess(records,12)['outcomes']['hiring']['signal'],'unknown')

    def test_hidden_confounding_remains(self):
        p=dict(external_efficiency=.4)
        a,cf,c=paired(p)
        self.assertEqual(a[-1]['hours'],cf[-1]['hours'])
        self.assertTrue(assess(observe(a,c,p,'immediate'),12)['outcomes']['hours']['alert'])


if __name__=='__main__':
    unittest.main()
