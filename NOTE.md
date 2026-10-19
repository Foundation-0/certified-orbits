# Proving that numerical three-body orbits exist: method and certificate format

*Draft written on 19 October 2026 by Claude (an AI model by Anthropic) when this repository was set up. Not checked
by a person. Nothing here has been run yet. The method is the one proposed in the scouting report: an interval
Newton–Krawczyk proof on each orbit's symmetric half-period shooting map. This note explains what that means.*

## 1. The problem

Three bodies with masses $m_1,m_2,m_3$ move in the plane or in space under Newton's law (with $G=1$):

$$\ddot q_i=\sum_{j\ne i} m_j\,\frac{q_j-q_i}{|q_j-q_i|^3},\qquad i=1,2,3.$$

Write $x=(q,\dot q)$ for the state and $\varphi_t(x)$ for the state reached after time $t$. A periodic orbit of
period $T$ is a state $x^*$ with $\varphi_T(x^*)=x^*$.

A catalogue prints, for each orbit, initial conditions and a period to some number of digits. A proof shows that a
true periodic orbit exists within a stated distance of the printed initial conditions, with a period inside a
stated interval. The certificate gives that distance, so a reader can see how close the true orbit is to the
published one.

## 2. Making the solution isolated

The Krawczyk test (Section 4) needs an isolated solution with an invertible derivative. A periodic orbit is never
isolated in the full space of states, because each orbit comes with copies:

| copy | how to remove it |
|---|---|
| shifted in time (every point of the orbit is a starting point) | fix the starting point, for example by starting on a symmetry's fixed set (Section 3) |
| translated, or moving with constant velocity | put the centre of mass at the origin, at rest |
| rotated | fix the orientation |
| rescaled: if $q(t)$ is a solution, so is $s\,q(s^{-3/2}t)$ | fix the scale, through the energy or the period, as the catalogue does |

After these are fixed, the period becomes one more unknown.

## 3. Symmetric half-period shooting

A *reversing symmetry* is a map $R$ of states that turns solutions into solutions run backwards:
$R(\varphi_t(x))=\varphi_{-t}(R(x))$. For example, mirror all positions in a line and reverse all velocities.

Let $R$ and $S$ be reversing symmetries. If the starting state $x_0$ is fixed by $R$, and the state at time $\tau$
is fixed by $S$, then

$$\varphi_{2\tau}(x_0)=S\,R\,x_0 .$$

So after time $2\tau$ the orbit is back at its start with the ordinary symmetry $SR$ applied. If $(SR)^k$ is the
identity, the orbit closes with period $2k\tau$. With $S=R$ it closes after $2\tau$.

This shrinks the problem. The unknowns are the free coordinates of $x_0$ inside the fixed set of $R$, and $\tau$.
The equations say that $\varphi_\tau(x_0)$ lies in the fixed set of $S$. Call this system $G(z)=0$. With a suitable
choice of $R$, $S$ and the normalisation of Section 2, it is square. Which symmetries each catalogue's orbits have,
and the resulting system, must be worked out per catalogue.

## 4. The Krawczyk test

Take a box $X$ of unknowns around the numerical solution, its centre $z_0$, an approximate inverse $C$ of the
derivative $DG(z_0)$, and an interval enclosure $DG(X)$ of the derivative over the whole box. Let

$$K(X)=z_0-C\,G(z_0)+\bigl(I-C\,DG(X)\bigr)(X-z_0).$$

If $K(X)$ lies inside the interior of $X$, then $G$ has exactly one zero in $X$, and its derivative is invertible
there. The $\tau$ component of $K(X)$, multiplied by $2k$, then encloses the period.

Both $G(z_0)$ and $DG(X)$ need the flow and its derivative with respect to the starting state, with guaranteed
bounds. A rigorous integrator that also encloses this derivative (a $C^1$ integrator) provides both. Options
named in the scouting report: the CAPD library, or TaylorIntegration.jl with IntervalArithmetic.jl.

## 5. Long and unstable orbits: multiple shooting

