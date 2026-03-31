[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

# AK-Threads-Booster

> **English Summary:** AK-Threads-booster is a Claude Code and Codex skill and AI writing assistant built specifically for Threads creators. This open-source Threads skill analyzes your historical post data, leverages social media psychology research and the Threads algorithm to provide personalized writing analysis, Brand Voice profiling, and draft assistance. Works as a skill / plugin for Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, and Google Antigravity.

Threads クリエイター専用に設計された、データ駆動型の AI ライティング Skill。Claude Code、Cursor、Codex、Windsurf、GitHub Copilot、Google Antigravity に対応。あなた自身の投稿データ、ソーシャルメディア心理学研究、Meta のスレッズ アルゴリズムを基に、パーソナライズされた投稿分析、Brand Voice 構築、下書き支援を提供します。

日本は Threads のグローバル第2位の市場です。毎日大量のコンテンツが投稿される中、「何を書けば伸びるのか」「スレッズ アルゴリズムは日本語コンテンツをどう扱うのか」「フォロワー 増やし方の正解は何か」。こうした疑問に、あなた自身の過去データから答えを出すのが AK-Threads-Booster です。

汎用の SNS 運用テンプレートではありません。あなたのアカウントのデータを分析し、何が効果的かを特定し、その根拠を心理学とアルゴリズムの観点から説明する、データ駆動型のコンサルタント Skill です。スレッズ攻略に必要なのは、一般論ではなく、あなた自身のデータに基づいた戦略です。

---

## AK-Threads-Booster とは

AK-Threads-Booster はオープンソースの Threads 投稿 Skill です。ライティングテンプレートでも、ルール集でも、AI 代筆ツールでもありません。

直接インストールして使える Skill 方法論システムで、核心は3つです：

1. **あなたの過去データを分析** し、どのコンテンツがアカウントで最もエンゲージメントを獲得しているかを特定
2. **心理学とスレッズ アルゴリズムの知識を分析レンズとして使用** し、なぜそれが効果的なのかを論理的に説明
3. **分析結果を透明に提示** し、次のアクションはあなた自身が判断

ユーザーごとに異なる結果が出ます。オーディエンス、投稿スタイル、データが異なるためです。これが汎用テンプレートとデータ駆動型のスレッズ攻略の根本的な違いです。

---

## コアコンセプト

**コンサルタントであり、先生ではない。** AK-Threads-Booster は「こう書くべき」とは言いません。「以前こう書いたとき、データはこうでした。参考までに」と伝えます。採点なし、添削なし、代筆なし。

**データ駆動であり、ルール駆動ではない。** すべての提案はあなた自身の過去データに基づいています。「SNS 運用 10 の法則」のような一般論ではありません。データが不十分な場合は、正直にそう伝えます。

**レッドラインだけが唯一のハードルール。** Meta のアルゴリズムが明示的にペナルティを科す行為（engagement bait、clickbait、高類似度の重複投稿など）のみ直接警告します。それ以外のすべての分析はアドバイスであり、最終判断はあなたにあります。

---

## マルチツール対応

AK-Threads-Booster は複数の AI コーディングツールに対応しています。Claude Code では7つの Skill をフル活用でき、他のツールではコア分析機能を利用できます。

### 対応ツールと設定ファイル

| ツール | 設定ファイルの場所 | 機能範囲 |
|--------|-------------------|----------|
| **Claude Code** | `skills/` ディレクトリ（7 Skill） | フル機能：setup、voice、analyze、topics、draft、predict、review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | コア分析（4次元分析） |
| **Codex** | `AGENTS.md`（ルート） | コア分析（4次元分析） |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | コア分析（4次元分析） |
| **GitHub Copilot** | `.github/copilot-instructions.md` | コア分析（4次元分析） |
| **Google Antigravity** | `.agents/` ディレクトリ + ルート `AGENTS.md` | コア分析（4次元分析） |

### 機能の違い

- **Claude Code**：フル機能。初期化（setup）、Brand Voice 構築（voice）、投稿分析（analyze）、トピック推薦（topics）、下書き支援（draft）、バズ予測（predict）、投稿後レビュー（review）の7つの独立した Skill
- **他のツール**：4次元のコア投稿分析（スタイルマッチング、心理学分析、アルゴリズム対齐チェック、AI 臭検知）。共通のナレッジベース（`knowledge/` ディレクトリ）を使用
- **Google Antigravity**：ルートの `AGENTS.md`（コンサルタント規範とレッドラインルール）と `.agents/` ディレクトリ（rules + skills）の両方を読み込み

すべてのツールバージョンに含まれる内容：
- コンサルタントトーンのガイドライン（採点なし、添削なし、代筆なし）
- アルゴリズムレッドラインルール（該当時は即警告）
- ナレッジベース参照（心理学、アルゴリズム、AI 臭検知）

---

## インストール方法

### 方法1：GitHub からインストール

```bash
# Claude Code プロジェクトディレクトリで実行
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### 方法2：手動インストール

1. リポジトリをローカルにクローン：
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. `AK-Threads-booster` ディレクトリを Claude Code プロジェクトの `.claude/plugins/` にコピー：
   ```bash
   cp -r AK-Threads-booster /path/to/your/project/.claude/plugins/
   ```

3. Claude Code を再起動。Skill は自動的に検出されます。

### 他のツール

Cursor、Windsurf、Codex、GitHub Copilot を使用している場合は、リポジトリをプロジェクトディレクトリにクローンするだけです。各ツールが対応する設定ファイルを自動的に読み込みます。

---

## 初期化

初回使用前に、過去データをインポートする初期化を実行してください：

```
/setup
```

初期化では以下の手順を案内します：

1. **データインポート方法の選択**
   - Meta Threads API（自動取得）
   - Meta アカウントエクスポート（手動ダウンロード）
   - 既存のデータファイルを直接指定

2. **過去投稿の自動分析**。3つのファイルを生成：
   - `threads_daily_tracker.json` -- 過去投稿データベース
   - `style_guide.md` -- パーソナライズされたスタイルガイド（Hook の傾向、文字数範囲、結びのパターンなど）
   - `concept_library.md` -- コンセプトライブラリ（オーディエンスに既に説明した概念を追跡）

3. **分析レポート**。アカウントのスタイル特性とデータ概要を表示

初期化は一度だけ実行すれば十分です。以降のデータ更新は `/review` モジュールで継続的に蓄積されます。

---

## 7つの Skill

### 1. /setup -- 初期化

初回使用時に実行。過去投稿をインポートし、スタイルガイドを生成し、コンセプトライブラリを構築します。

```
/setup
```

### 2. /voice -- Brand Voice 構築

すべての過去投稿とコメント返信を深く分析し、包括的な Brand Voice プロファイルを構築します。`/setup` のスタイルガイドよりも詳細で、文体の傾向、トーンの変化、感情表現、ユーモアスタイル、避けるべき表現などの微細な特徴をカバーします。

```
/voice
```

Brand Voice が充実するほど、`/draft` の出力はあなたの実際の文体に近づきます。`/setup` 後に一度実行することを推奨します。

分析次元：文体構造の傾向、トーン変化パターン、感情表現スタイル、知識の提示方法、ファンと批判者に対するトーンの違い、よく使う比喩と例え、ユーモアスタイル、自称と読者への呼びかけ方、禁忌表現、段落リズムの微細特徴、コメント返信のトーン特性。

出力：`brand_voice.md`。`/draft` モジュールが自動的に参照します。

### 3. /analyze -- 投稿分析（コア機能）

投稿を書いた後、内容を貼り付けて4次元分析を実行：

```
/analyze

[投稿内容を貼り付け]
```

4つの分析次元：

- **スタイルマッチング**：あなた自身の過去スタイルと比較し、逸脱箇所と過去の実績を提示
- **心理学分析**：Hook メカニズム、感情の弧、シェア動機、信頼シグナル、認知バイアス、コメント誘発ポテンシャル
- **アルゴリズム対齐**：レッドラインスキャン（該当時は即警告）+ プラスシグナル評価
- **AI 臭検知**：文レベル、構造レベル、内容レベルでの AI 痕跡スキャン

### 4. /topics -- トピック推薦

次に何を書くべきか迷ったときに使用。コメントマイニングと過去データからトピックを推薦します。

```
/topics
```

3-5 個のトピックを推薦。それぞれに推薦根拠、データに基づく理由、類似過去投稿の実績、予測パフォーマンス範囲を付記。

### 5. /draft -- 下書き支援

トピックバンクからテーマを選び、Brand Voice に基づいて下書きを生成します。AK-Threads-Booster の AI ライティング支援として最も直接的な機能ですが、下書きはあくまで出発点です。

```
/draft [トピック]
```

トピックを指定することも、システムにトピックバンクから推薦させることもできます。下書きの品質は Brand Voice データの充実度に依存します。`/voice` を事前に実行しておくと明確な違いが出ます。

下書きは出発点です。自分で編集・調整してください。編集後に `/analyze` を実行することを推奨します。

### 6. /predict -- バズ予測

投稿を書いた後、公開後24時間の予測パフォーマンスを算出します。

```
/predict

[投稿内容を貼り付け]
```

保守的/基準/楽観的の3区間で予測（views / likes / replies / reposts / shares）。予測根拠と不確実性要因を併記。

### 7. /review -- 投稿後レビュー

公開後に使用。実際のパフォーマンスデータを回収し、予測と比較し、システムデータを更新します。

```
/review
```

実行内容：
- 実際のパフォーマンスデータを回収
- 予測との比較、乖離原因の分析
- tracker とスタイルガイドを更新
- 最適な投稿タイミングを提案

---

## ナレッジベース

AK-Threads-Booster には3つのナレッジベースが組み込まれており、分析の参考基準として使用されます。

### ソーシャルメディア心理学（psychology.md）

出典：学術研究の整理。Hook の心理的トリガーメカニズム、コメント誘発心理学、シェア動機と拡散メカニズム（STEPPS フレームワーク）、信頼構築（Pratfall Effect、Parasocial Relationship）、認知バイアス応用（Anchoring、Loss Aversion、Social Proof、IKEA Effect）、感情の弧と覚醒レベルをカバー。

用途：`/analyze` 心理学分析次元の理論基盤。心理学は分析レンズであり、ライティングルールではありません。

### Meta アルゴリズム（algorithm.md）

出典：Meta 特許文書、Facebook Papers、公式ポリシー声明、KOL 観察（補足のみ）。レッドラインリスト（12種のペナルティ対象行為）、ランキングシグナル（DM シェア、深いコメント、滞在時間など）、投稿後戦略、アカウントレベル戦略をカバー。

用途：`/analyze` アルゴリズム対齐チェックのルール基盤。レッドライン項目は該当時に警告、シグナル項目はアドバイザリートーンで提供。

### AI 臭検知（ai-detection.md）

文レベルの AI 痕跡（10種）、構造レベルの AI 痕跡（5種）、内容レベルの AI 痕跡（5種）、AI 臭低減方法（7種）、スキャントリガー条件、重大度定義をカバー。

用途：`/analyze` AI 臭スキャンの検知基準。AI 痕跡を特定し、あなた自身が修正できるようにします。自動修正は行いません。

---

## 典型的なワークフロー

```
1. /setup              -- 初回使用、システム初期化
2. /voice              -- Brand Voice を深く構築（一度実行）
3. /topics             -- トピック推薦を確認
4. /draft [トピック]   -- 下書きを生成
5. /analyze [投稿]     -- 下書きまたは自作投稿を分析
6. （分析に基づいて自分で調整）
7. /predict [投稿]     -- 公開前にパフォーマンスを予測
8. （公開）
9. /review             -- 公開24時間後にデータ回収
10. ステップ3に戻る
```

サイクルを重ねるごとに、システムの分析と予測の精度が向上します。`/voice` は一度だけ実行すれば十分です（投稿が増えた後に再実行して更新することも可能）。`/draft` は Brand Voice ファイルを自動参照します。

---

## よくある質問

**Q：AK-Threads-Booster は投稿を代筆しますか？**
`/draft` モジュールで初稿を生成できますが、初稿はあくまで出発点です。自分で編集・調整する必要があります。初稿の品質は Brand Voice データの充実度に依存します。他のモジュールは分析とアドバイスのみを行い、代筆はしません。

**Q：データが少ない段階での分析精度は？**
率直に言って高くありません。システムはそれを正直に伝えます。データの蓄積に伴い精度は向上します。

**Q：提案に必ず従う必要がありますか？**
いいえ。すべての提案はアドバイスであり、最終判断はあなたにあります。唯一の直接警告はアルゴリズムレッドライン（降格を引き起こす投稿パターン）です。

**Q：Threads 以外のプラットフォームに対応していますか？**
現在は主に Threads 向けに設計されています。ナレッジベースの心理学原理は汎用的ですが、アルゴリズムナレッジベースは Meta プラットフォームに特化しています。

**Q：一般的な AI ライティングツールとの違いは？**
一般的なツールは汎用モデルからコンテンツを生成します。AK-Threads-Booster の分析と提案はすべてあなた自身の過去データに基づいているため、ユーザーごとに結果が異なります。コンサルタントであり、代筆者ではありません。これがあなたのオーディエンスに合った Threads 戦略を構築する鍵です。

**Q：日本語の投稿でもスレッズ アルゴリズムの分析は有効ですか？**
はい。Meta のアルゴリズムの基本ロジック（エンゲージメントシグナル、レッドライン行為、ランキング要因）は言語に依存しません。心理学分析と AI 臭検知は日本語の文脈に適用できます。スタイルガイドはあなた自身の日本語投稿データから生成されるため、日本語特有の表現パターンも反映されます。

**Q：SNS 運用の AI ツールとして、スレッズ フォロワー 増やし方に直結しますか？**
AK-Threads-Booster はフォロワーを自動的に増やすツールではありません。各投稿のパフォーマンスを最適化するための分析と提案を行います。フォロワー増加は、良質なコンテンツの継続的な投稿の結果として得られるものです。

**Q：スレッズ 伸びる投稿を保証できますか？**
保証はできません。Threads のアルゴリズムは極めて複雑なシステムであり、バズ投稿を保証できるツールは存在しません。AK-Threads-Booster ができるのは、あなた自身の過去データに基づいてより良い判断を下し、既知のアルゴリズムレッドラインを回避し、心理学とデータ分析の観点から各投稿のパフォーマンス確率を向上させることです。現時点で最も包括的な Threads コンテンツ作成 Skill ですが、投稿がバズるかどうかを決定する要因（タイミング、トピックの関連性、オーディエンスの状態、その時点でのアルゴリズムの分配ロジック）は、いかなるツールでも完全にはコントロールできません。データコンサルタントとしてご活用ください。

---

## ディレクトリ構造

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

MIT License. [LICENSE](./LICENSE) を参照してください。
