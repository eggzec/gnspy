# gnspy — complete help for GNS Animator4

This repo is the complete documentation site and PyPI package for scripting
GNS Animator4 with `gnspy`: commands, usage guides, scripting tutorials, and
hand-written, fully-typed PEP 484 stub files for the compiled `gnspy` and
`gnsgui` Python extension modules.

The stubs serve two purposes at once:

- **Static typing / IDE autocomplete** — drop-in stubs for the compiled modules.
- **API documentation** — every symbol carries a NumPy-style docstring that
  [griffe](https://mkdocstrings.github.io/griffe/) parses, so the same files can
  feed mkdocstrings. (Docstring-in-stub is intentional; see the ruff notes below.)

Note that `pyproject.toml` (the PyPI package: name, version, stub-checking
tooling) and `zensical.toml` (the docs site: commands/usage/scripting +
generated API reference) intentionally describe the project at different
scopes — one ships the stubs, the other documents the whole product.

## Contents

| File | Classes | Notes |
|------|---------|-------|
| `gnspy.pyi` | 89 API classes + 19 enums | Model, scan, presentation, view, results, GUI-adjacent handles + the global `GNS`/`gns` handle |
| `gnsgui.pyi` | 26 classes | Qt-based widget toolkit for custom dialogs inside Animator |
| `pyproject.toml` | — | PyPI package metadata + ruff/mypy/ty/pyrefly/griffe dev tooling (strict, with documented ignores) |
| `zensical.toml`, `docs/` | — | The documentation site (commands, usage, scripting, API reference) |

## Running the checks

The stub-checking tools are pinned dev dependencies (see `[dependency-groups]`
in `pyproject.toml`), so run them via `uv run`:

```bash
uv run ruff    check          gnspy.pyi gnsgui.pyi
uv run ruff    format --check gnspy.pyi gnsgui.pyi
uv run mypy    --strict --config-file pyproject.toml gnspy.pyi gnsgui.pyi
uv run ty      check          gnspy.pyi gnsgui.pyi
uv run pyrefly check          gnspy.pyi gnsgui.pyi
```

All of the above pass with zero errors.

griffe cannot discover a lone `.pyi` (no companion `.py`); to validate docstring
parsing, place the stub beside an empty module of the same name and run
`uv run griffe dump gnspy -s <dir> -d numpy`. In production, point
mkdocstrings at the installed compiled module and let it merge these stubs.

## Documentation site

The docs site (built with [Zensical](https://zensical.org)) lives under
`docs/` and is configured in `zensical.toml`:

```bash
uv run zensical serve   # preview at localhost:8000
uv run zensical build   # static output in site/
```

## ruff configuration — why `ALL` minus a few rules

`pyproject.toml` selects **every** ruff rule (`select = ["ALL"]`) and ignores only
rules that are fundamentally incompatible with a *documentation-bearing stub that
mirrors an external, non-PEP8 C++ API we do not control*:

- `PYI021`, `D418` — forbid docstrings in stubs / on overloads. We deliberately
  embed NumPy docstrings (including per-overload ones) for griffe/mkdocstrings.
- `N802/N803/N815/N816`, `A002/A003` — the real API is camelCase and uses
  argument names like `id`/`type`/`filter`; renaming would break user calls.
- `FBT001/FBT002` — the real API exposes boolean parameters (e.g. `indirect`).
- `COM812`, `ISC001` — conflict with the formatter.

Every other rule (including the full `D` pydocstyle set under the NumPy
convention, and `PYI*` stub rules) is enforced.

## Caveat — inferred enum integer values

Six enums have integer values taken directly from the source dump and are
authoritative: `Element`, `Property`, `Item`, `View`, `Analysis`, `Function`.

The other 13 enums (`ArrowPosition`, `BorderMode`, `Event`, `FontStyle`,
`FrameSide`, `FunctionItem`, `LabelPosition`, `LegendPosition`, `LineStyle`,
`MarkerStyle`, `PageOrientation`, `PolygonType`, `Presentation`) have member
**names** grounded in the appendix docs, but their integer **values are not
published anywhere** — they are assigned by convention. Each such enum's docstring
says so. Reference these members **by name**, not by numeric value. If the real
integer values are ever recovered (e.g. from a running Animator), update them.
