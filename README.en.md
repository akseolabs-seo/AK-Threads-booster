[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

# AK-Threads-Booster

An open-source Claude Code skill and AI writing assistant designed specifically for Threads creators. This Threads content creation skill analyzes your historical post data, applies social media psychology research and Threads algorithm insights to deliver personalized writing analysis, Brand Voice profiling, and draft assistance.

If you are looking for a ready-to-use Threads skill, an AI social media post generator that actually learns from your own data, or a content creation tool backed by real performance metrics, this is it. Not a template. Not a rule set. A consultant skill that helps you understand the Threads algorithm and turn your data into actionable Threads tips for sustained Threads growth. Works as a skill / plugin for Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, and Google Antigravity.

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
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | Core analysis (4-dimension) |
| **Codex** | `AGENTS.md` (root) | Core analysis (4-dimension) |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | Core analysis (4-dimension) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Core analysis (4-dimension) |
| **Google Antigravity** | `.agents/` directory + root `AGENTS.md` | Core analysis (4-dimension) |

### Feature Differences

- **Claude Code**: Full functionality including initialization (setup), Brand Voice profiling (voice), writing analysis (analyze), topic recommendations (topics), draft assistance (draft), viral post prediction (predict), and post-publish review (review) -- seven independent Skills
- **Other tools**: Core writing analysis with four dimensions (style matching, psychology analysis, algorithm alignment check, AI-tone detection), sharing the same knowledge base (`knowledge/` directory)
- **Google Antigravity**: Reads both root `AGENTS.md` (consultant norms and red-line rules) and `.agents/` directory (rules files + analysis skills)

All tool versions include:
- Consultant tone guidelines (no scoring, no corrections, no ghostwriting)
- Algorithm red-line rules (trigger warnings on match)
- Knowledge base references (psychology, algorithm, AI-tone detection)

---

## Installation

### Option 1: Install via GitHub

```bash
# In your Claude Code project directory
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

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

### Other Tools

If you use Cursor, Windsurf, Codex, or GitHub Copilot, simply clone the repo into your project directory. Each tool will automatically read its corresponding configuration file.

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

Initialization only needs to run once. Subsequent data updates accumulate through the `/review` module.

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

After writing a post, paste your content for four-dimension analysis:

```
/analyze

[paste your post content]
```

Four analysis dimensions:

- **Style matching**: Compares against your own historical style, flags deviations and historical performance
- **Psychology analysis**: Hook mechanisms, emotional arc, sharing motivation, trust signals, cognitive biases, comment trigger potential
- **Algorithm alignment**: Red-line scan (warnings on match) + positive signal assessment
- **AI-tone detection**: AI-trace scanning at sentence, structure, and content levels

### 4. /topics -- Topic Recommendations

When you do not know what to write next. Mines insights from comments and historical data to recommend topics.

```
/topics
```

Recommends 3-5 topics, each with: recommendation source, data-backed reasoning, similar historical post performance, estimated performance range.

### 5. /draft -- Draft Assistance

Selects a topic from your topic bank and generates a draft based on your Brand Voice. This is the most direct AI content creator function in AK-Threads-Booster, but the draft is only a starting point.

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

After publishing, use this to collect actual performance data, compare against predictions, and update system data.

```
/review
```

What it does:
- Collects actual performance data
- Compares against predictions and analyzes deviations
- Updates tracker and style guide
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
5. /analyze [post]     -- Analyze the draft or your own writing
6. (Edit based on analysis)
7. /predict [post]     -- Estimate performance before publishing
8. (Publish)
9. /review             -- Collect data 24h after publishing
10. Back to step 3
```

Each cycle makes the system's analysis and predictions more accurate. `/voice` only needs to run once (or re-run after accumulating more posts). `/draft` automatically references your Brand Voice file.

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
├── templates/
│   ├── tracker-template.json
│   ├── style-guide-template.md
│   └── concept-library-template.md
├── README.md
├── README.en.md
├── README.ja.md
├── README.ko.md
└── LICENSE
```

---

## License

MIT License. See [LICENSE](./LICENSE).
