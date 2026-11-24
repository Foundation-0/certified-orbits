"""Independent input audit only. This program cannot accept an orbit proof."""
import argparse
from fractions import Fraction
import json
from pathlib import Path

def number(value):
    if not isinstance(value,str):raise ValueError("proof inputs must be rational strings")
    return Fraction(value)

def interval(value):
    if not isinstance(value,list) or len(value)!=2:raise ValueError("expected two endpoints")
    lo,hi=map(number,value)
    if lo>=hi:raise ValueError("interval must have nonempty interior")
    return lo,hi

def audit(data):
    if not isinstance(data,dict):raise ValueError("expected object")
    masses=data["masses"]
    if len(masses)!=3 or any(number(x)<=0 for x in masses):raise ValueError("three positive masses required")
    names=data["unknowns"]
    if (not isinstance(names,list) or not names or any(not isinstance(x,str) or not x for x in names)
        or len(set(names))!=len(names)):raise ValueError("unique unknown names required")
    box=data["box"]
    if not isinstance(box,dict) or set(box)!=set(names):raise ValueError("box must match unknowns")
    for name in names:interval(box[name])
    lo,_=interval(data["period"])
    if lo<=0:raise ValueError("period must be positive")
    for key in ("initial_conditions","normalisation","symmetry"):
        if not isinstance(data[key],dict) or not data[key]:raise ValueError("missing structured "+key)
    return {"input_audit":"passed", "proof":"not_verified",
            "reason":"Independent rigorous flow and derivative integration are not implemented."}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("certificate")
    args=parser.parse_args()
    try:
        data=json.loads(Path(args.certificate).read_text());result=audit(data)
    except (ValueError,KeyError,TypeError,OSError) as error:
        print(json.dumps({"input_audit":"rejected","proof":"not_verified","reason":str(error)}))
        return 1
    print(json.dumps(result));return 2

if __name__=="__main__":raise SystemExit(main())
