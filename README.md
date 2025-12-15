# CRNStudio

CRNStudio is an engineering workbench for chemical reaction networks (CRNs). It treats CRNs as engineered systems that must be specified, simulated, and validated with the same rigor as any other engineered product. The goal is to provide a clear intermediate representation, reproducible simulation backends, and simple analysis tools that connect mechanistic models to experimental data.

This initial version focuses on deterministic ordinary differential equation (ODE) simulation driven by a minimal intermediate representation of species, reactions, and rate laws. The public API is intentionally small to support composable extensions without accidental coupling.

## Features

- Minimal CRN representation (`Species`, `Reaction`, `RateLaw`) with explicit mass-action helper utilities.
- Deterministic ODE integrator suitable for small and medium models without external dependencies.
- Tested examples for mass conservation and reversible reactions.
- Tooling for linting (Ruff), type checking (mypy), and testing (pytest).

## Getting started

Install development dependencies:

```bash
pip install -e .[dev]
```

Run formatting, linting, type checking, and tests:

```bash
ruff format
ruff check
mypy
pytest
```

## Roadmap

Future iterations will integrate stochastic simulation, parameter estimation, and experimental data comparison while preserving the explicit, auditable model definitions that engineers expect.
