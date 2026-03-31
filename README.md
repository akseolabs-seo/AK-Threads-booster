[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

# AK體 Threads Booster

> **English Summary:** AK-Threads-booster is a Claude Code and Codex skill and AI writing assistant built specifically for Threads creators. This open-source Threads skill analyzes your historical post data, leverages social media psychology research and the Threads algorithm to provide personalized writing analysis, Brand Voice profiling, and draft assistance. Whether you need an AI social media post generator, actionable Threads tips, a data-backed Threads strategy for sustainable Threads growth and higher Threads engagement, or a ready-to-use content creation skill, this tool turns your own data into insights. Works as a skill / plugin for Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, and Google Antigravity. Not a template -- a consultant skill powered by your data.

一套專為 Threads 發文設計的 AI Skill，支援 Claude Code、Cursor、Codex、Windsurf、GitHub Copilot、Google Antigravity 等主流 AI 編碼工具。數據驅動的 Threads 經營顧問系統，基於你自己的歷史數據、社交媒體心理學研究、Meta 演算法機制，為你的帳號提供個人化的寫文分析、Brand Voice 建立與初稿輔助。

這個 Skill 幫助你掌握 Threads 演算法的運作邏輯，找到屬於你的 Threads 流量密碼，持續產出高互動的 Threads 爆文。包含 7 個獨立 Skill 模組，從初始化、選題、寫文、分析到發文後覆盤，覆蓋完整的 Threads 發文流程。

如果你正在尋找一套結合 AI 寫文能力與數據分析的 Threads AI Skill，AK體就是為這個需求設計的。它不靠猜測，靠你自己的數據。關於 AK體背後的 [Threads 演算法與流量研究](https://akseolabs.com/blog/threads-algorithm-traffic)，可以先看這篇了解整套系統的理論基礎。

---

## AK體是什麼

AK體是一個開源的 Threads 發文 Skill，不是寫文模板，不是規則集，也不是 AI 代寫工具。

它是一套可直接安裝使用的 Skill 方法論系統，核心做三件事：

1. **分析你的歷史數據**，找出什麼內容在你的帳號上能帶來最多 Threads 流量
2. **用心理學和 Threads 演算法知識作為分析鏡頭**，幫你理解為什麼有效
3. **把分析結果攤開來**，讓你自己判斷下一步怎麼做

每個用戶跑出來的結果都不一樣，因為每個人的受眾、風格、數據都不同。這正是數據驅動的 Threads 經營方式和通用模板最大的差異。

---

## 核心理念

**顧問不是老師。** AK體不會說「你應該這樣寫」，它會說「你之前這樣做的時候數據長這樣，供你參考」。不打分、不糾正、不代寫。

**數據驅動不是規則驅動。** 所有建議都來自你自己的歷史數據，不是通用的「社群行銷 10 大法則」。數據不足時會誠實告訴你，不會假裝有信心。

**紅線是唯一硬規則。** 只有 Meta 演算法明確會降權的東西（engagement bait、clickbait、高相似度重複等）才會直接警告。其他所有分析都是參考，用戶永遠有最終決定權。

---

## 多工具支援

AK-Threads-booster 支援多種 AI 編碼工具。Claude Code 提供完整的 7 個 Skill 功能，其他工具則提供核心分析功能。

### 支援的工具與檔案位置

| 工具 | 設定檔位置 | 功能範圍 |
|------|-----------|----------|
| **Claude Code** | `skills/` 目錄（7 個 Skill） | 完整功能：setup、voice、analyze、topics、draft、predict、review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | 核心分析功能（四維度分析） |
| **Codex** | `AGENTS.md`（根目錄） | 核心分析功能（四維度分析） |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | 核心分析功能（四維度分析） |
| **GitHub Copilot** | `.github/copilot-instructions.md` | 核心分析功能（四維度分析） |
| **Google Antigravity** | `.agents/` 目錄 + 根目錄 `AGENTS.md` | 核心分析功能（四維度分析） |

### 功能差異說明

- **Claude Code**：完整功能，包含初始化（setup）、Brand Voice 建立（voice）、寫文分析（analyze）、選題推薦（topics）、寫文輔助（draft）、爆文預估（predict）、發文後回饋（review）七個獨立 Skill
- **其他工具**：提供核心的寫文分析功能（風格比對、心理學分析、演算法對齊檢查、AI 味檢測四個維度），共用同一組知識庫（`knowledge/` 目錄）
- **Google Antigravity**：同時讀取根目錄 `AGENTS.md`（顧問規範與紅線規則）和 `.agents/` 目錄（rules 規則檔 + skills 分析技能），提供核心四維度分析功能

所有工具版本都包含：
- 顧問語氣規範（不打分、不糾正、不代寫）
- 演算法紅線規則（命中即警告）
- 知識庫引用（心理學、演算法、AI 味檢測）

---

## 安裝方式

### 方式一：透過 GitHub 安裝

```bash
# 在你的 Claude Code 專案目錄下
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### 方式二：手動安裝

1. Clone 這個 repo 到本地：
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. 把整個 `AK-Threads-booster` 目錄放到你的 Claude Code 專案的 `.claude/plugins/` 下：
   ```bash
   cp -r AK-Threads-booster /path/to/your/project/.claude/plugins/
   ```

3. 重啟 Claude Code，Skill 會自動被偵測到。

### 其他工具

如果你使用 Cursor、Windsurf、Codex 或 GitHub Copilot，把整個 repo clone 到你的專案目錄下即可。各工具會自動讀取對應的設定檔。

---

## 初始化流程

首次使用前，你需要先跑一次初始化來匯入歷史數據：

```
/setup
```

初始化會引導你完成：

1. **選擇數據匯入方式**
   - Meta Threads API（自動抓取）
   - Meta 帳號匯出（手動下載）
   - 直接提供現有數據檔案

2. **自動分析歷史貼文**，生成三份檔案：
   - `threads_daily_tracker.json` -- 歷史貼文數據庫
   - `style_guide.md` -- 個人化風格指南（你的 Hook 偏好、字數範圍、結尾模式等）
   - `concept_library.md` -- 概念知識庫（追蹤你已向受眾解釋過的概念）

3. **報告分析結果**，讓你了解自己帳號的風格特徵和數據概況

初始化只需執行一次。之後的數據更新透過 `/review` 模組持續累積。

---

## 七個 Skill 的使用說明

### 1. /setup -- 初始化

首次使用時執行。匯入歷史貼文、生成風格指南、建立概念知識庫。

```
/setup
```

觸發詞：`初始化`、`setup`、`設定`

### 2. /voice -- Brand Voice 建立

深度分析所有歷史貼文和留言回覆，建立超詳盡的 Brand Voice 檔案。比 `/setup` 產出的風格指南更深入，涵蓋句式偏好、語氣轉換、情緒表達、幽默風格、禁忌用語等微觀特徵。

```
/voice
```

Brand Voice 越完整，`/draft` 寫出來的初稿越像你。建議在 `/setup` 之後跑一次。

分析維度包含：句式結構偏好、語氣轉換模式、情緒表達方式、知識展示方式、對粉絲 vs 對噴子的語氣差異、常用類比和比喻手法、笑點和幽默風格、自稱方式和對讀者的稱呼、禁忌用語、段落節奏的微觀特徵、留言回覆的語氣特徵。

產出：`brand_voice.md`，供 `/draft` 模組自動引用。

觸發詞：`brand voice`、`品牌聲音`、`語感分析`

### 3. /analyze -- 寫文分析（核心功能）

寫完貼文後，貼上內容做四維度分析：

```
/analyze

[貼上你的貼文內容]
```

四個分析維度：

- **風格比對**：跟你自己的歷史風格做比對，標記偏離項和歷史表現
- **心理學分析**：Hook 機制、情緒弧線、分享動機、信任元素、認知偏誤、留言觸發潛力
- **演算法對齊**：紅線掃描（命中直接警告）+ 加分信號評估
- **AI 味檢測**：語句層、結構層、內容層的 AI 痕跡掃描

觸發詞：`分析`、`analyze`、`檢查`、`AK體`

### 4. /topics -- 選題推薦

不知道下一篇寫什麼的時候用。從留言挖礦和歷史數據推薦題材。

```
/topics
```

推薦 3-5 個題材，每個附上：推薦來源、數據支撐的理由、相似歷史貼文表現、預估表現區間。

觸發詞：`選題`、`topics`、`寫什麼`、`題材`

### 5. /draft -- 寫文輔助

從題材庫選題，基於用戶的 Brand Voice 產出貼文初稿。這是 AK體作為 AI 寫文輔助工具最直接的功能，但初稿只是起點。

```
/draft [題材]
```

可以指定題材，也可以不指定讓系統從題材庫推薦。初稿品質取決於 Brand Voice 資料的完整度：有跑過 `/voice` 的效果會明顯更好。

初稿只是起點，用戶需要自己修改調整。寫完後建議用 `/analyze` 跑一次分析。

觸發詞：`寫文`、`draft`、`起草`、`幫我寫`

### 6. /predict -- 爆文預估

寫完貼文後，預估發布後 24 小時的表現數據。想知道你的內容有沒有 Threads 爆文潛力，發文前先跑一次預估。

```
/predict

[貼上你的貼文內容]
```

產出保守/基準/樂觀三個區間的預估（views / likes / replies / reposts / shares），附上預估依據和不確定因素。

觸發詞：`預估`、`predict`、`預測`、`爆文`

### 7. /review -- 發文後回饋

發文後用來回收數據、跟預估做比對、更新系統數據。

```
/review
```

會做的事：
- 回收實際表現數據
- 跟預估比對，分析偏差原因
- 更新 tracker 和風格指南
- 建議最佳發文時間

觸發詞：`回顧`、`review`、`覆盤`、`數據`

---

## 知識庫說明

AK體內建三份知識庫，作為分析的參考基準：

### 社交媒體心理學知識庫（psychology.md）

來源：學術研究整理。涵蓋 Hook 心理觸發機制、留言觸發心理學、分享動機與傳播機制（STEPPS 框架）、信任建立原理（Pratfall Effect、Parasocial Relationship）、認知偏誤應用（Anchoring、Loss Aversion、Social Proof、IKEA Effect）、情緒弧線與激發程度。

用途：作為 `/analyze` 心理學分析維度的理論基礎。心理學是分析鏡頭，不是寫作規則。

### Meta 演算法知識庫（algorithm.md）

來源：Meta 專利文件、Facebook Papers、官方政策聲明、KOL 觀察（僅作補充）。涵蓋紅線清單（12 項降權行為）、排名信號（私訊分享、深度留言、停留時間等）、發文後策略、帳號層級策略。想深入了解 Threads 演算法的底層邏輯，可以參考這篇完整解析：[Threads 演算法與流量機制深度分析](https://akseolabs.com/blog/threads-algorithm-traffic)。

用途：作為 `/analyze` 演算法對齊檢查的規則基礎。紅線項目命中即警告，信號項目用顧問語氣提供參考。

### AI 味檢測知識庫（ai-detection.md）

涵蓋語句層級 AI 痕跡（10 種）、結構層級 AI 痕跡（5 種）、內容層級 AI 痕跡（5 種）、降 AI 味方法（7 種）、掃描觸發條件和嚴重度定義。

用途：作為 `/analyze` AI 味掃描的檢測基準。標記出 AI 痕跡讓用戶自己改，不自動修改。

---

## 典型工作流程

```
1. /setup              -- 首次使用，初始化系統
2. /voice              -- 深度建立 Brand Voice（建議跑一次）
3. /topics             -- 不知道寫什麼，看推薦
4. /draft [題材]       -- 產出初稿
5. /analyze [貼文]     -- 分析初稿或自己寫的貼文
6. （用戶根據分析自行調整）
7. /predict [貼文]     -- 發文前預估表現
8. （發文）
9. /review             -- 發文 24h 後回收數據
10. 回到步驟 3
```

每跑一輪，系統的分析和預估就會更準一點。`/voice` 只需要跑一次（或在累積更多貼文後重跑更新），`/draft` 會自動引用 Brand Voice 檔案。

---

## 常見問題

**Q：AK體會幫我寫貼文嗎？**
`/draft` 模組可以產出初稿，但初稿只是起點，你需要自己修改調整。初稿品質取決於你的 Brand Voice 資料完整度。其他模組只做分析和建議，不代寫。

**Q：數據很少的時候分析準嗎？**
不太準，系統會誠實告訴你。隨著數據累積會越來越準。

**Q：一定要照建議做嗎？**
不用。所有建議都只是參考，用戶永遠有最終決定權。唯一直接警告的是演算法紅線（會被降權的寫法）。

**Q：支援 Threads 以外的平台嗎？**
目前主要針對 Threads 設計。知識庫中的心理學原理是通用的，但演算法知識庫專注 Meta 平台。

**Q：這跟一般的 AI 寫文工具有什麼不同？**
一般工具用通用模型產出內容。AK體的分析和建議全部來自你自己的歷史數據，所以每個用戶的結果都不一樣。它是顧問，不是代筆。

**Q：這個 Skill 跟其他 Claude Code Skill 有什麼不同？**
大多數 Skill 是通用型的開發工具。AK體是專門為 Threads 內容創作者設計的垂直領域 Skill，內建社交媒體心理學知識庫、Meta 演算法研究、AI 味檢測系統，專注解決 Threads 發文的實際問題。

**Q：可以用在其他社群平台嗎？**
Skill 的心理學分析和 AI 味檢測是通用的，但演算法知識庫目前專注 Meta 平台（Threads / Instagram）。未來可能擴展到其他平台。

**Q：用了 AK體就能保證爆文嗎？**
不能。Threads 的演算法是極其複雜的系統，沒有任何工具可以保證爆文。AK體能做的是讓你基於自己的歷史數據做出更好的判斷，避免踩到已知的演算法紅線，並從心理學和數據的角度提高每篇貼文的表現機率。它是目前最完整的 Threads 發文 Skill，但最終決定一篇文能不能爆的因素太多了，包括時機、話題、受眾狀態、演算法當下的分發邏輯，這些都不是任何工具能完全掌控的。把它當成你的數據顧問，不是爆文保證機。

---

## 目錄結構

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

MIT License. 詳見 [LICENSE](./LICENSE)。
