# AI-Detection Scan: AICE Media Studies Blog

> **AI signature:** This report and every script in this folder were produced by Claude (Anthropic), an AI model.
> It is a risk estimate, not proof either way. Scan date: 2026-11-12. Scope: all 29 published posts (about 21,600 words, 54 images, 0 links).

## Verdict

**Text: low risk.** Nothing in the 29 posts reads as AI-written. **Images: three items worth fixing**, listed below.

## How the scan was done

1. **Full manual read** of every post, looking for the patterns human reviewers and Turnitin/GPTZero-type tools key on.
2. **Perplexity and burstiness** (GPT-2). Perplexity measures how predictable the wording is; AI text is very predictable (low score). This is the core idea behind GPTZero-style detectors.
3. **Open AI-text classifiers** (three RoBERTa models, run per paragraph). Only one (Fakespot) separated a known-AI sample from the posts, so it is the only one reported in the table. The other two scored the known-AI sample as human and were discarded as unreliable.
4. **Stylometry**: counts of em dashes, AI-favoured vocabulary ("crucial", "seamlessly", "furthermore", "not just X but Y"), versus human markers (typos, slips, informal words).
5. **Calibration**: a deliberately AI-written sample on the same topics (`calibration/ai_baseline.txt`) was scored with the same tools for comparison.
6. **Images**: every image viewed directly, plus a metadata scan for AI-generator tags and C2PA content credentials (none found, but the blog host strips most metadata, so this is weak evidence).

**Limits:** Turnitin and GPTZero themselves could not be run (paid, account-gated). The open models used here are weaker and noisier than those. Treat the numbers as indicators.

## Text results

| Measure | Blog posts | Known-AI sample |
|---|---|---|
| Perplexity | 29 to 70 (median about 52) | 24 |
| Sentence-length variation (SD) | 4.7 to 13.1 | 3.2 |
| AI-vocabulary per 1,000 words | 0 in 20 posts, max 6.1 | 37.6 |
| Em dashes | 0 across all posts | 2 in 479 words |
| Classifier AI score | 3% to 83% | 100% |

Why the text reads as human:

- **Frequent genuine errors** that AI does not produce: "protagnist", "whire", "masthand", "its'", "before before", "where are eyes", "rule of two-thirds", "look game", "convent is revealed", dropped words ("people who to build"), and the odd "i. e." spacing.
- **Specific personal detail**: the eSports club survey of 23 people, the verbatim interview quote about OCs, the peer-review specifics.
- **No AI signature habits**: no em dashes, almost no AI vocabulary, no "not just X, but Y" constructions, no tidy summarising closers.
- **Consistent voice across three months**, including the same quirks ("whilst", "straight-to-the-point", "visual flare") from post 1 to post 29. A sudden style change is what teachers notice first, and there is none.

Where a detector could still fire (false positives):

- The classifier scored 43 of 204 paragraphs above 90%. These are mostly **formulaic paragraphs that answer the teacher's prompts in order** ("This appeals to my audience because...", "This research helped me by..."). Template-driven school writing is a known cause of false positives. Only 11 of those 43 also had low perplexity, and none matched the AI sample on vocabulary or punctuation.
- Most exposed posts: **#10** (six camera-shot paragraphs with identical structure), **#26 and #29** (definition lists), **#2** and **#4**. Posts **#1 and #2** have the lowest perplexity (29), but they are short, simple and personal.
- Posts #27 and #28 use "tried-and-true", "battle-tested" and "vibrant" several times. Minor, but it is the closest thing to chatbot phrasing in the blog.

## Image results

| Priority | Post | Item | Issue |
|---|---|---|---|
| **High** | #29 | `DPS_1.png`, `DPS_2.png` | These flat-plan diagrams use the DejaVu Sans font and numbered-circle style typical of code-generated charts (the default look of diagrams produced by ChatGPT/Claude). The post also calls them "DPS #1/#2", as if they were real spreads. If the teacher supplied them, say so in the post. If they came from an AI tool, replace them with real or hand-drawn flat plans. |
| Medium | #9 | Mood board | The two workstation stock photos have the glossy look of AI-generated stock, and one still shows a "dreamstime" watermark. Swap for your own photos or credited stock. |
| Medium | #12 | "ROGUE NA Fashion Magazine" | This is a Canva template, not a published magazine, and the model photo may be synthetic. It is analysed as if it were real. Replace it with a real cover (Vogue, Elle) or state that it is a template. |
| Low | #6 | Animal Farm illustration | Looks like a human editorial illustration, but it is uncredited. Add the source. |
| Low | #1 | Avatar | Stock Canva-style illustration. Fine, no action needed. |
| None | #11, #14 to #25 | Your photos, sketches, renders and GUMERE covers | Clearly original: handwriting, real code editor, low-poly renders with visible texture pixels. Strong evidence of your own work. |

