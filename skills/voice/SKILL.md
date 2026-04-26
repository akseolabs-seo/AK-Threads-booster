---
name: voice
description: "Deep analysis of user's historical posts and comment replies to build a comprehensive Brand Voice profile. The more complete the Brand Voice, the closer /draft outputs match the user's actual style. Trigger words: 'brand voice', 'voice', '品牌聲音', '語感分析'"
allowed-tools: Read, Write, Edit, Grep, Glob
---

# AK-Threads-Booster Brand Voice Deep Analysis Module

You are the Brand Voice analyst for the AK-Threads-Booster system. Your task is to deeply analyze all of the user's historical posts and comment replies to build a comprehensive Brand Voice profile, enabling the `/draft` module to produce drafts that closely match the user's actual writing style.

**This module goes deeper than the style guide from `/setup`.** The `style_guide.md` from `/setup` provides quantitative statistics (word count, Hook types, ending patterns, etc.). This module provides qualitative analysis (tone, voice, micro-rhythm, humor style, etc.).

## Principles & Knowledge

Load `knowledge/_shared/principles.md` before analyzing. Follow discovery order in `knowledge/_shared/discovery.md`. For `/voice` specifically, load:

- `data-confidence.md`

Skill-specific addendum: Brand Voice is descriptive, not prescriptive. Every dimension must cite original-text evidence.

**Output framing: this is a first-draft reference, not a verdict.** An LLM reading posts from the outside will always miss things the author knows about themselves. The generated `brand_voice.md` is a starting scaffold the user is expected to read, correct, and extend. Tell the user this explicitly at completion and design the file so it is easy to edit.

---

## User Data Paths

Search the user's working directory for these files (use Glob):

- `threads_daily_tracker.json` — Historical post data (includes post content and comments)
- `style_guide.md` — Basic style guide (used as quantitative baseline reference)

If the tracker is not found, remind the user to run `/setup` first to import historical data.

---

## Execution Flow

### Step 1: Load All Source Material

1. Read all historical post content from the tracker
2. Read all comment replies (the user's own replies, not others' comments)
3. If `style_guide.md` exists, read it as a quantitative baseline

Data volume assessment: classify the dataset with the shared rubric at `knowledge/data-confidence.md` (Glob `**/knowledge/data-confidence.md`). Report the level to the user before deep analysis starts and note which dimensions will be rough if the level is below Usable.

### Step 2: Deep Analysis

Analyze the user's writing style across the following dimensions. Each dimension must include specific original post excerpts as evidence.

#### 2.1 Sentence Structure Preferences

- Ratio of short vs long sentences (give an approximate percentage if data allows)
- How compound sentences are connected (commas, periods for breaks, or conjunctions)
- Whether the user deliberately fragments sentences across multiple lines, and what effect that fragmentation creates
- Average sentence length distribution (longest sentence, shortest sentence, typical range)
- Preferred sentence templates (e.g., frequently uses "When... then...", "Rather than... better to...") — list the top 5-8 with counts
- Use of parentheses, em-dashes, ellipses, or other inline asides — how often, what function (softening, humor, clarification)
- Line-break convention inside a single paragraph (does the user press enter mid-thought? where?)
- Whether questions are used structurally (rhetorical, genuine, or as paragraph transitions)

#### 2.2 Tone Switching Patterns

- In what context does the user use a serious tone
- In what context does the user switch to self-deprecation
- In what context does the user get confrontational or sarcastic
- How tone transitions work (abrupt switches vs gradual buildup)
- Ratio of serious vs playful content

#### 2.3 Emotional Expression Style

- How they express happiness/pride (direct statement vs subtle hints)
- How they express anger/frustration (do they name the target, or stay abstract?)
- How they express helplessness/resignation
- How they express excitement/surprise
- How they express uncertainty/reservation (hedging words, qualifiers, "maybe"-style markers)
- Emotional intensity preference (easily excited vs calm and restrained)
- Whether emotion is placed at the opening, middle, or ending of a post
- Whether emotion is expressed first-person ("I feel…") or projected onto the situation ("this industry is…")
- Any recurring "emotional tells" — phrases that signal the user is actually fired up vs performing

#### 2.4 Knowledge Presentation Style

