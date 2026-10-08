# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps you shop for secondhand clothes. You describe what you want, like "vintage graphic tee under $30", and it searches 40 thrift listings by keywords, size, and price. It takes the best match and suggests one or two outfits using clothes you already own. It then writes a short caption you could post about the find.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Finds listings that match the user's words. It can also filter by size and price.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->`description` (str), `size` (str or None), `max_price` (float or None)
- **Returns:** A list of up to 10 listing dicts, best match first. Each dict has `id`, `title`, `description`, `category`, `style_tags` (list), `size`, `condition`, `price` (float), `colors` (list), `brand` (str or None), and `platform`.
- **When it has nothing:** An empty list `[]`. Not None. Not an error.
- **How it matches:** The description is split into lowercase words, and small words like "a", "the", "under" are dropped. Each listing scores one point for every word that appears in its `title`, `description`, or `style_tags`. Listings that score 0 are dropped.
- **Size match rule:** Sizes are split on "/" and text in brackets is removed. Two sizes match if they share a part. Case does not matter. So "M" matches "S/M", and "XL" matches "XL (oversized)". But "S" does not match "US 9", and "L" does not match "XL". "W30" does not match "W30 L30", and "One Size" does not match other sizes.
- **Price rule:** `max_price` is inclusive. A $30 item matches `max_price=30`.

### `suggest_outfit`

- **What it does:** Asks the model for one or two outfits. Each outfit pairs the new item with clothes the user already owns.
- **Inputs:** `new_item` (dict, one listing), `wardrobe` (dict with an `items` key; `items` is a list of wardrobe item dicts, each with `id`, `name`, `category`, `colors`, `style_tags`, and `notes`)
- **Returns:** A non-empty string with one or two outfit ideas. Each idea names real pieces from the wardrobe.
- **When it has nothing:** If the wardrobe is empty (`{"items": []}`), it returns general styling tips for the item. It still returns a non-empty string. Never "" and never an error.

### `create_fit_card`

- **What it does:** Asks the model to write a short social media caption about the find.
- **Inputs:** `outfit` (str, the text from `suggest_outfit`), `new_item` (dict, one listing)
- **Returns:** A caption of 2 to 4 sentences. It names the item, its price, and its platform once each.
- **When it has nothing:** If `outfit` is empty or only spaces, it returns "No outfit to caption yet." It does not call the model.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` that names what was searched and what the user could change (broader words, a different size, a higher price), and stop before `suggest_outfit`. Otherwise, take the first result as `session["selected_item"]` and pass it to `suggest_outfit`. Then pass the outfit to `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::parse_query`. It looks for a price like "under $30" and a size like "size M" or ", M" at the end. Whatever is left becomes the description. It does not use the model. Limit: it misses prices written in words, like "under thirty dollars".

**What moves through the session:** `query` → `parsed` (description, size, max_price) → `search_results` → `selected_item` (the first result) → `outfit_suggestion` → `fit_card`. If the search is empty, the run stops and only `error` is filled in after `search_results`.
<!-- regex, string splitting, or asking the model — say which -->


**What moves through the session:** `query` → `parsed` (description, size, max_price) → `search_results` → `selected_item` (the first result) → `outfit_suggestion` → `fit_card`. If the search is empty, the run stops and only `error` is filled in after `search_results`.<!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: **Outfit 1: Casual Y2K Streetwear** * Y2K Baby Tee — Butterfly Print * Baggy straight-leg jeans, dark wash * C…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Butterflies are officially back, and this vintage baby tee is giving major 2000s mall-goth-meets-sweetheart en…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Casual Y2K Streetwear**
* Y2K Baby Tee — Butterfly Print
* Baggy straight-leg jeans, dark wash
* Chunky white sneakers
* Black crossbody bag

**Outfit 2: Edgy Contrast**
* Y2K Baby Tee — Butterfly Print
* Wide-leg khaki trousers
* Vintage black denim jacket
* Black combat boots

  Fit card: Butterflies are officially back, and this vintage baby tee is giving major 2000s mall-goth-meets-sweetheart energy. Style it low-key with baggy denim and chunky kicks, or toughen it up with wide-leg khakis and combat boots. Grab this gem on my Depop right now for just $18! 🦋✨

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

`search_listings` — no model call. Every result is $30 or less.

```
$ python -c "from tools import search_listings; [print(l['id'], l['title'], l['price'], l['size']) for l in search_listings('graphic tee', max_price=30)]"
lst_002 Y2K Baby Tee — Butterfly Print 18.0 S/M
lst_006 Graphic Tee — 2003 Tour Bootleg Style 24.0 L
lst_017 Mesh Long-Sleeve Top — Black 15.0 S/M
lst_033 Vintage Band Tee — Faded Grey 19.0 L
lst_011 Low-Rise Cargo Pants — Khaki 27.0 W29
lst_015 Vintage Graphic Hoodie — Faded Black 26.0 L

