# Independent verifier: input audit and remaining proof work

Status: draft preflight tool. It cannot accept a certificate. Refs #4.

The input audit checks exact rational encodings, positive masses and period,
box dimensions, unknown names and the presence of structured model metadata.
It imports no certifier code. The draft box representation is an object keyed by
unknown name; the certifier's eventual format still needs agreement.

```sh
python3 -m unittest discover -s tests -v
python3 tools/verifier_preflight.py /path/to/proposed-certificate.json
```

Exit 1 means malformed input. Exit 2 means the input passed basic checks but the
proof was not verified. There is no success exit. A certificate's claimed result
and Krawczyk image are never trusted. Tests show that shifted boxes, changed
positive masses and changed positive periods cannot acquire a verified result
merely by passing these structural checks.

The next component must parse a fixed, documented physical model, reconstruct
its shooting equations, and integrate them with independent validated arithmetic
and a C1 integrator. It must rederive the residual, Jacobian and Krawczyk image,
exclude collisions, and check the period and published-value distance. It must
not read the certifier's intermediate enclosures as proof inputs.

Use a separate implementation and dependency path from the certifier, then have
another reviewer inspect that separation. Different files or authors alone do
not establish algorithmic independence. The draft was written in the same task
as the certifier's algebra component and makes no independence claim beyond its
lack of imports or copied arithmetic.

Acceptance remains the figure-eight certificate plus corrupted-box, period and
mass rejections produced by the actual independent integration. None of those
proof runs has occurred. CI currently exercises only input-audit controls.