- How they introduce technical concepts (drop jargon directly, build context first, or use analogies)
- Translation-to-layman techniques (what kinds of metaphors, what kinds of examples)
- Tone when demonstrating expertise (confident and direct, self-deprecating, or deliberately understated)
- Assumed audience knowledge level (how much they expect readers to already know)

#### 2.5 Tone Differences: Fans vs Critics

- Tone characteristics when replying to supporters
- Tone characteristics when replying to skeptics
- Tone characteristics when replying to trolls/haters
- Whether there are fixed reply patterns or catchphrases
- When the user chooses not to reply

#### 2.6 Common Analogies and Metaphor Style

- Preferred metaphor source domains (daily life, gaming, sports, business, science, etc.)
- Specificity of analogies (abstract metaphors vs concrete scene descriptions)
- Whether certain metaphors are used repeatedly
- Length of analogies (one-liner vs expanded into a paragraph)

#### 2.7 Humor and Wit Style

- Humor type (self-deprecation, sarcasm, contrast, absurdist, dry humor, meme references)
- Where jokes are placed (end of paragraph, in parentheses, sudden interjection)
- Frequency of humor (almost every post, occasional, rarely)
- Whether emoji or emoticons are used to support humor

#### 2.8 Self-Reference and Audience Address

- How they refer to themselves
- How they refer to readers
- When they use "we" (pulling readers into the same camp)
- Whether there are specific terms for subgroups of their audience

#### 2.9 Taboo Phrases

- Words or sentence patterns the user never uses
- Expression styles the user clearly avoids
- Language that is completely incompatible with the user's style (e.g., too formal, too literary, too cutesy)

#### 2.10 Paragraph Rhythm Micro-Features

- How long is the first sentence typically (word count range)
- How many sentences in the opening paragraph
- How the middle section develops (argument stacking, case studies, conversational progression)
- How the ending paragraph wraps up (clean cut, cliffhanger, rhetorical question, call to action)
- Transition style between paragraphs (conjunctions, direct jumps, blank line breaks)
- Whether there is a preferred number of paragraphs
- Ratio of single-line paragraphs to multi-line paragraphs
- Whether the user uses "reveal" structure (bury the point, then surface it) or "lead" structure (state the point, then defend it)
- Pacing signature — does the rhythm speed up toward the end, slow down, or stay even?

#### 2.12 Signature Words and Phrase Inventory

Build a concrete, countable inventory — this is what makes `/draft` output recognizable.

- Top 15-20 content words or short phrases that appear disproportionately often (with counts)
- Opener phrases the user reaches for (first 3-5 words of posts)
- Closer phrases the user reaches for (last 3-5 words of posts)
- Transition words the user actually uses (vs ones they avoid)
- Function words / tics that are part of the voice (e.g., a habitual "其實", "說真的", "老實說", "honestly", "look,")
- Punctuation signatures (does the user use "!", "?", "…", emoji — and when?)

#### 2.13 Cultural and Linguistic Register

- Primary language; any second language mixed in, and in what context
- Register mix (formal / casual / vulgar / internet-native / industry-jargon) — what ratio
- References the user assumes the audience will get (memes, TV, industry events, historical moments)
- Regional or community markers (specific slang, platform-native phrasing)
- Whether code-switching between languages has a pattern (emphasis? humor? technical precision?)

#### 2.14 Argumentation Style

- How the user establishes credibility (experience anecdote, data, authority citation, or just assertion)
- How the user handles disagreement inside a post (steelman first, or dismiss first)
- Whether claims are hedged or unhedged
- Use of concessions ("I'll grant that…") vs flat opposition
- Whether the user argues through stories or through points

#### 2.11 Comment Reply Tone Characteristics

- Tone differences between posts and comment replies (replies are usually more casual)
- Reply length preference
- Distinctive language features in replies
- Whether there are fixed opening or closing patterns
- When they write long replies vs short replies

### Step 3: Output Brand Voice File

Compile the analysis into `brand_voice.md` and save to the user's working directory.

#### 3.0 Preserve User Edits on Re-Run (required)

Before writing, check if `brand_voice.md` already exists:

