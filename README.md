# CRNStudio
CRNStudio is an engineering workbench for chemical reaction networks (CRNs). It treats CRNs as engineered systems that must be specified, simulated, and validated with the same rigor as any other engineered product. The goal is to provide a clear intermediate representation, reproducible simulation backends, and simple analysis tools that connect mechanistic models to experimental data.

This initial version focuses on deterministic ordinary differential equation (ODE) simulation driven by a minimal intermediate representation of species, reactions, and rate laws. The public API is intentionally small to support composable extensions without accidental coupling.

## Features

- Minimal CRN representation (Species, Reaction, RateLaw) with explicit mass-action helper utilities

- Deterministic ODE integrator suitable for small and medium models

- Tested examples for mass conservation and reversible reaction dynamics

## Getting started

CRNStudio is currently under active development.

To install in editable mode for experimentation:

pip install -e .

A minimal example demonstrating CRN definition and simulation is provided in the examples and tests directories.

## Scope and roadmap

Future iterations will integrate stochastic simulation, parameter estimation, and experimental data comparison while preserving explicit, auditable model definitions suitable for engineering and scientific use.