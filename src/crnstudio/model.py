"""Core data structures for CRNStudio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, Mapping, MutableMapping


@dataclass(frozen=True)
class Species:
    """A chemical species tracked in the network."""

    name: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Species name must be non-empty")


class RateLaw:
    """A rate law mapping time and concentrations to a scalar reaction rate."""

    def __init__(self, law: Callable[[float, Mapping[str, float]], float]) -> None:
        self._law = law

    def __call__(self, t: float, concentrations: Mapping[str, float]) -> float:
        return self._law(t, concentrations)


@dataclass(frozen=True)
class Reaction:
    """A chemical reaction with stoichiometry and an associated rate law."""

    reactants: Mapping[Species, float]
    products: Mapping[Species, float]
    rate_law: RateLaw

    def __post_init__(self) -> None:
        if not self.reactants:
            raise ValueError("Reaction must have at least one reactant")
        if not self.products:
            raise ValueError("Reaction must have at least one product")
        for stoich in self.reactants.values():
            if stoich <= 0:
                raise ValueError("Reactant stoichiometry must be positive")
        for stoich in self.products.values():
            if stoich <= 0:
                raise ValueError("Product stoichiometry must be positive")

    def net_change(self) -> Dict[Species, float]:
        """Compute net stoichiometric change per reaction event."""

        delta: Dict[Species, float] = {}
        for species, stoich in self.products.items():
            delta[species] = delta.get(species, 0.0) + stoich
        for species, stoich in self.reactants.items():
            delta[species] = delta.get(species, 0.0) - stoich
        return delta


def mass_action(rate_constant: float, reactants: Mapping[Species, float]) -> RateLaw:
    """Create a mass-action rate law parameterized by reactants."""

    if rate_constant < 0:
        raise ValueError("Rate constant must be non-negative")

    def _law(_: float, concentrations: Mapping[str, float]) -> float:
        rate = rate_constant
        for species, stoich in reactants.items():
            rate *= concentrations[species.name] ** stoich
        return rate

    return RateLaw(_law)


def ensure_concentrations(
    species: Iterable[Species], initial_conditions: Mapping[str, float]
) -> Dict[str, float]:
    """Validate and normalize initial concentrations for simulation."""

    concentrations: Dict[str, float] = {}
    for sp in species:
        if sp.name not in initial_conditions:
            raise KeyError(f"Missing initial concentration for species {sp.name}")
        value = initial_conditions[sp.name]
        if value < 0:
            raise ValueError("Concentrations must be non-negative")
        concentrations[sp.name] = float(value)
    return concentrations


def update_concentrations(
    concentrations: MutableMapping[str, float],
    derivatives: Mapping[str, float],
    delta: float,
) -> None:
    """Apply a time step update to concentrations in-place."""

    for name, deriv in derivatives.items():
        concentrations[name] += deriv * delta
