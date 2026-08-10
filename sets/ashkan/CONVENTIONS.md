# CONVENTIONS

Units, signs, normalisations and notation, fixed **before** a derivation or a line of code depends
on them (Law 2 in [AGENTS.md](AGENTS.md)). Most silent errors in this field are sign errors and
factors of two; this file is the defence against them.

Entries here are *our choices*, not claims about the world, so they need no source. But whenever a
source uses a different convention, record the translation here and cite it — a mistranslated
convention is how a wrong result acquires a correct-looking derivation.

## How to add an entry

State the choice, why it was chosen if it is not obvious, and where it first mattered. Keep entries
short. When a source disagrees, add a translation line: *"`[S:Key §2]` uses X; ours is Y; convert
with Z."*

## Baseline

- **Units.** SI throughout, in code and in notes. Quantities that are naturally reported in other
  units (recoil energy, µK, Gauss, ħ = 1) may be *displayed* in those units, but the stored value
  and every function signature is SI. Any function taking or returning non-SI values says so in its
  name or docstring.
- **Constants.** Physical constants come from `scipy.constants`, never from a literal typed into a
  script. System-specific values (masses, transition frequencies, coupling constants) are cited to
  a registered source and defined in one place per simulation.
- **Angles and phases.** Radians. Phases are accumulated in radians and unwrapped explicitly; no
  implicit `mod 2π`.
- **Numerics.** Double precision (`float64`/`complex128`) by default. Any reduced precision is a
  documented choice with a convergence check behind it.

## Notation

- Vectors are bold in LaTeX (`\vb` or `\mathbf`), plain in code.

## Sign and normalisation choices

*(To be filled when first touched.)*

## Source translations

One row per registered source whose conventions differ from ours. Convert **on entry** — at the
point where a number or an equation is taken out of the paper — never midway through a derivation.

_none yet_
