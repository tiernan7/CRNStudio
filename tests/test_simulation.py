from crnstudio import DeterministicSimulator, Reaction, Species, mass_action


def test_mass_conservation() -> None:
    a = Species("A")
    b = Species("B")

    reaction = Reaction(
        reactants={a: 1.0},
        products={b: 1.0},
        rate_law=mass_action(1.0, {a: 1.0}),
    )

    simulator = DeterministicSimulator([a, b], [reaction])
    snapshots = simulator.simulate(t_span=[0.0, 5.0], initial_conditions={"A": 1.0, "B": 0.0}, dt=0.01)

    totals = [state["A"] + state["B"] for state in snapshots]
    assert max(abs(total - 1.0) for total in totals) < 1e-3


def test_reversible_reaction_equilibrium() -> None:
    a = Species("A")
    b = Species("B")

    forward = Reaction(
        reactants={a: 1.0},
        products={b: 1.0},
        rate_law=mass_action(1.0, {a: 1.0}),
    )
    reverse = Reaction(
        reactants={b: 1.0},
        products={a: 1.0},
        rate_law=mass_action(0.5, {b: 1.0}),
    )

    simulator = DeterministicSimulator([a, b], [forward, reverse])
    snapshots = simulator.simulate(t_span=[0.0, 20.0], initial_conditions={"A": 1.0, "B": 0.0}, dt=0.01)

    final_state = snapshots[-1]
    ratio = final_state["B"] / final_state["A"]
    assert 1.8 < ratio < 2.2  # Expect roughly 2:1 at equilibrium