On a very unstable orbit, small errors grow fast, and one long integration gives enclosures too wide for the test
to pass. Multiple shooting splits the orbit at points $z_1,\dots,z_m$ with travel times $h_1,\dots,h_{m-1}$. It
solves $\varphi_{h_i}(z_i)=z_{i+1}$ for all $i<m$ at once, together with the symmetry conditions at the two ends.
Each piece is short, so its enclosure stays tight. The Krawczyk test runs on the whole system.

## 6. Stability

The monodromy matrix $M=D\varphi_T(x^*)$ describes how small nudges to the orbit evolve over one period. Some of
its eigenvalues equal 1 because of the copies in Section 2. After those are removed, the orbit is linearly stable
when all remaining eigenvalues lie on the unit circle.

An enclosure alone cannot show that an eigenvalue lies exactly on the circle, but the structure of the problem
helps. The flow conserves a symplectic form (the geometric structure of Hamiltonian mechanics), so the eigenvalues
of $M$ come in sets $\{\lambda,\bar\lambda,1/\lambda,1/\bar\lambda\}$.

If a small region that the map
$\lambda\mapsto 1/\bar\lambda$ sends to itself holds exactly one eigenvalue (counted with
multiplicity), that eigenvalue equals its own image, so it lies on the circle. An enclosure of $M$ is therefore
enough to prove linear stability when the eigenvalues are well separated.

KAM stability (most nearby motions stay close to the orbit forever) needs much more work, and is not planned yet.

## 7. Certificate format (draft)

One JSON file per orbit in `certificates/`, modelled on the certificates of
[point-charges](https://github.com/Foundation-0/point-charges). Numbers that the proof depends on are stored as
exact rationals, written as strings.

| field | content |
|---|---|
| `orbit` | the catalogue, its version or download date, and the orbit's identifier in it |
| `published` | the initial conditions and period exactly as printed, and how many digits they have |
| `masses` | exact rationals |
| `initial_conditions` | the starting values used, as exact rationals: the printed decimals converted exactly (never through floating point), or refined values (Section 8) |
| `normalisation` | how the centre of mass, the orientation, the scale and the labels are fixed |
| `symmetry` | the reversing symmetries $R$ and $S$, and $k$ |
| `unknowns`, `box` | the names of the unknowns and the box $X$ |
| `distance_to_published` | the largest distance from the printed initial conditions to a point of $X$ |
| `period` | an enclosure $[T_{\min},T_{\max}]$ of the period |
| `krawczyk` | an enclosure of $K(X)$ and of $\lVert I-C\,DG(X)\rVert$; the claim is $K(X)\subset\operatorname{int}X$ |
| `shooting_points` | for multiple shooting, the box of every point and travel time |
| `stability` | optional: an enclosure of the reduced monodromy matrix and the regions holding its eigenvalues |
| `integrator` | method, order and step-size rule |
| `tools` | names and versions of every program and library, the compiler, hardware and run time |
| `result` | `certified`, or `failed` with the reason (enclosures blew up, too few printed digits, test failed) |

**Independent verifier.** A second program that shares no code with the certifier, as in point-charges. It reads
`masses`, `initial_conditions`, `normalisation`, `symmetry` and `box`, then:

1. integrates with its own rigorous integrator and its own arithmetic, for example a Taylor-series integrator on
   Arb balls from python-flint (numbers stored as a midpoint and a guaranteed error radius) if the certifier uses
   CAPD;
2. recomputes $G(z_0)$, $DG(X)$ and $K(X)$, and checks $K(X)\subset\operatorname{int}X$;
3. checks the period enclosure and the distance to the published values.

An orbit counts as proved only when both programs accept its certificate.

## 8. Risks and when to stop

From the scouting report, not yet re-checked:

- Long, very unstable orbits blow up interval enclosures, so multiple shooting is needed.
- Some initial conditions may be printed with too few digits. Then the box around the printed values has to be
  wide, or the values refined numerically first. The certificate then records the printed and the refined values.
- Stop if fewer than half of the 50 shortest orbits certify within two weeks.