$ python -c "from tools import search_listings; print(search_listings('designer ballgown', max_price=5))"
[]
```

`suggest_outfit` — with the example wardrobe. Every piece it names is in the wardrobe.

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
**Outfit 1: Casual Streetwear**
Pair the Vintage Levi's 501 Jeans with the White ribbed tank top and the Chunky white sneakers. Layer on the Vintage black denim jacket and accessorize with the Brown leather belt and the Black crossbody bag. 

**Outfit 2: Relaxed Layers**
Combine the Vintage Levi's 501 Jeans with the Oversized grey crewneck sweatshirt and the Black combat boots. Cinch the waist with the Brown leather belt and complete the look using the Black crossbody bag.
```

`suggest_outfit` — with an empty wardrobe. It gives general tips, not "" and not an error.

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_empty_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_empty_wardrobe()))"
**Casual Everyday:** Pair the vintage 501s with a classic white crewneck t-shirt and a canvas belt. Layer an unbuttoned flannel shirt or a black zip-up hoodie over top. Finish the look with white canvas sneakers or worn-in leather boots for an effortless, timeless aesthetic. 

**Smart-Casual:** Dress up the medium-wash denim by tucking in a crisp black or navy turtleneck. Add a structured leather belt and a vintage leather jacket. Complete the outfit with minimalist leather loafers or sleek black ankle boots for a sharp, elevated contrast.
```

`create_fit_card` — run three times with the cache on. All three are word-for-word the same, because the cache returned the first answer.

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the effortless, off-duty model vibe of a properly broken-in medium wash. Paired these vintage Levi's 501 jeans with my go-to white sneakers for that ultimate 90s casual look. Grabbed them for just $38 and they are officially live on my Depop shop—run, don't walk!

$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the effortless, off-duty model vibe of a properly broken-in medium wash. Paired these vintage Levi's 501 jeans with my go-to white sneakers for that ultimate 90s casual look. Grabbed them for just $38 and they are officially live on my Depop shop—run, don't walk!

$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the effortless, off-duty model vibe of a properly broken-in medium wash. Paired these vintage Levi's 501 jeans with my go-to white sneakers for that ultimate 90s casual look. Grabbed them for just $38 and they are officially live on my Depop shop—run, don't walk!
```

`create_fit_card` — run three times with the cache off. All three are different. `TEMPERATURE` is 0.9, so the identical runs above came from `CACHE_ENABLED`, not temperature.

```
$ AI201_CACHE=0 python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the effortless 90s off-duty model vibe of a properly broken-in medium wash. Paired these vintage Levi's 501 jeans with my go-to white sneakers and honestly, I never want to take them off. Snagged them for just $38 over on my Depop—run, don't walk!

$ AI201_CACHE=0 python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the effortless 90s off-duty model vibe of a perfectly worn-in pair of vintage Levi's 501 jeans. Just paired them with my go-to white sneakers for that ultimate effortless look that goes with literally everything. Grab these medium wash staples over on my depop right now for just $38!

$ AI201_CACHE=0 python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the way broken-in denim hugs you just right. These vintage Levi's 501 jeans in a classic medium wash give off major effortless off-duty model energy when paired with crisp white sneakers. Snagged them for just $38—run, don't walk, over to my Depop before I change my mind and keep them for myself!
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I gave Claude the `_size_tokens` helper I wrote in class and asked it to add it to `tools.py`.
- *What came back:* It pointed out a bug. I wrote `p.strip().upper` without `()`. That returns the method, not the uppercase text. So the size filter would never match anything.
- *What I changed:* I changed it to `p.strip().upper()`. Then I tested it. `"S/M (fits like M)"` gave `{"S", "M"}`, and `None` gave an empty set.


**Moment 2**

- *What I asked for:* I asked Claude to write `suggest_outfit`. I wanted it to use only clothes from the user's wardrobe.
- *What came back:* The prompt told the model to name each piece exactly as it is written in the wardrobe list.
- *What I changed:* I did not trust it right away. I checked all 7 pieces the model named against the example wardrobe. All 7 were real, with exact names. I kept the prompt and added the test to my Sample Run.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'vintage graphic tee under $30' --trace
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: **Outfit 1: Casual Y2K Streetwear** * Y2K Baby Tee — Butterfly Print * Baggy straight-leg jeans, dark wash * C…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Butterflies are officially back, and this vintage baby tee is giving major 2000s mall-goth-meets-sweetheart en…

0 model calls this session, 2 served from cache
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit

  Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.

0 model calls this session
```

The empty search stops at step 3. The happy path goes on to step 5. So the branch works.

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->
I registered `search_listings` in `mcp_server.py`, with typed inputs and a description. `agent.py::_search` now calls it with `mcp_client.call_tool`. Nothing behaved differently. I called the tool both ways with `'graphic tee'` and `max_price=30`. Both returned a list of 6 dicts, with the same ids in the same order. Prices stayed floats (`18.0`), and `brand` stayed `None`. One thing to know: `_search` falls back to the direct call if MCP fails, without a warning. So if MCP breaks, the trace would still say "via MCP".


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