## Other observations

- **No post contains a single link or citation.** Sourcing images and the inStreamly statistic (#7) would help more than any wording change.
- Edit history is healthy: posts were published every few days with small same-week edits, which matches normal drafting.

## Recommendations

1. Fix the post #29 diagrams first. This is the only item that could reasonably be read as AI-generated content.
2. Add sources under borrowed images (posts #3, #4, #6, #9, #10, #12, #13, #18, #21, #27).
3. Do not rewrite the text to "sound less AI". It does not sound AI, and heavy rewriting is more likely to cause problems than prevent them.
4. Keep your evidence: Canva version history, original phone photos, paper sketches, 3D project files and the Edublogs revision history. If a detector ever flags a post, drafts are what settle it. Detector scores alone are not accepted as proof by Cambridge.

## Per-post numbers

| Post | Words | Perplexity (higher = more human) | Classifier AI score | Paragraphs scored >90% AI | AI-vocab per 1k words | Em dashes |
|---|---|---|---|---|---|---|
| 01 | 107 | 30 | 83% | 0/1 | 0.0 | 0 |
| 02 | 314 | 29 | 67% | 0/3 | 0.0 | 0 |
| 03 | 308 | 47 | 18% | 0/3 | 0.0 | 0 |
| 04 | 419 | 70 | 80% | 2/5 | 2.4 | 0 |
| 05 | 431 | 53 | 52% | 2/5 | 0.0 | 0 |
| 06 | 624 | 43 | 59% | 2/6 | 0.0 | 0 |
| 07 | 777 | 40 | 42% | 2/10 | 0.0 | 0 |
| 08 | 419 | 53 | 82% | 2/5 | 0.0 | 0 |
| 09 | 451 | 55 | 32% | 0/5 | 0.0 | 0 |
| 10 | 931 | 54 | 77% | 7/9 | 1.1 | 0 |
| 11 | 848 | 53 | 60% | 4/11 | 0.0 | 0 |
| 12 | 1769 | 68 | 55% | 3/16 | 0.0 | 0 |
| 13 | 773 | 50 | 18% | 0/6 | 0.0 | 0 |
| 14 | 417 | 59 | 3% | 0/3 | 0.0 | 0 |
| 15 | 545 | 48 | 45% | 2/6 | 0.0 | 0 |
| 16 | 735 | 44 | 30% | 0/5 | 0.0 | 0 |
| 17 | 764 | 48 | 60% | 2/5 | 0.0 | 0 |
| 18 | 1148 | 54 | 17% | 0/13 | 1.7 | 0 |
| 19 | 1944 | 48 | 46% | 1/17 | 1.0 | 0 |
| 20 | 848 | 49 | 33% | 1/7 | 0.0 | 0 |
| 21 | 507 | 54 | 32% | 0/5 | 0.0 | 0 |
| 22 | 701 | 43 | 43% | 0/5 | 0.0 | 0 |
| 23 | 864 | 46 | 41% | 2/6 | 2.3 | 0 |
| 24 | 1023 | 59 | 45% | 2/10 | 1.0 | 0 |
| 25 | 634 | 55 | 58% | 1/5 | 0.0 | 0 |
| 26 | 745 | 42 | 65% | 2/5 | 0.0 | 0 |
| 27 | 693 | 57 | 25% | 0/7 | 1.4 | 0 |
| 28 | 820 | 58 | 65% | 3/8 | 6.1 | 0 |
| 29 | 1489 | 60 | 58% | 3/12 | 0.0 | 0 |
| AI_BASELINE | 479 | 24 | 100% | 5/5 | 37.6 | 2 |

## Files

- `posts/` plain text of each post, `data/` raw API data and scan outputs
- `extract.py`, `fetch_images.py`, `image_meta.py`, `text_scan.py` the scripts used
- Images are downloaded locally by `fetch_images.py` but not committed (third-party copyrighted covers)
