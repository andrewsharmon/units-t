<div align="center">

# units-t

**Exact unit conversion and dimensional analysis for Python, built all the way down to the fundamental constants.**

[![CI](https://github.com/andrewsharmon/units-t/actions/workflows/ci.yml/badge.svg)](https://github.com/andrewsharmon/units-t/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Typed: mypy strict](https://img.shields.io/badge/typed-mypy%20strict-2A6DB2)
![Dependencies: none](https://img.shields.io/badge/dependencies-none-lightgrey)

</div>

```python
>>> from units_t import units as u
>>> print((26.2 * u.mi).to(u.km))
42.1648128 km
```

`units-t` attaches units to numbers, converts between them exactly, and refuses to let
you add metres to seconds. Every unit in the library has an exact definition that goes
back through the SI base units to the seven constants that have defined the SI since 2019.

## Why units-t?

- **Exact by construction.** Conversion factors are rational numbers (`Fraction`), not
  floats. A mile is *exactly* `25146/15625` km, and an electronvolt is *exactly*
  `1.602176634e-19` J.
- **Grounded in physics.** The second, metre, kilogram, ampere, kelvin, mole and candela
  are each tied to a defining constant (Δν_Cs, c, h, e, k_B, N_A, K_cd). Everything else
  is built from those.
- **Dimensional safety.** Every quantity carries its physical dimension, so mistakes like
  `metres + seconds` raise an error instead of returning a wrong number.
- **Zero dependencies.** Pure Python, fully type-annotated (`py.typed`), checked with
  `mypy --strict`.

> **Status: early.** `units-t` is a young project. For mature, full-featured unit
> handling, see [Related projects](#related-projects). The [Direction](#direction)
> section describes what this project is exploring that's new.

## Installation

`units-t` is not on PyPI yet. Install it straight from GitHub:

```bash
pip install git+https://github.com/andrewsharmon/units-t.git
```

or, in a uv project:

```bash
uv add git+https://github.com/andrewsharmon/units-t.git
```

Requires Python 3.11 or newer.

## Quick start

```python
from units_t import units as u
from units_t import constants as const

# Attach a unit by multiplying
speed = 100 * u.km / u.h

# Convert with .to()
print(speed.to(u.m / u.s))        # 27.77777777777778 m/s
print(speed.to(u.m / u.s).value)  # 250/9  (exact Fraction under the hood)

# Physics, straight from the constants: energy of a 500 nm photon
photon = const.h * const.c / (500 * u.nm)
print(photon.to(u.eV))            # 2.479683968664005 eV
```

## Usage guide

### Quantities and conversion

Multiplying a number by a unit gives you a `Quantity`. Use `.to()` to convert it to
any unit with the same dimension.

```python
energy = (2 * u.kW) * (3 * u.h)
print(energy)                              # 6 kW·h
print(energy.to(u.prefixed("mega", u.J)))  # 21.6 MJ

area = (3 * u.ft) ** 2
print(area.to(u.m**2))                     # 0.83612736 m^2
```

Integer and `Fraction` values stay exact through conversion. Floats are converted with
a single multiplication by the exact factor. `str()` shows exact values as decimals,
and `.value` holds the exact value.

### Arithmetic

Quantities support `+`, `-`, `*`, `/`, `**`, negation, `abs()`, comparisons and
hashing. When you add or subtract, the result uses the left operand's unit:

```python
print(1 * u.km + 250 * u.m)       # 1.25 km
print(1 * u.km == 1000 * u.m)     # True
print(1 * u.mi > 1 * u.km)        # True

force = (75 * u.kg) * (9.81 * u.m / u.s**2)
print(force.to(u.N))              # 735.75 N
```

### Dimensional analysis

Every unit and quantity has a `Dimension`. A dimension is a vector of exponents over
the seven SI base dimensions: length **L**, mass **M**, time **T**, current **I**,
temperature **Θ**, amount **N** and luminous intensity **J**.

```python
print(u.V.dimension)                           # L^2·M·T^-3·I^-1
print(force.dimension)                         # L·M·T^-2
print(u.N.is_compatible(u.kg * u.m / u.s**2))  # True
print(u.J == u.N * u.m)                        # True
```

Combining incompatible dimensions raises `DimensionError`:

```python
from units_t import DimensionError

(1 * u.m).to(u.s)
# DimensionError: cannot convert m [L] to s [T]
```

Fractional exponents are supported, for example in noise spectral density:

```python
from fractions import Fraction

noise = u.V / u.Hz ** Fraction(1, 2)
print(noise.dimension)            # L^2·M·T^(-5/2)·I^-1
```

### Fundamental constants

`units_t.constants` holds the seven exact SI defining constants as quantities, plus
constants that follow exactly from them:

| Name          | Constant                    | Value (exact)                  |
| ------------- | --------------------------- | ------------------------------ |
| `delta_nu_Cs` | Caesium hyperfine frequency | 9 192 631 770 Hz               |
| `c`           | Speed of light in vacuum    | 299 792 458 m/s                |
| `h`           | Planck constant             | 6.626 070 15 × 10⁻³⁴ J·s       |
| `e`           | Elementary charge           | 1.602 176 634 × 10⁻¹⁹ C        |
| `k_B`         | Boltzmann constant          | 1.380 649 × 10⁻²³ J/K          |
| `N_A`         | Avogadro constant           | 6.022 140 76 × 10²³ mol⁻¹      |
| `K_cd`        | Luminous efficacy (540 THz) | 683 lm/W                       |
| `R`           | Molar gas constant, N_A·k_B | 8.314 462 618 153 24 J/(mol·K) |
| `F`           | Faraday constant, N_A·e     | 96 485.332 123 310 0184 C/mol  |

```python
light_time = (1 * u.au) / const.c
print(light_time.to(u.minute))    # 8.316746397269274 min
```

### Defining your own units

Create a new unit from an existing one with an exact factor (an `int`, `Fraction` or
decimal string). Floats are not accepted, so definitions stay exact.

```python
furlong = u.yd.scaled(220, "fur")
fortnight = u.day.scaled(14, "fortnight")

print((1 * u.m / u.s).to(furlong / fortnight))  # 6012.884753042234 fur/fortnight

MW = u.prefixed("mega", u.W)      # any of the 24 SI prefixes, quecto to quetta
print((5 * MW).to(u.kW))          # 5000.0 kW
```

### Esoteric units, uncertainty and sources

`units_t.catalog` holds ~700 units: furlongs, bushels (struck, heaped, imperial, and by
weight of wheat), hogsheads, Roman feet, Egyptian royal cubits, Planck lengths, parsecs,
smoots and pinches. They are grouped by quantity or origin (`catalog.length`,
`catalog.volume`, `catalog.ancient` …), and every one is also available by name:

```python
from units_t import catalog as uc

print((1 * u.mi).to(uc.furlong))                 # 8.0 fur
print((1 * uc.bushel).to(u.L))                   # 35.23907016688 L
print((1 * uc.bushel_of_wheat).to(u.kg))         # 27.2155422 kg
print((1 * u.m / u.s).to(uc.furlong_per_fortnight))  # 6012.884753042234 fur/ftn
```

Not every unit has an exact value, and the catalogue says so. Each unit has a
`certainty`, one of `EXACT`, `EXACT_IRRATIONAL` (defined via π, √ or ln and stored to
60 digits), `MEASURED` (CODATA constants, astronomical periods), `CONVENTIONAL`
(competing definitions, like hogsheads or the Scots ell), `ESTIMATED` (archaeological
reconstructions) or `NOMINAL` (a pinch). Each unit also has a `relative_uncertainty`
and a tuple of `sources`:

```python
print(uc.dalton.certainty)                       # Certainty.MEASURED
print(uc.dalton.relative_uncertainty)            # ≈ 3.1e-10 (CODATA 2022)
print(uc.royal_cubit.certainty)                  # Certainty.ESTIMATED
print(uc.pinch.relative_uncertainty)             # None: not quantifiable

print(uc.amphora.conversion(u.L).explain())
# 1 amphora = 25.934336 L (estimated, relative uncertainty ≈ 0.012)
#   - Roman foot (power 3): from surviving rulers and buildings: 0.294-0.297 m
#   sources:
#     * F. Hultsch, Griechische und römische Metrologie, 2nd ed. (1882)
#     ...
```

Uncertainty is tracked as independent *terms* raised to powers, the same way
dimensions are. Shared terms cancel, so correlations come out right:

```python
uc.planck_length.relative_uncertainty            # 1.1e-5 (from G, to the power ½)
(uc.planck_length / uc.planck_time).conversion(uc.speed_of_light).is_exact  # True
uc.solar_mass.conversion(u.kg).relative_uncertainty      # 2.2e-5 (G again)
uc.solar_mass.conversion(uc.earth_mass).is_exact         # True: G cancels
uc.degree.conversion(uc.arcminute).is_exact              # True: π cancels
```

`uc.inexact()`, `uc.with_certainty(...)` and `uc.search("bushel")` list units.
`uc.ALL` is the full registry.

## How it works: down to the constants

```mermaid
flowchart LR
    subgraph C["SI defining constants (exact)"]
        dnu["Δν_Cs"]
        c["c"]
        h["h"]
        e["e"]
        kB["k_B"]
        NA["N_A"]
        Kcd["K_cd"]
    end
    subgraph B["SI base units"]
        s["s"]
        m["m"]
        kg["kg"]
        A["A"]
        K["K"]
        mol["mol"]
        cd["cd"]
    end
    dnu --> s
    c --> m
    h --> kg
    e --> A
    kB --> K
    NA --> mol
    Kcd --> cd
    B --> D["Derived units<br/>N, J, W, V, Ω, T, …"]
    D --> X["Everyday units<br/>km, h, eV, L, mi, lb, …"]
```

A `Unit` is three things: a symbol, a **dimension**, and an exact **scale**, the
`Fraction` that converts one of this unit into the coherent SI unit of the same
dimension. To convert, the library divides one scale by the other and checks that the
dimensions match. Because each scale comes from exact definitions (the 1959 inch, the
fixed value of *e* for the electronvolt, the IAU astronomical unit), the result is exact
too.

## What's included

| Category                   | Units                                                                                              |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| SI base                    | `s` `m` `kg` `A` `K` `mol` `cd`                                                                    |
| SI derived (special names) | `Hz` `N` `Pa` `J` `W` `C` `V` `F` `ohm` `S` `Wb` `T` `H` `lm` `lx` `Bq` `Gy` `Sv` `kat`            |
| Dimensionless              | `one` `rad` `sr`                                                                                   |
| Prefixed shortcuts         | `km` `cm` `mm` `um` `nm` `g` `mg` `ms` `us` `ns` `kHz` `MHz` `GHz` `kJ` `kW` `kPa` `mA` `mV` `kV` |
| Accepted non-SI            | `minute` `h` `day` `L` `mL` `tonne` `au` `eV` `keV` `MeV` `GeV`                                    |
| Imperial / US customary    | `inch` `ft` `yd` `mi` `lb` `oz`                                                                    |

Any unit can take an SI prefix with `u.prefixed(name, unit)`.

`units_t.catalog` adds about 700 more:

| Module            | Highlights                                                                                         |
| ----------------- | -------------------------------------------------------------------------------------------------- |
| `length`          | furlong, chain, rod, link, US survey units, fathom, cable, league, ell, span, hand, smoot, potrzebie |
| `area`            | acre, rood, section, township, barn, shed, circular mil, hide, virgate, morgen, arpent              |
| `volume`          | US and imperial bushels, pecks, gallons and pints; hogshead, tun, firkin; jeroboam to melchizedek   |
| `mass`            | grain, stone, troy and apothecaries' weights, carat, bushels of wheat, corn, oats …                 |
| `time`            | fortnight, Julian/Gregorian/tropical years, sidereal day, synodic month, shake, jiffy, sol         |
| `mechanics`       | knot, Mach, lbf, kgf, poundal, slug, torr, mmHg, inH₂O, psi, poise, stokes                          |
| `energy`          | erg, five calories, six BTUs, therm, quad, ton of TNT, toe, horsepowers, ton of refrigeration      |
| `electromagnetic` | gauss, maxwell, oersted, statcoulomb, abampere, debye                                              |
| `radiation`       | curie, röntgen, rad, rem, banana equivalent dose                                                   |
| `photometry`      | phot, foot-candle, nit, stilb, lambert, foot-lambert                                               |
| `angle`           | degree, gradian, turn, NATO mil, compass point, square degree, spat                                |
| `information`     | bit, byte, kB to QB, KiB to YiB, nat, hartley                                                      |
| `temperature`     | rankine and °F, °Ré, °Rø, °De, °N *intervals*                                                      |
| `typography`      | DTP point, TeX point, pica, twip, Didot point, cicero                                              |
| `astronomical`    | light-year, parsec, IAU nominal solar/planetary units, solar mass, jansky                          |
| `natural`         | Planck units, Hartree atomic units, dalton, electron mass, x units                                 |
| `regional`        | Japanese, Chinese, Hong Kong, Russian, French, Prussian, Spanish, Scots, Irish, Indian, Thai       |
| `ancient`         | Roman, Greek, Egyptian, Babylonian and biblical units; the megalithic yard                         |

## Project layout

```
src/units_t/
├── dimensions.py   # Dimension: exponent vectors over the 7 SI base dimensions
├── unit.py         # Unit: symbol + exact scale + dimension
├── quantity.py     # Quantity: value + unit, with arithmetic and comparison
├── units.py        # core SI, prefixed, non-SI and imperial units
├── catalog/        # ~700 more units, grouped by quantity or origin
├── provenance.py   # Certainty, UncertaintyTerm, Source, Conversion
├── sources.py      # citations for unit definitions
├── constants.py    # fundamental constants as Quantities
├── _defining.py    # exact numerical values of the SI defining constants
├── _irrational.py  # π, ln 2, ln 10, √ to 60 digits
└── exceptions.py   # UnitsError, DimensionError
```

## Related projects

`units-t` builds on ideas from some excellent, mature libraries. If you need a
production-ready units package today, one of these is probably what you want:

- **[Pint](https://github.com/hgrecco/pint)** is the go-to general-purpose units library
  for Python. It has a readable definitions file, NumPy, pandas and uncertainties
  integration, and it can even use `Fraction` or `Decimal` values.
- **[astropy.units](https://docs.astropy.org/en/stable/units/)** and
  **[astropy.constants](https://docs.astropy.org/en/stable/constants/)** are the
  standard in astronomy. They offer fast array support, CODATA constants with
  uncertainties, and "equivalencies" such as wavelength ↔ frequency ↔ energy.
- **[unyt](https://github.com/yt-project/unyt)**, from the yt project, provides NumPy
  arrays with units, SymPy-backed unit expressions, and built-in CGS, MKS and Planck
  unit systems.
- **[sympy.physics.units](https://docs.sympy.org/latest/modules/physics/units/)** offers
  exact, symbolic units and dimension systems inside SymPy.
- **[forallpeople](https://github.com/connorferster/forallpeople)** is a lightweight
  SI library for engineering calculations, with a great Jupyter display.
- **[scipy.constants](https://docs.scipy.org/doc/scipy/reference/constants.html)** is a
  handy table of CODATA values and conversion factors.

`units-t` does not try to out-feature these. It aims to explore a few things none of
them treat as a core focus.

## Direction

1. **Exactness with provenance.** Conversions are exact by default. The goal is for every
   factor to be able to explain itself: *"1 eV = e × 1 V, exact, because e is a
   defining constant"*. Exact values will be kept apart from measured ones, and
   measured ones will carry their CODATA uncertainty.
2. **Unit systems built from the constants.** Pick which constants to set to 1
   (c = ħ = 1, Planck's c = ħ = G = k_B = 1, Hartree atomic units, Gaussian…). The library
   then builds the whole system and its conversions to SI, instead of shipping a fixed
   list of systems.
3. **Dimensional analysis as a first-class tool.** Use Buckingham π to find the
   dimensionless groups in a problem, check that equations are dimensionally
   consistent, and find which combinations of constants produce a given dimension.
4. **Small and dependency-free at the core.** NumPy and other integrations will be
   optional extras.

### Roadmap

- [ ] Measured CODATA constants (G, mₑ, α, …) with uncertainties
- [x] Provenance: sources, certainty and uncertainty for every catalogued unit
- [ ] Provenance: explain the full derivation chain of any conversion factor
- [ ] Natural, Planck, atomic and Gaussian unit systems derived from the constants
- [ ] Buckingham π-theorem tools for dimensional analysis
- [ ] Affine units (°C, °F) and logarithmic units (dB, Np)
- [ ] Uncertainty propagation through conversions
- [ ] Parsing unit expressions (`"kg*m/s^2"`)
- [ ] Optional NumPy array support

## Development

The project uses [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/andrewsharmon/units-t.git
cd units-t
uv sync                      # create .venv and install dev dependencies
uv run pytest                # run the test suite
uv run ruff check .          # lint
uv run ruff format .         # format
uv run mypy                  # type-check (strict)
uv run pre-commit install    # run the checks on every commit
```

CI runs lint, format and type checks, and runs the tests on Python 3.11, 3.12 and 3.13.

## License

MIT. See [LICENSE](LICENSE).