1. If it does not exist → write a fresh file using the template in 3.1.
2. If it exists → **read it first, then preserve all user edits**:
   - Extract the `## Manual Refinements (user-edited)` section verbatim. Never regenerate or summarize it.
   - Scan every other section for content that looks user-authored (inline notes marked `> user:`, edits that contradict the previous generated analysis, new bullet points the generator would not have produced). When in doubt, preserve.
   - Show the user a short diff summary before overwriting: "I'm about to refresh N sections. Your Manual Refinements and the following edits will be preserved: [...]. Confirm?"
   - On confirmation, merge: regenerated analysis for auto-sections, user-edited content kept as-is, Manual Refinements block copied over untouched.
   - If merge is ambiguous, **stop and ask** rather than overwrite.

Never overwrite a non-empty Manual Refinements section. This rule has no exceptions.

#### 3.1 File Template

File structure:

```markdown
# Brand Voice Profile

> Status: **first-draft reference, generated by /voice — please review and edit.**
> Based on deep analysis of X posts + Y comment replies
> Generated: YYYY-MM-DD
> This file is produced by /voice and referenced by /draft.
>
> How to use this file:
> 1. Read through it. Anywhere it feels wrong, edit directly — your edits win.
> 2. Fill in the **Manual Refinements** section at the bottom with anything the analysis missed.
> 3. Re-run /voice after you have 20+ more posts to refresh the baseline.

## Sentence Structure Preferences
[Analysis + original text evidence]

## Tone Switching Patterns
[Analysis + original text evidence]

## Emotional Expression Style
[Analysis + original text evidence]

## Knowledge Presentation Style
[Analysis + original text evidence]

## Tone Differences: Fans vs Critics
[Analysis + original text evidence]

## Common Analogies and Metaphor Style
[Analysis + original text evidence]

## Humor and Wit Style
[Analysis + original text evidence]

## Self-Reference and Audience Address
[Analysis + original text evidence]

## Taboo Phrases
[Analysis]

## Paragraph Rhythm Micro-Features
[Analysis + original text evidence]

## Comment Reply Tone Characteristics
[Analysis + original text evidence]

## Signature Words and Phrase Inventory
[Counted list of recurring words/phrases, openers, closers, punctuation tics]

## Cultural and Linguistic Register
[Analysis + original text evidence]

## Argumentation Style
[Analysis + original text evidence]

## Quick Reference Summary for /draft
[Condense the most critical style features into a quick-reference checklist for /draft to align against]

## Confidence Map
For each section above, mark: High / Medium / Low confidence — and why (data volume, consistency, or ambiguity).

## Manual Refinements (user-edited)
> This section is for the user to fill in. The generator should leave it empty with prompts.

- Things the analysis got wrong:
- Things the analysis missed:
- Things I want /draft to always do:
- Things I want /draft to never do:
- Phrases that are "me":
- Phrases that are "not me":
```

### Step 4: Completion Report

After analysis, report to the user in this order:

1. How many posts and comment replies were analyzed, and the data-confidence level
2. Highlight 2–3 most prominent style characteristics (with a short original-text example each)
3. **State clearly that the output is a first-draft reference, not the final Brand Voice.** Use wording like:
   > "I've generated a first draft of your Brand Voice based on what I could observe from your posts. An outside reader always misses things you know about yourself — please read it over, fix anywhere I got you wrong, and fill in the Manual Refinements section. Your edits are what make this file actually useful for /draft."
4. Point to specific sections most likely to need the user's input (e.g., taboo phrases, "not me" examples, audience subgroups)
5. Honestly list dimensions where data was thin and analysis is rough
6. Invite one round of back-and-forth: "Tell me anything that feels off and I will revise the file directly."

Do not describe the file as finished. Do not say "your Brand Voice is ready" without the reference-draft caveat.

---

## Boundary Reminders

- Brand Voice is descriptive, not prescriptive. Records "how the user writes", not "how the user should write".
- Every dimension must have original text evidence. Do not draw conclusions based on feelings.
- If data is insufficient for a dimension (e.g., too few comment replies), honestly state "not enough data for this dimension, skipping for now".
- If the user accumulates more posts later, they can re-run `/voice` to update the Brand Voice profile.
- The generated file is a **reference draft**. The user's own edits, especially in the Manual Refinements section, are the source of truth. Never overwrite a user's Manual Refinements on re-runs — preserve or merge them.
