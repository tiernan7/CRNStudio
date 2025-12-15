"""Deterministic ODE simulation backend."""

from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, Sequence

from .model import Reaction, Species, ensure_concentrations, update_concentrations


class DeterministicSimulator:
    """Fixed-step Runge–Kutta 4 ODE integrator for CRNs."""

    def __init__(
        self,
        species: Sequence[Species],
        reactions: Sequence[Reaction],
    ) -> None:
        if not species:
            raise ValueError("At least one species is required")
        self.species = list(species)
        self.reactions = list(reactions)

    def derivative(self, t: float, concentrations: Mapping[str, float]) -> Dict[str, float]:
        changes: Dict[str, float] = {sp.name: 0.0 for sp in self.species}
        for reaction in self.reactions:
            rate = reaction.rate_law(t, concentrations)
            for species, stoich in reaction.net_change().items():
                changes[species.name] += stoich * rate
        return changes

    def simulate(
        self,
        t_span: Sequence[float],
        initial_conditions: Mapping[str, float],
        dt: float,
    ) -> List[Dict[str, float]]:
        if len(t_span) != 2 or t_span[1] <= t_span[0]:
            raise ValueError("t_span must be [t0, t1] with t1 > t0")
        if dt <= 0:
            raise ValueError("Time step must be positive")

        t0, t1 = float(t_span[0]), float(t_span[1])
        concentrations = ensure_concentrations(self.species, initial_conditions)
        snapshots: List[Dict[str, float]] = [dict(concentrations)]

        steps = int((t1 - t0) / dt)
        t = t0
        for _ in range(steps):
            k1 = self.derivative(t, concentrations)
            mid1 = {name: conc + 0.5 * dt * k1[name] for name, conc in concentrations.items()}

            k2 = self.derivative(t + 0.5 * dt, mid1)
            mid2 = {name: conc + 0.5 * dt * k2[name] for name, conc in concentrations.items()}

            k3 = self.derivative(t + 0.5 * dt, mid2)
            end_state = {name: conc + dt * k3[name] for name, conc in concentrations.items()}

            k4 = self.derivative(t + dt, end_state)

            derivatives = {
                name: (k1[name] + 2 * k2[name] + 2 * k3[name] + k4[name]) / 6.0
                for name in concentrations
            }
            update_concentrations(concentrations, derivatives, dt)
            t += dt
            snapshots.append(dict(concentrations))

        return snapshots
