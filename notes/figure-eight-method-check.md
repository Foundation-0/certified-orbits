# Figure-eight method check: first component

Status: draft exact interval algebra. No orbit has been certified. Refs #2.

`tools/rational_krawczyk.py` evaluates the operator in NOTE.md using rational
interval endpoints. It rejects floating-point inputs, singular preconditioners,
inconsistent dimensions and boxes with empty interior. Inclusion is strict in
every component. Tests include a scalar square-root problem, boundary contact,
negative interval products and a singular matrix.

```sh
python3 -m unittest discover -s tests -v
```

This component trusts the supplied residual and derivative enclosures. It does not
integrate a trajectory, prove that the enclosures are correct, remove symmetries,
or write a certificate. A successful algebra test is not an orbit proof.

The [2003 Kapela–Zgliczynski paper](https://ww2.ii.uj.edu.pl/~kapela/papers/nbody.pdf)
uses a C1 Lohner integrator and describes interval Newton and Krawczyk methods.
Its figure-eight existence calculation uses interval Newton; reproducing it with
Krawczyk would be a new implementation check, not a byte-for-byte replay of that
calculation. The [2007 Kapela–Simo paper](https://ww2.ii.uj.edu.pl/~kapela/papers/nosym.pdf)
addresses further choreographies and stability. Existence, local uniqueness and
stability require separate evidence.

Before connecting an integrator, a reviewer must derive the figure-eight's
specific square shooting system and gauge from the published proof. Record the
reversing maps, label permutations, time multiplier and normalisation explicitly.
Then implement a rigorous C1 flow enclosure with collision exclusion, validate
the variational equation, and compare the period in the same scale as the paper.
Keep integrator versions, compiler settings and outward-rounding checks in the
run record. NOTE.md's general symmetry description is not that derivation.

Only after a strict inclusion from those validated bounds and an independent
verifier replay may a figure-eight certificate and README result be proposed.
The independent verifier must implement its own arithmetic and flow enclosure;
it must not import this module. Both implementations still need separate review.
