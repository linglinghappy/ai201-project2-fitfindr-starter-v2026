# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
Two of the three tools call the model. A model call can fail. Also, `parse_query` uses regex. It can miss a price or size written in a new way, like "nothing over thirty dollars". So I allow one miss.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
This path never calls the model. The stop is a fixed `if not results:` check in `agent.py::run_agent`. The same query takes the same path every time. So any miss is a real bug.

---

## 3. Something about state

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

I run 5 queries that reach `suggest_outfit`. Each time, the `id` of `session["selected_item"]` must match the `id` of the item `suggest_outfit` receives. Target: 5 of 5.

**Why this target:**
No model call happens between these two steps. If the ids do not match once, they will not match every time. So one miss means a real bug. I use `id` because it is unique. Two listings can have similar titles.

---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

I make fit cards for 5 different listings. Each card must mention the item's price. Target: at least 4 of 5.

The price counts if the caption shows the number. It can have "$", ".00", "dollars" or "bucks". It must not be part of a bigger number. For a $24 item, "$24" counts, but "$124" does not.

**Why this target:**
The model writes the caption. It can leave out the price, even when the prompt asks for it. So I allow one miss. I check the number's edges so a bigger number does not count by mistake.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

I call `search_listings` directly with the description "vintage". I run 5 searches: size "S", "M", "L", "XL", and "M" with `max_price=30`. Every result must fit the size rule in my README. Target: 5 of 5.

A search fails if:
- it returns a size the rule excludes, like "US 9" for "S" or "XL" for "L", or
- size "M" leaves out a matching "S/M" or "M/L" listing.

**Why this target:**
`search_listings` does not call the model. The same search gives the same result every time. So one miss means a real bug. I test the tool directly. That way, a miss points to the size rule, not to `parse_query`.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
