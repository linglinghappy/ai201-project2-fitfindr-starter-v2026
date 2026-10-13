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
| 1. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected_item reaches suggest_outfit unchanged | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's price (5 listings) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Size filter follows the size rule | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Criteria 1–4 come from `python run_eval.py --label before` (`results/run_2026-10-12_1524_before.md`, caching off, 80 model calls). For criterion 4, Try N means the Nth run of each of the 5 listings. All 25 fit cards had the right price. Criterion 5 does not call the model, so I called `search_listings` directly (`results/criterion5_direct.txt`).

**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Criterion 1** — `agent.py::run_agent`, try 1. All three tools ran and a fit card came back:

```
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
  try 1: completed — fit card 364 chars
```

**Criterion 2** — `agent.py::run_agent` (the branch) and `agent.py::_nothing_found_message`, try 1:

```
[2] search_listings (via MCP)
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit
  try 1: stopped early — Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
```

**Criterion 3** — `agent.py::run_agent`, try 1. The same item goes from select_item into both tools:

```
[3] select_item
      out: Oversized Flannel Shirt — Plaid Red/Black ($22.0, thredUp)
[4] suggest_outfit
      in:  Oversized Flannel Shirt — Plaid Red/Black ($22.0, thredUp)
[5] create_fit_card
      in:  Oversized Flannel Shirt — Plaid Red/Black ($22.0, thredUp)
```

`run_eval.py` doesn't print the ids, so I matched the item shown in the trace at each step. It was the same in all 5 tries.

**Criterion 4** — `tools.py::create_fit_card`, baby tee try 1. The price ($18) is in the caption:

```
Butterfly print baby tees are having a major moment right now, and this Y2K thrift find is literally everything. I styled it two ways: super casual with baggy dark wash denim, and then flipped the script with khaki trousers and chunky combat boots for that effortless edgy contrast. Grab this exact piece over on my Depop for just $18 before someone else snags it!
```

**Criterion 5** — `tools.py::search_listings`, called directly with description `"vintage"` (no model):

```
size=S max_price=None: 3 results -> [('S/M', 18.0), ('S', 42.0), ('S', 52.0)]
size=M max_price=None: 10 results -> [('S/M', 18.0), ('M', 45.0), ('M', 30.0), ('M/L', 38.0), ('M', 16.0), ('M', 75.0), ('M', 18.0), ('M', 28.0), ('M', 25.0), ('M', 27.0)]
size=L max_price=None: 5 results -> [('L', 24.0), ('L', 40.0), ('L', 26.0), ('M/L', 38.0), ('L', 19.0)]
size=XL max_price=None: 3 results -> [('XL (oversized)', 22.0), ('XL (fits oversized)', 20.0), ('XL', 21.0)]
size=M max_price=30: 7 results -> [('S/M', 18.0), ('M', 30.0), ('M', 16.0), ('M', 18.0), ('M', 28.0), ('M', 25.0), ('M', 27.0)]
```

No size the rule excludes shows up: "L" does not return "XL" or "W30 L30". "M" includes both "S/M" and "M/L". With max_price=30, every result is $30 or less.

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
| 1 | Full three-tool run returns a fit card | 4 of 5 | MET (5/5) | All 5 tries reached create_fit_card and returned a non-empty card (276–364 chars). |
| 2 | Impossible query stops before suggest_outfit | 5 of 5 | MET (5/5) | All 5 traces end at `[3] branch` with no suggest_outfit step, and session["error"] names what to change. |
| 3 | selected_item reaches suggest_outfit unchanged (revised) | 5 of 5 | MET (5/5) | In all 5 traces the listing at select_item, suggest_outfit and create_fit_card is the same. |
| 4 | Fit card mentions the item's price | 4 of 5 | MET (5/5) | 25 fit cards (5 listings × 5 tries). Every one had the exact price, e.g. "$18". |
| 5 | Size filter follows the size rule | 5 of 5 | MET (5/5) | 5 direct searches. No excluded size appeared, "M" included S/M and M/L, and max_price=30 kept every result at $30 or less. |

**Diagnoses**

No criterion missed. All five were 5 of 5.

Were my targets too low? Partly, yes.

- Criteria 2, 3 and 5 don't depend on the model. The search, the branch and the session are deterministic, so 5 of 5 was expected. They show the code is right, but they don't test anything that varies.
- Criterion 1 aimed at 4 of 5 and got 5 of 5. The only model-dependent risk is a ModelUnavailable error, and that didn't happen in this run.
- Criterion 4 is the one I would tighten. It aimed at 4 of 5 and passed 25 of 25 cards. My prompt in `tools.py::create_fit_card` gives the price, and the model copies it every time, so "mentions the price" is too easy. I would make it 5 of 5 and add a check the model can actually fail, like a length a person would post: 19 of the 25 cards were longer than 300 characters.

Criterion 3 was revised, not missed. As written, it compares ids, and `run_eval.py` doesn't print them. See the revision in `criteria.md`.



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

### Failure Modes

**1. Empty search.** The agent stops before `suggest_outfit` and says what to change.

```
$ python app.py ask 'designer ballgown size XXS under $5'

  Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.

0 model calls this session
```

