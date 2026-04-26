[中文](README.md) | [English](README.en.md)

# AK體-基於Threads演算法的優化skill

AK-Threads-Booster 是這個 skill 的內部代號與安裝 id。

AK-Threads-Booster 是一套給 Threads 創作者用的 AI skill 系統。

它不是要幫你亂寫一堆貼文，而是幫你把「選題、起草、分析、預測、復盤」變成一套有資料依據的工作流，讓你更容易發出值得被分享、收藏、討論的內容。

如果你平常的痛點是這些：

- 不知道下一篇到底該寫什麼
- 有很多題目，但分不出哪個更值得先發
- 文章不是寫不好，只是常常撞題、老梗、沒新鮮度
- 想讓內容更像自己，不想一看就很 AI
- 發完之後沒有把結果整理回來，下一篇又從零猜

這套 skill 就是為這些問題設計的。

它不保證爆文。

它做的是讓你用自己的歷史資料，提高每一次發文決策的品質，讓「更有擴散機會」這件事變得比較可複製。

---

## 這套 skill 會幫你做什麼

### 1. 幫你選出更值得發的題

`/topics` 不是單純丟熱門題給你。

它會一起看：

- 你的歷史貼文表現
- 留言裡反覆出現的問題
- 你自己曾經回過哪些問題
- 最近有沒有撞到同一個 semantic cluster
- 外部話題現在是不是已經過熱

也就是說，它不只是找「熱門」，而是找「對你這個帳號來說，現在更值得發」的題目。

### 2. 幫你起草，但盡量像你

`/draft` 會根據：

- `brand_voice.md`
- `style_guide.md`
- 歷史貼文
- concept library

來起草一篇比較接近你語感的內容。

而且它不是拿到題目就直接寫：

- 先做 freshness gate，避免你花時間寫一個已經被寫爛的角度
- 做 fact-check，但**不會動你自己說過的個人事實與事件順序**（你的貼文是 source of truth）
- research 時會主動丟「你可能沒想到的 2-3 個角度」給你選，幫貼文變更豐富
- 寫完以後會回問 3-5 個針對這篇的改進問題，不是罐頭提問

這些對話功能都是開關式的——第一次會問你要不要開，也可以設成 always on / always off，存在 `threads_booster_config.json`。想要快就快，想要深就深。

### 3. 幫你在發文前做最後判斷

`/analyze` 是這套 skill 的 decision layer。

它會看：

- 有沒有演算法紅線
- 這篇最大的上升空間在哪
- 主要卡點在哪
- 比較像 follower-fit 還是 stranger-fit
- 有沒有 AI 味太重

這樣你在按下發送前，不是只靠感覺。

### 4. 幫你建立比較合理的預期

`/predict` 會用相似歷史貼文幫你估 24 小時的可能區間，讓你不要因為單篇波動就誤判。

### 5. 幫你把發文結果變成下一次的優勢

`/review` 會把實際表現、預測偏差、風格訊號再寫回 tracker。

這點很重要，因為很多工具只會給你建議，不會讓系統越用越準。這套 skill 的重點就是把學到的東西留下來。

### 6. 幫你更新 tracker，不用每次手動整理

`/refresh` 可以更新 `threads_daily_tracker.json`：

- 有 Threads API token 就走 API
- 沒有 API 就走 Chrome MCP 抓自己的 Threads profile

你不用每次都自己慢慢補資料。

---

## 最適合誰

這套 skill 特別適合：

- 已經有固定在經營 Threads 的人
- 想把發文從「靈感型」變成「決策型」的人
- 想更穩定找到下一篇題目的人
- 想知道自己什麼內容比較有機會擴散的人
- 想把歷史貼文真的變成可用資產的人

如果你現在還完全沒有歷史資料，它也可以用，但前期的判斷會比較弱。這套系統的價值，會隨著你的資料累積而變強。

---

## 第一次使用你會得到什麼

跑完 `/setup` 之後，工作目錄通常會有：

- `threads_daily_tracker.json`
- `style_guide.md`
- `concept_library.md`
- `brand_voice.md`（如果有跑 `/voice`）
- `posts_by_date.md`
- `posts_by_topic.md`
- `comments.md`

其中最重要的是 `threads_daily_tracker.json`。

其他 skill 幾乎都是圍繞這份 tracker 在做判斷。

---

## 建議使用流程

### 第一次使用

```text
/setup
/voice
```

先把歷史資料整理好，再把 Brand Voice 建起來。

`/voice` 產出的 `brand_voice.md` 是**參考初稿**，不是定稿。LLM 從外部看你的貼文一定會漏東西。建議：

- 直接改檔案裡任何覺得不對的地方
- 最下面的 **Manual Refinements** 區塊用來補分析漏掉的、你自己知道的細節（禁用詞、必做事項、「這不是我」的例子）
- 重跑 `/voice` 會保留你改過的內容，不會覆蓋掉

`/draft` 會把 Manual Refinements 當硬約束讀，優先級高於其他章節。

### 平常發文前

```text
/topics
/draft
/analyze
```

這是最實用的一組流程：

- `/topics` 找題
- `/draft` 起草
- `/analyze` 發文前檢查

### 發完之後

```text
/predict
/review
```

這樣系統會慢慢知道：

- 你估得準不準
- 哪些題真的會跑
- 哪些風格只是你以為有效

---

## 資料可以怎麼進來

你可以用這些方式建立資料：

- Threads Developer API token
- Meta 官方匯出 zip
- 既有 JSON / Markdown / CSV
- Chrome 已登入 Threads + Claude in Chrome MCP
- 舊版 tracker migration

API 不是必須，但如果你有 API，更新會輕鬆很多。

---

## 產品定位

AK-Threads-Booster 是一套以你的 Threads 歷史資料為核心的內容決策系統。

它的重點不是自動亂生文，而是幫你：

- 找出更值得發的題目
- 起草更接近你自己的內容
- 避開明顯的重複與紅線
- 把每次發文結果累積成下一次判斷的依據

---

## 安裝

### Claude Code

```bash
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### 手動安裝

```bash
git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
```

再依你使用的工具，把這個 repo 放到對應的 skill / plugin 目錄即可。

---

## 目錄結構

```text
AK-Threads-booster/
|- SKILL.md
|- AGENTS.md
|- skills/
|  |- setup/SKILL.md
|  |- refresh/SKILL.md
|  |- analyze/SKILL.md
|  |- draft/SKILL.md
|  |- predict/SKILL.md
|  |- review/SKILL.md
|  |- topics/SKILL.md
|  |- voice/SKILL.md
|- knowledge/
|  |- _shared/
|  |- psychology.md
|  |- algorithm.md
|  |- ai-detection.md
|  |- data-confidence.md
|  |- chrome-selectors.md
|- scripts/
|  |- fetch_threads.py
|  |- parse_export.py
|  |- update_snapshots.py
|  |- update_topic_freshness.py
|  |- render_companions.py
|- templates/
|- examples/


```
## Star History

<a href="https://www.star-history.com/?repos=akseolabs-seo%2FAK-Threads-booster&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=akseolabs-seo/AK-Threads-booster&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=akseolabs-seo/AK-Threads-booster&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=akseolabs-seo/AK-Threads-booster&type=date&legend=top-left" />
 </picture>


---

## License

MIT License. See [LICENSE](./LICENSE).
