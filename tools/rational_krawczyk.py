"""Exact rational interval algebra; callers must supply validated flow enclosures."""
from dataclasses import dataclass
from fractions import Fraction

def rational(value):
    if isinstance(value, float) or isinstance(value, bool):
        raise TypeError("use exact rational strings, integers or Fractions")
    return Fraction(value)

@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction
    def __post_init__(self):
        object.__setattr__(self, "lo", rational(self.lo))
        object.__setattr__(self, "hi", rational(self.hi))
        if self.lo > self.hi: raise ValueError("reversed interval")
    def __add__(self, other): return Interval(self.lo+other.lo, self.hi+other.hi)
    def __neg__(self): return Interval(-self.hi, -self.lo)
    def __sub__(self, other): return self + -other
    def __mul__(self, other):
        corners=[self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi]
        return Interval(min(corners),max(corners))

def point(value): return Interval(value,value)

def nonsingular(matrix):
    a=[[rational(x) for x in row] for row in matrix]
    n=len(a)
    if not n or any(len(row)!=n for row in a): return False
    for col in range(n):
        pivot=next((row for row in range(col,n) if a[row][col]),None)
        if pivot is None:return False
        a[col],a[pivot]=a[pivot],a[col]
        for row in range(col+1,n):
            factor=a[row][col]/a[col][col]
            for k in range(col,n):a[row][k]-=factor*a[col][k]
    return True

def enclose(box, residual, jacobian, inverse):
    n=len(box)
    if (not n or len(residual)!=n or len(jacobian)!=n or
        any(len(row)!=n for row in jacobian) or len(inverse)!=n or
        any(len(row)!=n for row in inverse)):
        raise ValueError("inconsistent dimensions")
    if not nonsingular(inverse):raise ValueError("preconditioner must be nonsingular")
    if any(x.lo>=x.hi for x in box):raise ValueError("box needs nonempty interior")
    centre=[(x.lo+x.hi)/2 for x in box]
    result=[]
    for i in range(n):
        value=point(centre[i])
        for j in range(n):value=value-point(inverse[i][j])*residual[j]
        for j in range(n):
            coefficient=point(int(i==j))
            for k in range(n):coefficient=coefficient-point(inverse[i][k])*jacobian[k][j]
            value=value+coefficient*(box[j]-point(centre[j]))
        result.append(value)
    return result

def strict_inclusion(box, image):
    return bool(box) and len(box)==len(image) and all(
        outer.lo<inner.lo<=inner.hi<outer.hi for outer,inner in zip(box,image))
