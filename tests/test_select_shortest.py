from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from select_shortest import select

def row(n,mass,period):return f"O_{{{n}}}({mass}) 0.1 0.2 0.3 0.4 {period} U"

class SelectionTests(unittest.TestCase):
    def test_exact_period_order_and_mass_filter(self):
        text="\n".join([row(1,"0.1","0.01"),row(2,"1","1.00000000000000002"),row(3,"1.0","1.00000000000000001")])
        self.assertEqual([x["orbit"] for x in select(text,2)],["O_{3}(1.0)","O_{2}(1)"])
    def test_duplicates_bad_rows_and_short_input_rejected(self):
        line=row(1,"1","6")
        for text,n in [(line+"\n"+line,1),(line,2),(row(1,"1","-2"),1),("O_{1}(1) 1 2",1)]:
            with self.assertRaises(ValueError):select(text,n)
    def test_selection_never_claims_a_proof(self):
        result=select(row(1,"1","6"),1)[0]
        self.assertEqual(result["result"],"not_attempted")
        self.assertIsNone(result["runtime_seconds"])

if __name__=="__main__":unittest.main()
