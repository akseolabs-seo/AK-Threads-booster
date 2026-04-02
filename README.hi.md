[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

<div align="center">

<img src="./assets/readme-banner.svg" alt="AK Threads Booster banner" width="100%">

<p>
  <a href="./LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/license-MIT-6ee7b7?style=for-the-badge&logo=open-source-initiative&logoColor=0b0f19"></a>
  <img alt="Status Alpha" src="https://img.shields.io/badge/status-alpha-f59e0b?style=for-the-badge&logo=target&logoColor=0b0f19">
  <img alt="Seven Skills" src="https://img.shields.io/badge/modules-7%20skills-60a5fa?style=for-the-badge&logo=buffer&logoColor=0b0f19">
  <img alt="Snapshot Ready" src="https://img.shields.io/badge/tracker-snapshot--ready-a78bfa?style=for-the-badge&logo=databricks&logoColor=0b0f19">
  <a href="https://www.threads.com/@darkseoking"><img alt="Follow on Threads" src="https://img.shields.io/badge/Threads-@darkseoking-111827?style=for-the-badge&logo=threads&logoColor=white"></a>
</p>

</div>


# AK-Threads-Booster

> **Current Version**
> - decision-first `/analyze` flow
> - tracker-only fallback when full setup files are missing
> - checkpoint review for all users
> - API-backed `snapshots[]` and `performance_windows` via `scripts/update_snapshots.py`

Threads creators ke liye ek open-source Claude Code skill aur AI writing assistant. Ye tool aapke historical post data ko analyze karta hai, social media psychology research aur Threads algorithm ki insights use karke personalized writing analysis, Brand Voice profiling, aur draft assistance deta hai.

Agar aap ek aisi AI content creation tool dhundh rahe ho jo actually aapke apne data se seekhe, ya phir Threads followers kaise badhaye iska data-backed jawab chahte ho, to ye project aapke liye hai. Ye koi template nahi hai. Koi rule set nahi hai. Ye ek consultant skill hai jo aapko Threads algorithm samajhne mein help karta hai aur aapke data ko actionable Threads tips mein convert karta hai. Works as a skill / plugin for Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, aur Google Antigravity.

**Completely free aur open-source** -- koi subscription nahi, koi hidden charges nahi. Saara data aapki local machine pe rehta hai.


## त्वरित शुरुआत

1. Repo ko apne AI tool me jodien.
2. `/setup` chala kar historical posts import karein.
3. Post likhne ke baad `/analyze` use karein; publish se pehle zarurat ho to `/predict`.
4. Post ke baad `/review` se 24h aur 72h checkpoints collect karein.
5. Agar Threads API token ho, to `scripts/update_snapshots.py` se snapshots update karein.

## Data Update Mode

- **Checkpoint mode**: sabhi users ke liye. `/review` 24h, 72h aur 7d values collect karke prediction base update karta hai.
- **Snapshot mode**: Threads API ke saath. `scripts/update_snapshots.py` lagatar `snapshots[]` likhta hai aur nearest `performance_windows` update karta hai.




---

## AK-Threads-Booster Kya Hai

AK-Threads-Booster ek open-source Threads skill hai -- na writing template, na rule set, na koi AI content creator jo aapki jagah likhe.

Ye ek methodology system hai jo teen kaam karta hai:

1. **Aapke historical data ko analyze karta hai** ye identify karne ke liye ki kaunsa content aapke account pe sabse zyada Threads engagement generate karta hai
2. **Psychology aur Threads algorithm knowledge ko analytical lenses ki tarah use karta hai** ye explain karne ke liye ki kuch posts kyun accha perform karte hain
3. **Findings ko transparently present karta hai** taaki aap apna next move decide kar sako

Har user ko different results milte hain kyunki har account ki audience, style, aur dataset alag hota hai. Yahi fundamental difference hai data-driven Threads strategy aur generic social media advice mein.

### India Mein Ye Kyun Important Hai

India mein creator economy bohot tezi se grow kar rahi hai, aur Threads pe ek massive potential user base hai. Lekin Indian creators ko kuch unique challenges face karne padte hain:

- **Multilingual content ka balance**: Hindi mein likhen ya English mein? Hinglish use karein? Har audience segment ka response alag hota hai
- **Massive competition mein standout karna**: Itne creators ke beech mein apni distinct voice kaise banaye?
- **Brand Voice consistency**: Jab aap multiple languages mein post karte ho, to aapki voice consistent rehni chahiye

AK-Threads-Booster in sab problems ko address karta hai aapke apne data ke through. Ye dekhta hai ki aapki audience actually kis type ke content pe respond karti hai, aur accordingly suggestions deta hai.







---

## Core Principles

**Consultant hai, teacher nahi.** AK-Threads-Booster ye nahi bolega "aapko aise likhna chahiye." Ye bolega "jab aapne pehle ye kiya tha, data aisa dikhta tha -- aapke reference ke liye." No scoring, no corrections, no ghostwriting.

**Data-driven hai, rule-driven nahi.** Saari suggestions aapke apne historical data se aati hain, kisi generic "Social Media Marketing ke 10 Tips" list se nahi. Jab data insufficient hota hai, system honestly bata deta hai instead of pretending confidence.

**Red lines hi sirf hard rules hain.** Sirf wahi behaviors jinhe Meta ka algorithm explicitly penalize karta hai (engagement bait, clickbait, high-similarity reposts, etc.) direct warnings trigger karte hain. Baaki sab advisory hai. Final decision hamesha aapka hai.







---

## Multi-Tool Support

AK-Threads-Booster multiple AI coding tools ke saath kaam karta hai. Claude Code full 7-Skill experience deta hai; doosre tools core analysis capabilities offer karte hain.

### Supported Tools Aur Configuration Files

| Tool | Config Location | Scope |
|------|----------------|-------|
| **Claude Code** | `skills/` directory (7 Skills) | Full features: setup, voice, analyze, topics, draft, predict, review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | Core analysis (4-dimension) |
| **Codex** | `AGENTS.md` (root) | Core analysis (4-dimension) |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | Core analysis (4-dimension) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Core analysis (4-dimension) |
| **Google Antigravity** | `.agents/` directory + root `AGENTS.md` | Core analysis (4-dimension) |

### Feature Differences

- **Claude Code**: Full functionality including initialization (setup), Brand Voice profiling (voice), writing analysis (analyze), topic recommendations (topics), draft assistance (draft), viral post prediction (predict), aur post-publish review (review) -- saat independent Skills
- **Other tools**: Core writing analysis with four dimensions (style matching, psychology analysis, algorithm alignment check, AI-tone detection), same knowledge base share karte hain (`knowledge/` directory)
- **Google Antigravity**: Root `AGENTS.md` (consultant norms aur red-line rules) aur `.agents/` directory (rules files + analysis skills) dono read karta hai

Saare tool versions mein included hai:
- Consultant tone guidelines (no scoring, no corrections, no ghostwriting)
- Algorithm red-line rules (match hone pe warning)
- Knowledge base references (psychology, algorithm, AI-tone detection)







---

## Installation

### Option 1: GitHub Se Install Karein

```bash
# Apne Claude Code project directory mein
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### Option 2: Manual Installation

1. Ye repo locally clone karein:
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. `AK-Threads-booster` directory ko apne Claude Code project ke `.claude/plugins/` mein copy karein:
   ```bash
   cp -r AK-Threads-booster /path/to/your/project/.claude/plugins/
   ```

3. Claude Code restart karein. Skills automatically detect ho jayengi.

### Other Tools

Agar aap Cursor, Windsurf, Codex, ya GitHub Copilot use karte ho, to bas repo ko apne project directory mein clone kar lo. Har tool automatically apni corresponding configuration file read kar lega.







---

## Initialization

Pehli baar use karne se pehle, initialization run karein apna historical data import karne ke liye:

```
/setup
```

Initialization aapko guide karega:

1. **Data import method choose karein**
   - Meta Threads API (automatic fetch)
   - Meta account export (manual download)
   - Existing data files directly provide karein

2. **Automatic historical post analysis**, teen files generate hoti hain:
   - `threads_daily_tracker.json` -- Historical post database
   - `style_guide.md` -- Personalized style guide (aapki Hook preferences, word count ranges, ending patterns, etc.)
   - `concept_library.md` -- Concept library (track karta hai ki aapne audience ko kaunse concepts pehle se explain kiye hain)

3. **Analysis report** jo aapke account ki style characteristics aur data overview dikhata hai

Initialization sirf ek baar run karna hota hai. Baad ke data updates `/review` module ke through accumulate hote hain.







---

## The Seven Skills

### 1. /setup -- Initialization

Pehli baar use pe run karein. Historical posts import karta hai, style guide generate karta hai, aur concept library build karta hai.

```
/setup
```

### 2. /voice -- Brand Voice Profiling

Saare historical posts aur comment replies ki deep analysis karke ek comprehensive Brand Voice profile build karta hai. `/setup` ke style guide se zyada deep jaata hai, covering sentence structure preferences, tone shifts, emotional expression style, humor style, taboo phrases, aur bahut kuch.

```
/voice
```

Aapka Brand Voice jitna complete hoga, `/draft` ke outputs utne zyada aapke actual writing style ke close honge. `/setup` ke baad recommend kiya jaata hai.

Ye feature especially Indian creators ke liye valuable hai jo Hindi aur English dono mein post karte hain. Brand Voice analysis aapki language mixing patterns ko bhi capture karta hai -- kab aap English switch karte ho, kab Hindi mein rehte ho, aur ye patterns aapki audience ke saath kaise resonate karte hain.

Analysis dimensions include: sentence structure preferences, tone transition patterns, emotional expression style, knowledge presentation, tone differences between fans aur critics, common analogies aur metaphors, humor aur wit style, self-reference aur audience address, taboo phrases, paragraph rhythm micro-features, comment reply tone characteristics.

Output: `brand_voice.md`, automatically referenced by the `/draft` module.

### 3. /analyze -- Writing Analysis (Core Feature)

Post likhne ke baad, apna content paste karein four-dimension analysis ke liye:

```
/analyze

[apna post content paste karein]
```

Four analysis dimensions:

- **Style matching**: Aapke apne historical style se compare karta hai, deviations aur historical performance flag karta hai
- **Psychology analysis**: Hook mechanisms, emotional arc, sharing motivation, trust signals, cognitive biases, comment trigger potential
- **Algorithm alignment**: Red-line scan (match pe warnings) + positive signal assessment
- **AI-tone detection**: Sentence, structure, aur content levels pe AI-trace scanning

### 4. /topics -- Topic Recommendations

Jab samajh nahi aa raha aage kya likhein. Comments se aur historical data se insights mine karke topics recommend karta hai.

```
/topics
```

3-5 topics recommend karta hai, har ek ke saath: recommendation source, data-backed reasoning, similar historical post performance, estimated performance range.

### 5. /draft -- Draft Assistance

Aapke topic bank se ek topic select karke aapke Brand Voice ke basis pe draft generate karta hai. Ye AK-Threads-Booster ki sabse direct AI content creator function hai, lekin draft sirf ek starting point hai.

```
/draft [topic]
```

Aap topic specify kar sakte ho ya system ko topic bank se recommend karne de sakte ho. Draft quality depend karti hai aapke Brand Voice data ki completeness pe -- `/voice` pehle run karna noticeable difference laata hai.

Draft ek starting point hai. Aapko khud edit aur adjust karna padega. Edit karne ke baad, `/analyze` run karna recommended hai.

### 6. /predict -- Viral Post Prediction

Post likhne ke baad, publish karne ke 24 ghante baad ki performance estimate karein.

```
/predict

[apna post content paste karein]
```

Conservative/baseline/optimistic estimates output karta hai (views / likes / replies / reposts / shares) supporting rationale aur uncertainty factors ke saath.

### 7. /review -- Post-Publish Review

Publish karne ke baad, isse use karein actual performance data collect karne ke liye, predictions se compare karne ke liye, aur system data update karne ke liye.

```
/review
```

Ye kya karta hai:
- Actual performance data collect karta hai
- Predictions se compare karke deviations analyze karta hai
- Tracker aur style guide update karta hai
- Optimal posting times suggest karta hai







---

## Knowledge Base

AK-Threads-Booster mein teen built-in knowledge bases hain jo analytical reference points ki tarah kaam karte hain:

### Social Media Psychology (psychology.md)

Source: Academic research compilation. Covers Hook psychological trigger mechanisms, comment trigger psychology, sharing motivation aur virality (STEPPS framework), trust building (Pratfall Effect, Parasocial Relationship), cognitive bias applications (Anchoring, Loss Aversion, Social Proof, IKEA Effect), emotional arc aur arousal levels.

Purpose: `/analyze` mein psychology analysis dimension ke liye theoretical foundation. Psychology ek analytical lens hai, writing rule nahi.

### Meta Algorithm (algorithm.md)

Source: Meta patent documents, Facebook Papers, official policy statements, KOL observations (supplementary only). Covers red-line list (12 penalized behaviors), ranking signals (DM sharing, deep comments, dwell time, etc.), post-publish strategy, account-level strategy.

Purpose: `/analyze` mein algorithm alignment check ke liye rule foundation. Red-line items warnings trigger karte hain; signal items advisory tone mein present hote hain.

### AI-Tone Detection (ai-detection.md)

Covers sentence-level AI traces (10 types), structure-level AI traces (5 types), content-level AI traces (5 types), AI-tone reduction methods (7 types), scan trigger conditions, aur severity definitions.

Purpose: `/analyze` mein AI-tone scanning ke liye detection baseline. AI traces flag karta hai aapke fix karne ke liye; auto-correct nahi karta.







---

## Typical Workflow

```
1. /setup              -- Pehla use, system initialize karein
2. /voice              -- Deep Brand Voice profiling (ek baar run karein)
3. /topics             -- Topic recommendations dekhein
4. /draft [topic]      -- Draft generate karein
5. /analyze [post]     -- Draft ya apni writing analyze karein
6. (Analysis ke basis pe edit karein)
7. /predict [post]     -- Publish karne se pehle performance estimate karein
8. (Publish karein)
9. /review             -- Publish ke 24h baad data collect karein
10. Step 3 pe wapas jayein
```

Har cycle ke saath system ki analysis aur predictions zyada accurate hoti jaati hain. `/voice` sirf ek baar run karna hota hai (ya zyada posts accumulate hone ke baad re-run karein). `/draft` automatically aapki Brand Voice file reference karta hai.







---

## Frequently Asked Questions

**Q: Kya AK-Threads-Booster mere liye posts likhega?**
`/draft` module initial drafts generate karta hai, lekin drafts sirf starting point hain. Aapko khud edit aur refine karna padega. Draft quality depend karti hai aapke Brand Voice data ki completeness pe. Baaki modules sirf analyze aur advise karte hain -- ghostwriting nahi.

**Q: Kya ye free hai?**
Haan, completely free aur open-source hai. MIT License ke under available hai. Koi subscription nahi, koi premium tier nahi, koi hidden charges nahi. Aapko sirf Claude Code ya koi supported AI coding tool chahiye.

**Q: Limited data ke saath analysis accurate hogi?**
Zyada nahi. System honestly bata dega. Data accumulate hone ke saath accuracy improve hoti hai.

**Q: Kya suggestions follow karna zaroori hai?**
Nahi. Saari suggestions sirf advisory hain. Final decision hamesha aapka hai. Sirf algorithm red lines ke liye direct warnings milte hain (writing patterns jo demotion trigger karte hain).

**Q: Hindi content ke saath kaam karta hai?**
Haan. Knowledge base English mein hai, lekin analysis universal principles pe based hai. System aapke historical data se compare karta hai -- agar aap Hindi ya Hinglish mein post karte ho, to system aapke Hindi/Hinglish style se seekhega. Brand Voice feature aapki language mixing patterns ko bhi capture karta hai.

**Q: Multilingual posting mein kaise help karta hai?**
Brand Voice profiling aapke language switching patterns track karta hai -- kab aap English use karte ho, kab Hindi, kab Hinglish. Ye patterns aapki audience ke response data ke saath correlate hote hain, to aapko pata chal jaata hai ki kaunsa language mix aapke specific audience ke liye best perform karta hai.

**Q: Threads ke alawa doosri platforms support karta hai?**
Currently primarily Threads ke liye designed hai. Knowledge base ke psychology principles universal hain, lekin algorithm knowledge base Meta ki platform pe focused hai.

**Q: Generic AI writing tool se ye kaise alag hai?**
Generic tools general models se content produce karte hain. AK-Threads-Booster ki analysis aur suggestions saari aapke apne historical data se aati hain, to har user ko different results milte hain. Ye consultant hai, ghostwriter nahi. Yahi key hai ek aisi Threads strategy build karne ki jo actually aapki audience ke liye fit ho.

**Q: Kya ye guarantee karta hai ki mere posts viral honge?**
Nahi. Threads ka algorithm ek bohot complex system hai, aur koi bhi tool viral posts guarantee nahi kar sakta. AK-Threads-Booster jo karta hai wo ye hai ki aapko apne historical data ke basis pe better decisions lene mein help karta hai, known algorithm red lines se bachata hai, aur psychology aur data-driven analysis ke through har post ki performance probability improve karta hai. Ye currently sabse comprehensive Threads content creation skill hai, lekin jo factors determine karte hain ki koi post viral hoga ya nahi -- timing, topic relevance, audience state, us moment pe algorithm ki distribution logic -- ye sab kisi bhi tool ke control mein nahi hain. Isse apna data consultant samjho, viral guarantee machine nahi.







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


