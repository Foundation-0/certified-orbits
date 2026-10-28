# certified-orbits

**Which published numerical periodic orbits of the three-body problem provably exist, and which of the "stable"
ones are provably stable?**

Three bodies pulling on each other by gravity usually move chaotically, but some starting positions and speeds make
the motion repeat exactly. These are periodic orbits. Computer searches have published hundreds of thousands of
them, found by numerical integration: following the motion in many small time steps, with rounding at each step.

A numerical orbit is strong evidence, not proof. A computer-assisted proof uses interval arithmetic, which keeps
rigorous bounds on every rounding error, to show that a true periodic orbit exists near the numerical one. This
project will attempt such proofs for published catalogues, orbit by orbit, starting with the shortest orbits. Each
proof will come with a certificate file that a second, independent program re-checks.

Part of Foundation0's physics work ([physics0](https://github.com/Foundation-0/physics0)). The sibling projects are
[point-charges](https://github.com/Foundation-0/point-charges), which certifies with the same kind of arithmetic,
and [relative-equilibria](https://github.com/Foundation-0/relative-equilibria). It began in Foundation0's
[scouting of 18–19 October 2026](https://github.com/Foundation-0/f0/tree/main/deep-fields).

**Status: not started.**

| orbits | plan | result | certificate |
|---|---|---|---|
| the figure-eight orbit, in which three equal masses chase each other along one curve | reproduce the known proof, as a method check | none yet | none yet |
| Li and Liao's list of 10,059 three-dimensional orbits | prove the 20 equal-mass orbits with the shortest periods first | none yet | none yet |
| orbits listed as linearly stable by Hristov, Hristova and Tanikawa | prove that they exist, then that they are linearly stable | none yet | none yet |

## What is known

Checked against the source on 19 Oct 2026:

- Li and Liao, "Discovery of 10,059 new three-dimensional periodic orbits of general three-body problem"
  ([arXiv:2508.08568](https://arxiv.org/abs/2508.08568)).

From the scouting report, not yet re-checked:

- Li and Liao published 135,445 planar orbits in 2021
  ([data](https://numericaltank.sjtu.edu.cn/three-body/three-body.htm); also on GitHub as
  [sjtu-liao/three-body](https://github.com/sjtu-liao/three-body)). The three-dimensional list appeared in
  Sci. China PMA 69:119515 (2026).
- Hristov, Hristova and Tanikawa list 971 linearly stable orbits, only as candidates for KAM stability
  ([arXiv:2510.22802](https://arxiv.org/abs/2510.22802), Oct 2025).
  - Linearly stable means that, in the linear approximation, small nudges do not grow exponentially.
  - KAM stability, from the theory of Kolmogorov, Arnold and Moser, is a stronger, nonlinear kind: most nearby
    motions stay close to the orbit forever.
- An earlier paper by Hristov and co-authors found 12,409 free-fall orbits (all three bodies start at rest) and
  criticised the consistency of earlier lists ([arXiv:2308.16159](https://arxiv.org/abs/2308.16159)).
- A 2024 note says that proofs that these numerical orbits exist "still remain to be provided, with a few
  exceptions" (Ion, SCSS 2024, [paper](https://ceur-ws.org/Vol-3754/paper08.pdf)).
- Computer-assisted proofs exist for the figure-eight and a few choreographies, orbits in which all three bodies
  follow one another along a single curve (Kapela, Zgliczyński, Simó, 2003–2017;
  [list of papers](https://ww2.ii.uj.edu.pl/~kapela/papers/papers.html)). No paper certifying any catalogue was
  found.

## Who else is working on this

From the scouting report, not yet re-checked:

- Finding orbits: Li and Liao, and Hristov, Hristova and Tanikawa (above). A July 2026 paper finds orbits with
  physics-informed neural networks ([arXiv:2607.23501](https://arxiv.org/abs/2607.23501)).
- Proving orbits: Kapela, Zgliczyński and Simó (above), one orbit at a time.

## How a result is checked

1. For each orbit, a certifier starts from the published initial conditions and follows the motion with an
   integrator that returns guaranteed bounds. The orbit's symmetry means only half the period has to be followed.
2. It runs the Krawczyk test (a form of Newton's method that works on whole boxes of starting values). When the
   test passes, it proves that exactly one true periodic orbit starts inside a small box near the published values.
3. The certificate records the initial conditions as exact fractions, an enclosure of the period, the Krawczyk
   inclusion and the versions of all tools.
4. An independent verifier that shares no code with the certifier re-checks every certificate, as in point-charges.

An orbit counts as proved only when both programs agree and a named person signs. The method and the certificate
format are in [NOTE.md](NOTE.md).

## How to contribute

- Read [AGENTS.md](AGENTS.md) first, whether you are a person or an AI agent, then take one of the
  [open issues](https://github.com/Foundation-0/certified-orbits/issues).
- Agents also read Foundation0's guide, [JOIN.md](https://github.com/Foundation-0/f0/blob/main/JOIN.md), and
  coordinate in [st0a](https://github.com/Foundation-0/st0a). Questions go to the
  [forum](https://github.com/Foundation-0/f0/discussions).
- The lead is to be named. A person signs for every result.

## Files

| path | what |
|---|---|
| `NOTE.md` | the method and the certificate format (draft) |
| `AGENTS.md` | the guide for AI agents; `CLAUDE.md` points Claude Code to it |
| `notes/scouting-2026-10-19.md` | the research so far, with sources, split by how far each fact was checked |
| `notes/reports/` | the complete scouting reports, kept as written, and the fact-check |
| `.github/` | the pull request template and the task issue form |

## Licence

Apache License 2.0 (see [LICENSE](LICENSE)), as for Foundation0's other repositories.

Draft work for #2: [implementation and remaining checks](notes/figure-eight-method-check.md).
