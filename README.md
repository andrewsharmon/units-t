# units-t

Unit conversion and dimensional analysis for Python, traced all the way down to
fundamental constants.

Every unit in `units-t` is defined as an **exact rational multiple** of the coherent
SI unit for its dimension, and the SI itself is anchored to the seven defining
constants of the 2019 redefinition (Δν_Cs, c, h, e, k_B, N_A, K_cd). Conversions are
therefore exact wherever the underlying definitions are exact. The electronvolt, for
instance, is exactly `1.602176634e-19 J` because the elementary charge is exact.

## Quick start

```python
from units_t import units as u
from units_t import constants as const

speed = 100 * u.km / u.h
print(speed.to(u.m / u.s))  # 27.77777777777778 m/s
print(speed.to(u.m / u.s).value)  # Fraction(250, 9) -- exact

energy = 1 * u.eV
print(energy.to(u.J))  # 1.602176634e-19 J (exact, via the elementary charge)

print(const.c.dimension)  # L·T^-1
```

Dimensional mismatches are caught:

```python
(1 * u.m).to(u.s)  # raises DimensionError
```

## Package layout

| Module                  | Purpose                                                      |
| ----------------------- | ------------------------------------------------------------ |
| `units_t.dimensions`    | `Dimension`: exponent vectors over the 7 SI base dimensions |
| `units_t.unit`          | `Unit`: exact scale factor + dimension + symbol              |
| `units_t.quantity`      | `Quantity`: value attached to a unit, with arithmetic        |
| `units_t.units`         | Catalogue of SI base, derived, prefixed and common units     |
| `units_t.constants`     | SI defining constants (exact, 2019 SI)                       |
| `units_t.exceptions`    | `DimensionError` and other library errors                    |

## Development

The project uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync                       # create .venv and install dev dependencies
uv run pytest                 # run tests
uv run ruff check .           # lint
uv run ruff format .          # format
uv run mypy                   # type-check (strict)
uv run pre-commit install     # optional: run checks on every commit
```

## Roadmap

- [ ] Measured CODATA constants (G, m_e, α, …) with uncertainties
- [ ] Affine units (°C, °F) and logarithmic units (dB, Np)
- [ ] Natural / Planck / atomic / Gaussian unit systems derived from the constants
- [ ] Buckingham π-theorem tooling for dimensional analysis
- [ ] Uncertainty propagation through conversions
- [ ] Unit-expression parsing (`"kg*m/s^2"`)
- [ ] NumPy array support

## License

MIT, see [LICENSE](LICENSE).
