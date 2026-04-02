[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

<div align="center">

<img src="./assets/readme-banner.svg" alt="AK Threads Booster banner" width="100%">

# AK-Threads-Booster

### Turn Threads writing from guesswork into a system backed by your own data

A data-backed AI Skill system for Threads creators.  
Not a generic template. Not a ghostwriter. A decision layer that reads your historical posts, helps you judge new posts, and writes the results back into your tracker over time.

<p>
  <a href="./LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/license-MIT-6ee7b7?style=for-the-badge&logo=open-source-initiative&logoColor=0b0f19"></a>
  <img alt="Status Alpha" src="https://img.shields.io/badge/status-alpha-f59e0b?style=for-the-badge&logo=target&logoColor=0b0f19">
  <img alt="Seven Skills" src="https://img.shields.io/badge/modules-7%20skills-60a5fa?style=for-the-badge&logo=buffer&logoColor=0b0f19">
  <img alt="Snapshot Ready" src="https://img.shields.io/badge/tracker-snapshot--ready-a78bfa?style=for-the-badge&logo=databricks&logoColor=0b0f19">
  <a href="https://www.threads.com/@darkseoking"><img alt="Follow on Threads" src="https://img.shields.io/badge/Threads-@darkseoking-111827?style=for-the-badge&logo=threads&logoColor=white"></a>
</p>

<p>
  <a href="#quick-start">Quick Start</a> •
  <a href="#installation">Installation</a> •
  <a href="#initialization">Initialization</a> •
  <a href="#data-update-modes">Data Update Modes</a> •
  <a href="#the-seven-skills">Seven Skills</a> •
  <a href="#directory-structure">Directory</a> •
  <a href="#typical-workflow">Workflow</a> •
  <a href="#license">License</a>
</p>

</div>

AK-Threads-Booster is an open-source Claude Code and Codex skill system designed specifically for Threads creators. It turns your own post history into a working decision layer for topic selection, draft support, post analysis, performance prediction, and post-publish feedback.

It already supports:

- importing historical posts into a tracker
- decision-first analysis for finished posts
- prediction ranges based on account history
- post-publish checkpoint review
- API-backed `snapshots[]` updates through `scripts/update_snapshots.py`

If you are looking for a Threads skill that actually learns from your own data instead of recycling generic social media advice, this is it.

---

## What Is AK-Threads-Booster

AK-Threads-Booster is an open-source Threads skill -- not a writing template, a rule set, or an AI content creator that replaces you.

It is a methodology system that does three things:

1. **Analyzes your historical data** to identify what content drives the most Threads engagement on your account
2. **Uses psychology and Threads algorithm knowledge as analytical lenses** to explain why certain posts perform well
3. **Presents the findings transparently** so you can decide your next move

Every user gets different results because every account has a different audience, style, and dataset. That is the core difference between a data-driven Threads strategy and generic social media advice.

---

## Core Principles

**A consultant, not a teacher.** AK-Threads-Booster will not tell you "you should write this way." It will say "when you did this before, the data looked like this -- for your reference." No scoring, no corrections, no ghostwriting.

**Data-driven, not rule-driven.** All suggestions come from your own historical data, not a generic "Top 10 Social Media Marketing Tips" list. When data is insufficient, the system tells you honestly instead of pretending confidence.

**Red lines are the only hard rules.** Only behaviors that Meta's algorithm explicitly penalizes (engagement bait, clickbait, high-similarity reposts, etc.) trigger direct warnings. Everything else is advisory. You always have the final say.

---

## Multi-Tool Support

AK-Threads-Booster works with multiple AI coding tools. Claude Code provides the full 7-Skill experience; other tools offer core analysis capabilities.

### Supported Tools and Configuration Files

| Tool | Config Location | Scope |
|------|----------------|-------|
| **Claude Code** | `skills/` directory (7 Skills) | Full features: setup, voice, analyze, topics, draft, predict, review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | Core analysis (decision-first analyze) |
| **Codex** | `AGENTS.md` (root) | Core analysis (decision-first analyze) |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | Core analysis (decision-first analyze) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Core analysis (decision-first analyze) |
| **Google Antigravity** | `.agents/` directory + root `AGENTS.md` | Core analysis (decision-first analyze) |

### Feature Differences

- **Claude Code**: Full functionality including initialization (setup), Brand Voice profiling (voice), writing analysis (analyze), topic recommendations (topics), draft assistance (draft), viral post prediction (predict), and post-publish review (review) -- seven independent Skills
- **Other tools**: Core writing analysis including decision-first judgment, red-line checks, style matching, psychology analysis, algorithm alignment, and AI-tone detection, sharing the same knowledge base (`knowledge/` directory)
- **Google Antigravity**: Reads both root `AGENTS.md` (consultant norms and red-line rules) and `.agents/` directory (rules files + analysis skills)

All tool versions include:
- Consultant tone guidelines (no scoring, no corrections, no ghostwriting)
- Algorithm red-line rules (trigger warnings on match)
- Knowledge base references (psychology, algorithm, AI-tone detection)

---

## Quick Start

If you want the shortest path to a working setup, use this order:

1. Install the repo into your AI tool environment
2. Run `/setup` to import your historical posts
3. Run `scripts/update_topic_freshness.py` to build semantic clusters and topic freshness
4. After writing a post, run `/analyze`
5. Before publishing, run `/predict` if you want a 24-hour range
6. After publishing, use `/review` to collect 24h / 72h checkpoints
7. If you have a Threads API token, add `scripts/update_snapshots.py` for automatic snapshots

Minimum workflow:

```text
/setup -> update_topic_freshness.py -> /analyze -> /predict -> publish -> /review
```

Advanced workflow (with API):

```text
/setup -> update_topic_freshness.py -> /analyze -> /predict -> publish -> update_snapshots.py -> /review
```

---

## Installation

### Option 1: Install via GitHub

```bash
# In your Claude Code project directory
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

After installation, the repo exposes a single top-level Skill entry named `ak-threads-booster`. That entry routes internally to `setup`, `analyze`, `draft`, `predict`, `review`, `topics`, or `voice` based on user intent.

### Option 2: Manual Installation

1. Clone this repo locally:
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. Copy the `AK-Threads-booster` directory into your Claude Code project's `.claude/plugins/`:
   ```bash
   cp -r AK-Threads-booster /path/to/your/project/.claude/plugins/
   ```

3. Restart Claude Code. The Skills will be detected automatically.

The detected top-level Skill name is `ak-threads-booster`.

### Other Tools

If you use Cursor, Windsurf, Codex, or GitHub Copilot, simply clone the repo into your project directory. Each tool will automatically read its corresponding configuration file.

For Skill-based installers, the intended single entry point is the root [SKILL.md](./SKILL.md), which exposes `ak-threads-booster`.

---

## Initialization

Before first use, run the initialization to import your historical data:

```
/setup
```

The initialization guides you through:

1. **Choose a data import method**
   - Meta Threads API (automatic fetch)
   - Meta account export (manual download)
   - Provide existing data files directly

2. **Automatic historical post analysis**, generating three files:
   - `threads_daily_tracker.json` -- Historical post database
   - `style_guide.md` -- Personalized style guide (your Hook preferences, word count ranges, ending patterns, etc.)
   - `concept_library.md` -- Concept library (tracks concepts you have already explained to your audience)

3. **Analysis report** showing your account's style characteristics and data overview

Initialization only needs to run once. Subsequent data updates accumulate through the `/review` module; if you have API access, you can also keep filling snapshots through `scripts/update_snapshots.py`. If you want tracker-backed topic fatigue and semantic-cluster freshness, run `scripts/update_topic_freshness.py` as well.

---

## Data Update Modes

AK-Threads-Booster now has two practical data update paths:

### Path A: Checkpoint Mode (available to everyone)

If you only have export data and no API access:

- `/setup` builds the initial tracker
- after publishing, `/review` collects 24h / 72h / 7d checkpoints
- the system uses those checkpoints to calibrate future predictions

This path does not preserve a growth curve, but it is reliable and low-maintenance.

### Path B: Snapshot Mode (requires Threads API)

If you have a Threads API token:

- `scripts/fetch_threads.py` imports posts and base metrics
- `scripts/update_snapshots.py` refreshes metrics on a schedule
- the tracker keeps accumulating `snapshots[]`
- the script writes the nearest 24h / 72h / 7d values into `performance_windows`

Most common snapshot update command:

```bash
python scripts/update_snapshots.py --token YOUR_TOKEN --tracker ./threads_daily_tracker.json --recent 10
```

Single post refresh:

```bash
python scripts/update_snapshots.py --token YOUR_TOKEN --tracker ./threads_daily_tracker.json --post-id POST_ID
```

This means the project is no longer limited to final result tables; it can now preserve growth checkpoints for individual posts.

---

### Topic Freshness Updates (available to everyone)

If you want the system to estimate whether a topic has already been overused from your account-history perspective, run:

```bash
python scripts/update_topic_freshness.py --tracker ./threads_daily_tracker.json
```

It will:

- build lightweight semantic clusters
- write `semantic_cluster` back into the tracker
- estimate `freshness_score / fatigue_risk`

This flow does not require the Threads API. A tracker file is enough.

---

## The Seven Skills

### 1. /setup -- Initialization

Run on first use. Imports historical posts, generates your style guide, and builds the concept library.

```
/setup
```

### 2. /voice -- Brand Voice Profiling

Deep analysis of all historical posts and comment replies to build a comprehensive Brand Voice profile. Goes deeper than the style guide from `/setup`, covering sentence structure preferences, tone shifts, emotional expression, humor style, taboo phrases, and more.

```
/voice
```

The more complete your Brand Voice, the closer `/draft` outputs match your actual writing style. Recommended after `/setup`.

Analysis dimensions include: sentence structure preferences, tone transition patterns, emotional expression style, knowledge presentation, tone differences between fans and critics, common analogies and metaphors, humor and wit style, self-reference and audience address, taboo phrases, paragraph rhythm micro-features, comment reply tone characteristics.

Output: `brand_voice.md`, automatically referenced by the `/draft` module.

### 3. /analyze -- Writing Analysis (Core Feature)

After writing a post, paste your content for decision-first analysis:

```
/analyze

[paste your post content]
```

The current output order is:

- **Algorithm Red Lines**: catches likely downranking triggers first
- **Decision Summary**: shows the biggest upside and biggest friction immediately
- **Highest-Upside Comparisons**: compares against your historical high-performing patterns
- **Suppression Risks**: flags what may limit distribution even if the post is not bad
- **Style / Psychology / Algorithm / AI-Tone**: then expands into the full analysis

If you only have a tracker and do not yet have a complete `style_guide.md`, `/analyze` can fall back to tracker-only mode instead of failing.

### 4. /topics -- Topic Recommendations

When you do not know what to write next. Mines insights from comments and historical data to recommend topics.

```
/topics
```

Recommends 3-5 topics, each with: recommendation source, data-backed reasoning, similar historical post performance, estimated performance range.

### 5. /draft -- Draft Assistance

Selects a topic from your topic bank and generates a draft based on your Brand Voice. Includes online fact-checking and source material research before drafting to ensure content accuracy. This is the most direct AI content creator function in AK-Threads-Booster, but the draft is only a starting point.

```
/draft [topic]
```

You can specify a topic or let the system recommend one from your topic bank. Draft quality depends on how complete your Brand Voice data is -- running `/voice` first makes a noticeable difference.

The draft is a starting point. You need to edit and adjust it yourself. After editing, running `/analyze` is recommended.

### 6. /predict -- Viral Post Prediction

After writing a post, estimate its performance 24 hours after publishing.

```
/predict

[paste your post content]
```

Outputs conservative/baseline/optimistic estimates (views / likes / replies / reposts / shares) with supporting rationale and uncertainty factors.

### 7. /review -- Post-Publish Review

After publishing, use this to collect actual performance data, compare against predictions, and update system data. If available, it also uses `snapshots[]` and `performance_windows`.

```
/review
```

What it does:
- Collects actual performance data
- Compares against predictions and analyzes deviations
- Updates tracker and style guide
- Consumes `snapshots[]` and `performance_windows` when present
- Suggests optimal posting times

---

## Knowledge Base

AK-Threads-Booster includes three built-in knowledge bases that serve as analytical reference points:

### Social Media Psychology (psychology.md)

Source: Academic research compilation. Covers Hook psychological trigger mechanisms, comment trigger psychology, sharing motivation and virality (STEPPS framework), trust building (Pratfall Effect, Parasocial Relationship), cognitive bias applications (Anchoring, Loss Aversion, Social Proof, IKEA Effect), emotional arc and arousal levels.

Purpose: Theoretical foundation for the psychology analysis dimension in `/analyze`. Psychology is an analytical lens, not a writing rule.

### Meta Algorithm (algorithm.md)

Source: Meta patent documents, Facebook Papers, official policy statements, KOL observations (supplementary only). Covers red-line list (12 penalized behaviors), ranking signals (DM sharing, deep comments, dwell time, etc.), post-publish strategy, account-level strategy.

Purpose: Rule foundation for the algorithm alignment check in `/analyze`. Red-line items trigger warnings; signal items are presented in advisory tone.

### AI-Tone Detection (ai-detection.md)

Covers sentence-level AI traces (10 types), structure-level AI traces (5 types), content-level AI traces (5 types), AI-tone reduction methods (7 types), scan trigger conditions, and severity definitions.

Purpose: Detection baseline for AI-tone scanning in `/analyze`. Flags AI traces for you to fix yourself; does not auto-correct.

---

## Typical Workflow

```
1. /setup              -- First use, initialize the system
2. /voice              -- Deep Brand Voice profiling (run once)
3. /topics             -- Browse topic recommendations
4. /draft [topic]      -- Generate a draft
5. /analyze [post]     -- Analyze the draft or your own writing with a decision-first flow
6. (Edit based on analysis)
7. /predict [post]     -- Estimate performance before publishing
8. (Publish)
9. update_snapshots.py      -- If you have API access, add snapshot / checkpoint updates
10. update_topic_freshness.py -- Refresh semantic clusters / topic freshness
11. /review                -- Collect data after publishing
12. Back to step 3
```

If you do not have API access, you can skip `update_snapshots.py` and rely on `/review` checkpoints plus `update_topic_freshness.py`. Each cycle makes the system's analysis and predictions more accurate. `/voice` only needs to run once (or re-run after accumulating more posts). `/draft` automatically references your Brand Voice file.

---

## FAQ

**Q: Will AK-Threads-Booster write posts for me?**
The `/draft` module generates initial drafts, but drafts are only a starting point. You need to edit and refine them yourself. Draft quality depends on how complete your Brand Voice data is. Other modules only analyze and advise -- they do not ghostwrite.

**Q: Is the analysis accurate with limited data?**
Not very. The system will tell you honestly. Accuracy improves as data accumulates.

**Q: Do I have to follow the suggestions?**
No. All suggestions are advisory only. You always have the final say. The only direct warnings are for algorithm red lines (writing patterns that trigger demotion).

**Q: Does it support platforms other than Threads?**
Currently designed primarily for Threads. The psychology principles in the knowledge base are universal, but the algorithm knowledge base focuses on Meta's platform.

**Q: How is this different from a typical AI writing assistant?**
Generic tools produce content from general models. AK-Threads-Booster's analysis and suggestions all come from your own historical data, so every user gets different results. It is a consultant, not a ghostwriter. That is the key to building a Threads strategy that actually fits your audience.

**Q: Will this guarantee my posts go viral?**
No. The Threads algorithm is an extremely complex system, and no tool can guarantee viral posts. What AK-Threads-Booster does is help you make better decisions based on your own historical data, avoid known algorithm red lines, and improve the probability of each post performing well through psychology and data-driven analysis. It is currently the most comprehensive Threads content creation skill available, but the factors that determine whether a post goes viral -- timing, topic relevance, audience state, the algorithm's distribution logic at that moment -- are too numerous for any tool to fully control. Treat it as your data consultant, not a viral guarantee machine.

---

## Directory Structure

```
AK-Threads-booster/
├── .agents/
│   ├── rules/
│   │   └── ak-threads-booster.md
│   └── skills/
│       └── analyze/
│           └── SKILL.md
├── .claude-plugin/
│   └── plugin.json
├── .cursor/
│   └── rules/
│       └── ak-threads-booster.mdc
├── .windsurf/
│   └── rules/
│       └── ak-threads-booster.md
├── .github/
│   └── copilot-instructions.md
├── AGENTS.md
├── SKILL.md
├── assets/
│   └── readme-banner.svg
├── skills/
│   ├── setup/SKILL.md
│   ├── voice/SKILL.md
│   ├── analyze/SKILL.md
│   ├── topics/SKILL.md
│   ├── draft/SKILL.md
│   ├── predict/SKILL.md
│   └── review/SKILL.md
├── knowledge/
│   ├── psychology.md
│   ├── algorithm.md
│   └── ai-detection.md
├── scripts/
│   ├── fetch_threads.py
│   ├── parse_export.py
│   ├── update_snapshots.py
│   ├── update_topic_freshness.py
│   └── requirements.txt
├── templates/
│   ├── tracker-template.json
│   ├── style-guide-template.md
│   └── concept-library-template.md
├── examples/
│   ├── tracker-example.json
│   ├── style-guide-example.md
│   └── brand-voice-example.md
├── README.md
├── README.en.md
├── README.ja.md
├── README.ko.md
└── LICENSE
```

---

## License

MIT License. See [LICENSE](./LICENSE).
