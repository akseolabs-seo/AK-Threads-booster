# Changelog

What changed in AK-Threads-Booster, in plain language.

---

## Unreleased — Token redesign Phase 1

### 每次 `/analyze`、`/predict`、`/draft` 都唔再食 100K+ token

呢套 skill 之前每次 invoke 都會自動 load 三個大 knowledge file（psychology / algorithm / ai-detection 共 ~32K tokens）+ 成個 `threads_daily_tracker.json`（成 168KB / ~56K tokens）。實際分析 / 起稿時，通常只需要 knowledge 入面一兩段、tracker 入面 5-10 個 comparable post。**每次 invoke 開頭就食晒 ~95-110K token**，仲未 reason 你篇 post。

Phase 1 redesign 嘅核心：**push knowledge out of context, into queryable tools**。

- **新檔案 `tracker_summary.md`**（5KB markdown digest）— `/refresh` 跑完自動 generate。包含：top 10 alltime / top 10 last-30d / hook distribution / topic clusters / AI-tone signal frequencies / posting cadence / word-count quartiles / recent topic freshness。skills 而家讀呢個，唔再讀全本 tracker。
- **新 CLI `scripts/tracker_query.py`** — 7 個 subcommand（recent / top / comparable / hook-stats / ai-tone-stats / post / meta），返 1-10 KB 結構化 JSON。需要 comparable set 嗰陣 query 一次，唔再 Read 全本 tracker。
- **新 CLI `scripts/tracker_archive.py`** — `/refresh` 跑完之後自動將 60 日前嘅 post 移去 `archive/<YYYY>-<MM>.json`。Idempotent：冇舊 post 就 no-op。有 `top_performers_alltime[]` 留喺主 tracker，summary skill 唔會失去歷史錨點。
- **新 CLI `scripts/build_tracker_summary.py`** — 重新生成 `tracker_summary.md`。`/refresh` 自動 call。

**`/analyze`、`/predict`、`/review`、`/topics`、`/draft` SKILL.md 全部改晒。** 而家：

1. 預設讀 `tracker_summary.md`（5KB），唔再 bulk-load 知識庫
2. 需要 comparable post 嗰陣 call `tracker_query.py` 拎 1-10KB
3. 知識文件變 reference material — 需要某個 signal 嗰陣先 Glob + Read --offset --limit 開到嗰段

### Backwards compatible

冇 break 任何嘢。如果你個 working dir 仲未有 `tracker_summary.md`（譬如未跑過新版 `/refresh`），skill 會 fallback 去舊嘅 full-Read 路徑，同時 print 一行 hint 叫你跑 `/refresh` upgrade。即係：

- 舊 install — 行得，但慢，會見 hint
- 新 install / 跑過 `/refresh` 之後 — 自動行 lean path

### 量度

A/B harness（`scripts/tests/ab_compare.py`）對住真實 plugin v1.1.0 + 真實 working dir 嘅 measurement：

| Skill | Before | After | Reduction |
|---|---|---|---|
| `/analyze` | 118K tokens | 25K tokens | **78.4%** |
| `/predict` | 115K tokens | 23K tokens | **80.2%** |
| `/draft` | 118K tokens | 24K tokens | **79.6%** |
| `/review` | 84K tokens | 23K tokens | **72.5%** |
| `/topics` | 81K tokens | 22K tokens | **72.4%** |
| **5 skills 加埋** | **~516K** | **~118K** | **77.2%** |

唔係估算，係實際對住 file 大小量度。Output equivalence 要靠真 LLM call 對比驗證，呢 part 喺 PR review / 用家手動驗證階段做。

### Tests

新增 50 個 unittest case 覆蓋 4 個 script + A/B harness：
- `test_tracker_query.py` — 22 cases
- `test_tracker_archive.py` — 13 cases（包 idempotency、backup rotation、dry-run、comparable dedupe）
- `test_build_tracker_summary.py` — 7 cases
- `test_ab_compare.py` — 8 cases

全部 green。

---

## 2026-04-22

### `/draft` 變聰明了

- **寫稿前會先跟你討論**。找完 research、做完 fact-check 以後，不會直接開寫，會先問你 2-4 個關鍵問題（要不要用這個角度、這個說法查不到你有沒有第一手經驗、要不要預先回應留言區會吵的反駁），等你回覆再下筆。
- **寫完以後會再回問你 3-5 個針對這篇的改進問題**。不是「還可以嗎？」這種罐頭，是針對這篇的 hook、證據、立場強度、結尾寫法去問。
- **主動丟你可能沒想到的角度**。research 時會挑 2-3 個你原本沒提到的切入方式給你選（反直覺、歷史對照、產業類比……），能用就用，不想用就不用。
- **不會亂你自己說過的事**。fact-check 的時候，只要是你講過的個人事實或事件順序，以你自己的貼文為準，網路搜尋不會推翻你。查不到的個人細節會標 `[confirm with user]` 來問你，不自己猜。

### 你可以決定 `/draft` 要不要跟你聊

這些討論功能都是可開關的。第一次會問你要不要開，你可以回答：

- **只這次**——答完這次，下次再問
- **always on**——以後都要討論
- **always off**——以後都不討論，直接給稿

選擇會存在 `threads_booster_config.json`，隨時改。

> 想要快就選 always off，想要深就選 always on。預設是每次問你一次。

### `/voice` 生成更細、也更誠實

- **現在會說清楚「這是參考初稿，不是定稿」**。LLM 從外面看你的貼文一定漏東西，你自己才最懂自己。
- **分析維度加深**。除了原本的結構/語氣/情緒等，還會幫你抓：高頻字詞 top 15-20（含出現次數）、開場/收尾/標點習慣、中英夾雜模式、論證慣性。
- **新增 Manual Refinements 區塊**。檔案最下面留一塊給你自己填（分析哪裡寫錯了、漏了什麼、哪些是你「絕對不會講」的話）。你填的內容優先級最高，`/draft` 寫稿會當成硬規則。
- **重跑 `/voice` 不會蓋掉你的手動修改**。會先讀舊檔、保留你動過的地方，再跟你確認才覆蓋。

### `/analyze` 和 `/review` 也會主動問問題

和 `/draft` 一樣的邏輯：分析完/檢討完，可以選要不要補問 2-3 個針對這篇/這次表現的追問。同一個開關控制，設定方式一樣。

### `/review` 會回看 `/draft` 當初的決定

檢討實際表現時，會拉出你當初在 `/draft` 討論階段做過的選擇（「接受了這個角度」「丟了那個說法」），對照貼文實際表現回頭看當初的判斷是不是對的。下次類似情境就知道怎麼選。

### 新檔案

- `threads_booster_config.json`——存你的偏好設定
- `CHANGELOG.md`——就是你在看的這個

---

### 為什麼做這些改動

使用者反饋兩件事：`/draft` 寫太快、太少跟人討論，有時候會把貼文角度帶偏、甚至搞錯你講過的個人細節；`/voice` 生出來的 brand voice 又粗、又會被當成定稿用。

這次的核心想法：

1. **對話不是義務，是選項**——想要就開，不想要就關
2. **你自己的話才是最終依據**——不管是 brand voice 還是個人事實
3. **AI 的產出是初稿，你的手動修改優先級最高**
