"""Select equal-mass catalogue rows exactly; do not claim certification."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re

SOURCE_SHA256="a52eb43ec9dc2ef52e931f0e3cdc7708401093ad12c1088345be918b01164eda"
IDENTIFIER=re.compile(r"O_\{([0-9]+)\}\(([^)]+)\)")

def select(text, count=20):
    if count<1:raise ValueError("positive count required")
    rows=[];seen=set()
    for line_number,line in enumerate(text.splitlines(),1):
        if line.startswith("O_{index}(m_3)"):continue
        if not line.startswith("O_{"):continue
        columns=line.split();match=IDENTIFIER.fullmatch(columns[0])
        if not match or len(columns)!=7:raise ValueError("malformed catalogue row")
        if columns[0] in seen:raise ValueError("duplicate orbit identifier")
        seen.add(columns[0])
        values=[Fraction(x) for x in columns[1:6]]
        mass=Fraction(match.group(2))
        if mass<=0 or values[-1]<=0 or columns[6] not in ("S","U"):
            raise ValueError("invalid mass, period or stability marker")
        if mass!=1:continue
        rows.append({"orbit":columns[0],"source_line":line_number,"masses":["1","1","1"],
                     "z0":columns[1],"vx":columns[2],"vy":columns[3],"vz":columns[4],
                     "period":columns[5],"catalogue_stability":columns[6],
                     "result":"not_attempted","reason":"rigorous certifier and independent verifier pending",
                     "runtime_seconds":None})
    rows.sort(key=lambda row:(Fraction(row["period"]),int(IDENTIFIER.fullmatch(row["orbit"]).group(1))))
    if len(rows)<count:raise ValueError("fewer eligible rows than requested")
    return rows[:count]

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("catalogue")
    parser.add_argument("--sha256",default=SOURCE_SHA256);parser.add_argument("--count",type=int,default=20)
    args=parser.parse_args();raw=Path(args.catalogue).read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=args.sha256:parser.error("source hash differs; do not silently use another catalogue")
    try:rows=select(raw.decode(),args.count)
    except ValueError as error:parser.error(str(error))
    print(json.dumps({"source_sha256":digest,"selection":"equal masses; ascending exact printed period",
                      "rows":rows},indent=2))

if __name__=="__main__":main()
