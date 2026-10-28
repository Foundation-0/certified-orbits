import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from verifier_preflight import audit

def fixture():
    return {"masses":["1","1","1"],"unknowns":["x"],"box":{"x":["0","1"]},
            "period":["6","7"],"initial_conditions":{"source":"synthetic"},
            "normalisation":{"scale":"synthetic"},"symmetry":{"source":"synthetic"},
            "result":"certified","krawczyk":{"claimed":"inside"}}

class PreflightTests(unittest.TestCase):
    def test_self_reported_proof_never_accepted(self):
        self.assertEqual(audit(fixture())["proof"],"not_verified")
    def test_invalid_mass_period_box(self):
        for key,value in [("masses",["1","-1","1"]),("period",["-1","0"]),("box",{"x":["1","0"]})]:
            data=fixture();data[key]=value
            with self.assertRaises(ValueError):audit(data)
    def test_plausible_corruptions_still_not_verified(self):
        for key,value in [("masses",["1","2","1"]),("period",["60","70"]),("box",{"x":["10","11"]})]:
            data=fixture();data[key]=value
            self.assertEqual(audit(data)["proof"],"not_verified")
    def test_float_inputs_rejected(self):
        data=fixture();data["period"]=[6.0,7.0]
        with self.assertRaises(ValueError):audit(data)

if __name__=="__main__":unittest.main()
