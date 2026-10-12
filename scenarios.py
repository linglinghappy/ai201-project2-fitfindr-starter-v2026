"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # Criterion 3 — state. Compare selected_item.id with
        # outfit_input_id and fit_card_input_id in the session.
        "name": "state: selected item reaches both tools",
        "query": "black combat boots",
        "wardrobe": "example",
        "criterion": 3,
    },
    # Criterion 4 — fit card mentions the price, 5 different listings.
    {"name": "fit card price: baby tee ($18)",       "query": "vintage graphic tee under $30", "wardrobe": "example", "criterion": 4},
    {"name": "fit card price: cardigan ($35)",       "query": "pink cardigan under $40",       "wardrobe": "example", "criterion": 4},
    {"name": "fit card price: levi's 501 ($38)",     "query": "levi's 501 jeans",              "wardrobe": "example", "criterion": 4},
    {"name": "fit card price: track jacket ($45)",   "query": "90s track jacket",              "wardrobe": "example", "criterion": 4},
    {"name": "fit card price: corduroy pants ($32)", "query": "corduroy wide-leg pants",       "wardrobe": "example", "criterion": 4},
    # Criterion 5 is tested by calling search_listings directly, outside
    # run_eval.py — see results/criterion5_direct.txt.
    #
    # TODO: add what your criteria 3, 4 and 5 need.
    #
    # Set "criterion" to the number in criteria.md that the scenario tests.
    # "criterion": None means a diagnostic run — useful to have, but it isn't
    # one of your five, and run_eval.py marks it as such in the table.
    #
    # For a state criterion, any normal query works — what you're checking is
    # what ends up in the session, not what the user typed.
    #
    # For a fit-card criterion, you probably want the SAME query listed more
    # than once, or several different items, depending on what your criterion
    # actually says.
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
