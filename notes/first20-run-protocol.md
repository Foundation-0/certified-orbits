# First twenty equal-mass orbit attempts

Status: source selection completed; certification has not started. Refs #3.

The selection script reads the pinned Li–Liao three-dimensional catalogue,
requires the expected SHA-256, parses printed decimals exactly, filters the third
mass to one, and sorts by the printed period. It retains the full source ID,
source line, starting parameters and stability label. The label is the
catalogue's numerical classification, not this project's proof.

```sh
python3 -m unittest discover -s tests -v
python3 tools/select_shortest.py /path/to/initial-condition-of-3D-periodic-orbits.txt
```

Source: [Li–Liao catalogue at the inspected commit](https://github.com/sjtu-liao/three-body/blob/b96b0193579a9952299d710ed616f529bb7cf898/initial-condition-of-3D-periodic-orbits.txt).
The file's header fixes the initial positions and velocities and says the first
two masses are one. Preserve that convention when converting rows into a shooting
system; the unshifted coordinates need not have centre of mass zero.

The selected rows are in `results/li-liao-3d-first20.json`; the adjacent table
records all twenty as not attempted. Missing software is not an integration
failure. No certificate, success rate or run time is invented.

After #2 and #4 provide validated programs, record the exact command, tool commits,
arithmetic precision, time limit and wall time for each attempt. Preserve stdout,
stderr and input hash locally. A successful attempt requires both programs to
accept the same certificate. Separate enclosure growth, insufficient printed
precision, failed inclusion, collision overlap and software errors. A timeout is
inconclusive. Do not overwrite failures with later successes; append attempts.

Multiple shooting requires a reviewed system and certified segment enclosures;
adding unconstrained numerical waypoints is insufficient. Use local bounded runs
first. Rented compute requires the person's approval. The fifty-orbit/two-week
stopping criterion in NOTE.md cannot be evaluated from a twenty-row selection.
