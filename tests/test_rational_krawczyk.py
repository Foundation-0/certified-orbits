from fractions import Fraction as F
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from rational_krawczyk import Interval as I,enclose,strict_inclusion,nonsingular

class KernelTests(unittest.TestCase):
    def test_square_root_two(self):
        box=[I("1.4","1.5")];centre=F(29,20)
        result=enclose(box,[I(centre**2-2,centre**2-2)],[[I("2.8","3")]],[[F(10,29)]])
        self.assertTrue(strict_inclusion(box,result))
        self.assertLess(result[0].lo**2,2);self.assertGreater(result[0].hi**2,2)
    def test_boundary_not_strict(self):
        self.assertFalse(strict_inclusion([I(0,1)],[I(0,"1/2")]))
        self.assertFalse(strict_inclusion([I(0,1)],[I(-1,2)]))
    def test_negative_product_and_singular_matrix(self):
        self.assertEqual(I(-2,3)*I(-4,5),I(-12,15))
        self.assertFalse(nonsingular([[1,2],[2,4]]))
        with self.assertRaises(ValueError):enclose([I(0,1)],[I(0,0)],[[I(1,1)]],[[0]])
    def test_float_and_bad_dimensions_rejected(self):
        with self.assertRaises(TypeError):I(0.1,1)
        with self.assertRaises(ValueError):enclose([I(0,1)],[],[],[])

if __name__=="__main__":unittest.main()