**2. Empty wardrobe.** `suggest_outfit` gets 0 wardrobe items. It gives general advice, not a crash and not an empty string.

```
$ python app.py ask 'vintage graphic tee under $30' --empty-wardrobe --trace
(running with an empty wardrobe)
...
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: **Look 1: Casual Streetwear** Pair the baby tee with classic mid-rise blue straight-leg jeans and white canvas…
      →    0 wardrobe item(s)
[5] create_fit_card
      ...

  Outfit:   **Look 1: Casual Streetwear**
Pair the baby tee with classic mid-rise blue straight-leg jeans and white canvas sneakers. Add a small shoulder bag and a simple silver chain necklace to lean into the effortless Y2K aesthetic.

**Look 2: Sweet & Sporty**
Tuck the tee into a pleated white tennis skirt and layer with chunky white platform sneakers or retro trainers. Throw on a pastel pink zip-up hoodie over your shoulders for cool evenings, completing a playful, nostalgic weekend outfit.
```

**3. Model unavailable.** I used a wrong key and turned the cache off, so the model was really called. The agent did not hang and did not show a stack trace. It kept the search results and said what to fix.

```
$ GEMINI_API_KEY=bad_key_x AI201_CACHE=0 python app.py ask 'black leather boots size 8'
...
[3] select_item
      out: Platform Mary Janes — Black Patent ($55.0, depop)
[4] model unavailable
      →    stopping, search results kept

  The model couldn't be reached, so the outfit and caption steps didn't run. The search worked — 10 listing(s) were found. Check GEMINI_API_KEY in your .env, then run the same query again.
What the service said: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

1 model calls this session
```

None of the three crashed or went silent. The handler for the model error is the `except ModelUnavailable` block in `agent.py::run_agent`.

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

**What I changed:** One line in the prompt in `tools.py::create_fit_card`. I added "Keep the whole caption under 300 characters." Nothing else changed: same tools, same loop, same scenarios, same temperature (0.9). (I left out a space, so the prompt reads "once each.Keep the whole caption…". The model still followed it, and I kept it that way so the code matches the run.)

**Which failure it was meant to fix:** My diagnosis said criterion 4 was too easy and the real problem was length: 19 of the 25 fit cards in the before run were over 300 characters, up to 406. The prompt asked for "2 to 4 sentences" but never set a length, so the model wrote long sentences with many clauses.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected_item reaches suggest_outfit unchanged (revised) | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's price (5 listings) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Size filter follows the size rule | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:** Yes. From `results/run_2026-10-12_1524_before.md` to `results/run_2026-10-12_1813_after.md`:

| Fit cards (criterion 4, 25 cards) | Before | After |
|---|---|---|
| Over 300 characters | 19 of 25 | 0 of 25 |
| Longest card | 406 chars | 261 chars |
| Price mentioned | 25 of 25 | 25 of 25 |

The risk was that shorter captions would drop the price. They didn't: all 25 still have it. The other four criteria didn't change, which is what I expected, since search, the branch and the session don't touch this prompt. Criterion 5 calls `search_listings` directly and that code didn't change, so I didn't re-run it.

An after-run card, `tools.py::create_fit_card`, from the "fit card price: track jacket ($45)" scenario, try 5 (161 chars):

```
Channeling major 90s athletic energy with this navy & white track jacket! Grab it for $45 on Poshmark and style it baggy with jeans or prep it up with khakis. ✨👟
```



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

No criterion is still missed: all five were 5 of 5 before and after. But some things are still broken that my criteria don't catch.

1. **Search picks the wrong item.** For "black combat boots", all 10 runs selected "Oversized Flannel Shirt — Plaid Red/Black". `tools.py::search_listings` scores by how many query words appear, so "black" pulls the shirt to the top, and `agent.py::run_agent` always takes the first result. None of my criteria check that the selected item is what the user asked for. I'd add a criterion like "the top result's title contains the main item word (boots, jeans, jacket)" and score title matches higher than tag or description matches. I stopped because Milestone 5 allows one change, and I found this only when reading the run output.
2. **The MCP fallback is silent.** If `mcp_client.call_tool` fails, `agent.py::_search` calls `search_listings` directly, but the trace still says "via MCP". I'd add a trace note when the fallback runs. I left it because the fallback keeps the agent working, and MCP never failed in my runs.
3. **Criterion 3 checks titles, not ids.** `run_eval.py` doesn't print `outfit_input_id` or `fit_card_input_id`. I'd print them so the original id check can be scored.
4. **Criterion 4 is still too easy.** The 300-character limit is only in the prompt, not in a criterion. I'd revise criterion 4 to "5 of 5 cards mention the price and are under 300 characters." Also, the prompt is missing a space ("once each.Keep"). I left it so the code matches the after run.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [x] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [x] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [x] Run Log — Before, five criteria, five tries each
       [x] Real output pasted underneath, naming file and function
       [x] A verdict on every criterion
       [x] A diagnosis for every miss, naming a place AND a mechanism
       [x] Loop Trace, with the MCP call visible in it
       [x] All three failure modes triggered and handled
       [x] One improvement, with Run Log — After in the same format
       [x] What's Still Broken
       [x] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
