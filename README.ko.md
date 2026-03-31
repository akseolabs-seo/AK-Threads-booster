[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

# AK-Threads-Booster

> **English Summary:** AK-Threads-booster is a Claude Code and Codex skill and AI writing assistant built specifically for Threads creators. This open-source Threads skill analyzes your historical post data, leverages social media psychology research and the Threads algorithm to provide personalized writing analysis, Brand Voice profiling, and draft assistance. Works as a skill / plugin for Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, and Google Antigravity.

Threads 크리에이터를 위해 설계된 데이터 기반 AI 라이팅 Skill. Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, Google Antigravity 지원. 당신의 과거 게시물 데이터, 소셜 미디어 심리학 연구, Meta의 스레드 알고리즘을 기반으로 맞춤형 글쓰기 분석, Brand Voice 구축, 초안 지원을 제공합니다.

한국에서 Threads는 Instagram과 함께 빠르게 성장하고 있습니다. 인스타그램에서 스레드로의 유입은 늘어나는데, 스레드에서 어떤 콘텐츠가 먹히는지, 스레드 알고리즘은 어떻게 작동하는지, 스레드 팔로워 늘리기의 핵심은 무엇인지 명확한 답을 가진 크리에이터는 많지 않습니다.

AK-Threads-Booster는 당신의 과거 데이터에서 답을 찾아줍니다. 범용 SNS 운영 템플릿이 아닙니다. 당신의 계정 데이터를 분석하고, 무엇이 효과적인지 파악하고, 그 이유를 심리학과 알고리즘 관점에서 설명하는 데이터 기반 컨설턴트 Skill입니다. Instagram과 Threads를 함께 운영하는 크리에이터를 위한 크로스 플랫폼 콘텐츠 전략도 데이터로 뒷받침합니다.

---

## AK-Threads-Booster란

AK-Threads-Booster는 오픈소스 Threads 게시물 Skill입니다. 글쓰기 템플릿도, 규칙 모음도, AI 대필 도구도 아닙니다.

바로 설치해서 쓸 수 있는 Skill 방법론 시스템이며, 핵심은 세 가지입니다:

1. **과거 데이터를 분석** 해서 당신의 계정에서 어떤 콘텐츠가 가장 높은 스레드 성장을 이끄는지 파악
2. **심리학과 스레드 알고리즘 지식을 분석 렌즈로 활용** 해서 왜 효과적인지 논리적으로 설명
3. **분석 결과를 투명하게 제시** 해서 다음 행동은 당신이 판단

사용자마다 다른 결과가 나옵니다. 오디언스, 글쓰기 스타일, 데이터가 다르기 때문입니다. 이것이 범용 템플릿과 데이터 기반 Threads 전략의 근본적인 차이입니다.

---

## 핵심 원칙

**컨설턴트이지, 선생님이 아닙니다.** AK-Threads-Booster는 "이렇게 쓰세요"라고 말하지 않습니다. "이전에 이렇게 썼을 때 데이터가 이랬습니다, 참고하세요"라고 전달합니다. 채점 없음, 교정 없음, 대필 없음.

**데이터 기반이지, 규칙 기반이 아닙니다.** 모든 제안은 당신의 과거 데이터에서 나옵니다. "SNS 마케팅 10대 법칙" 같은 범용 팁이 아닙니다. 데이터가 부족할 때는 솔직히 알려드립니다.

**레드라인만이 유일한 하드 규칙입니다.** Meta 알고리즘이 명시적으로 페널티를 주는 행위(engagement bait, clickbait, 고유사도 중복 게시 등)만 직접 경고합니다. 나머지 분석은 모두 참고용이며, 최종 결정은 당신에게 있습니다.

---

## 멀티 툴 지원

AK-Threads-Booster는 여러 AI 코딩 도구를 지원합니다. Claude Code에서는 7개 Skill을 모두 사용할 수 있고, 다른 도구에서는 핵심 분석 기능을 제공합니다.

### 지원 도구 및 설정 파일

| 도구 | 설정 파일 위치 | 기능 범위 |
|------|---------------|----------|
| **Claude Code** | `skills/` 디렉토리 (7 Skill) | 전체 기능: setup, voice, analyze, topics, draft, predict, review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | 핵심 분석 (4차원 분석) |
| **Codex** | `AGENTS.md` (루트) | 핵심 분석 (4차원 분석) |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | 핵심 분석 (4차원 분석) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | 핵심 분석 (4차원 분석) |
| **Google Antigravity** | `.agents/` 디렉토리 + 루트 `AGENTS.md` | 핵심 분석 (4차원 분석) |

### 기능 차이

- **Claude Code**: 전체 기능 포함. 초기화(setup), Brand Voice 구축(voice), 글쓰기 분석(analyze), 주제 추천(topics), 초안 지원(draft), 바이럴 예측(predict), 게시 후 리뷰(review) 7개 독립 Skill
- **다른 도구**: 핵심 글쓰기 분석 기능 (스타일 매칭, 심리학 분석, 알고리즘 정렬 체크, AI 톤 감지) 4차원 분석. 동일한 지식 베이스(`knowledge/` 디렉토리) 공유
- **Google Antigravity**: 루트 `AGENTS.md`(컨설턴트 규범 및 레드라인 규칙)와 `.agents/` 디렉토리(rules + skills) 동시 로드

모든 도구 버전에 포함:
- 컨설턴트 톤 가이드라인 (채점 없음, 교정 없음, 대필 없음)
- 알고리즘 레드라인 규칙 (해당 시 즉시 경고)
- 지식 베이스 참조 (심리학, 알고리즘, AI 톤 감지)

---

## 설치 방법

### 방법 1: GitHub에서 설치

```bash
# Claude Code 프로젝트 디렉토리에서
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### 방법 2: 수동 설치

1. 리포지토리를 로컬에 클론:
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. `AK-Threads-booster` 디렉토리를 Claude Code 프로젝트의 `.claude/plugins/`에 복사:
   ```bash
   cp -r AK-Threads-booster /path/to/your/project/.claude/plugins/
   ```

3. Claude Code 재시작. Skill이 자동으로 감지됩니다.

### 다른 도구

Cursor, Windsurf, Codex, GitHub Copilot을 사용한다면 리포지토리를 프로젝트 디렉토리에 클론하면 됩니다. 각 도구가 해당 설정 파일을 자동으로 읽어들입니다.

---

## 초기화

첫 사용 전에 과거 데이터를 가져오는 초기화를 실행하세요:

```
/setup
```

초기화 과정에서 안내하는 내용:

1. **데이터 가져오기 방법 선택**
   - Meta Threads API (자동 수집)
   - Meta 계정 내보내기 (수동 다운로드)
   - 기존 데이터 파일 직접 제공

2. **과거 게시물 자동 분석**. 3개 파일 생성:
   - `threads_daily_tracker.json` -- 과거 게시물 데이터베이스
   - `style_guide.md` -- 맞춤형 스타일 가이드 (Hook 선호도, 글자 수 범위, 마무리 패턴 등)
   - `concept_library.md` -- 개념 라이브러리 (오디언스에게 이미 설명한 개념 추적)

3. **분석 리포트**. 계정의 스타일 특성과 데이터 개요 확인

초기화는 한 번만 실행하면 됩니다. 이후 데이터 업데이트는 `/review` 모듈로 지속적으로 축적됩니다.

---

## 7개 Skill

### 1. /setup -- 초기화

첫 사용 시 실행. 과거 게시물을 가져오고, 스타일 가이드를 생성하고, 개념 라이브러리를 구축합니다.

```
/setup
```

### 2. /voice -- Brand Voice 구축

모든 과거 게시물과 댓글 답변을 심층 분석해서 포괄적인 Brand Voice 프로필을 구축합니다. `/setup`의 스타일 가이드보다 더 깊이 있으며, 문체 선호도, 톤 변화, 감정 표현, 유머 스타일, 금기어 등 미세한 특징까지 다룹니다.

```
/voice
```

Brand Voice가 충실할수록 `/draft`의 결과물이 실제 글쓰기 스타일에 가까워집니다. `/setup` 이후에 한 번 실행하는 걸 추천합니다.

분석 차원: 문체 구조 선호도, 톤 전환 패턴, 감정 표현 방식, 지식 전달 방식, 팬 vs 안티에 대한 톤 차이, 자주 쓰는 비유와 메타포, 유머 스타일, 자칭과 독자 호칭, 금기어, 문단 리듬 미세 특징, 댓글 답변 톤 특성.

산출물: `brand_voice.md`. `/draft` 모듈이 자동 참조합니다.

### 3. /analyze -- 글쓰기 분석 (핵심 기능)

게시물 작성 후 내용을 붙여넣어 4차원 분석을 실행:

```
/analyze

[게시물 내용 붙여넣기]
```

4개 분석 차원:

- **스타일 매칭**: 자신의 과거 스타일과 비교, 이탈 지점과 과거 성과 표시
- **심리학 분석**: Hook 메커니즘, 감정 곡선, 공유 동기, 신뢰 시그널, 인지 편향, 댓글 유발 잠재력
- **알고리즘 정렬**: 레드라인 스캔 (해당 시 즉시 경고) + 긍정 시그널 평가
- **AI 톤 감지**: 문장 수준, 구조 수준, 콘텐츠 수준의 AI 흔적 스캔

### 4. /topics -- 주제 추천

다음에 뭘 쓸지 모를 때 사용. 댓글 마이닝과 과거 데이터에서 주제를 추천합니다.

```
/topics
```

3-5개 주제 추천. 각각 추천 근거, 데이터 기반 이유, 유사 과거 게시물 성과, 예상 성과 범위 포함.

### 5. /draft -- 초안 지원

주제 뱅크에서 토픽을 선택하고 Brand Voice 기반으로 초안을 생성합니다. AK-Threads-Booster의 AI 콘텐츠 제작 기능 중 가장 직접적이지만, 초안은 시작점일 뿐입니다.

```
/draft [주제]
```

주제를 지정하거나 시스템이 주제 뱅크에서 추천하게 할 수 있습니다. 초안 품질은 Brand Voice 데이터의 완성도에 좌우됩니다. `/voice`를 먼저 실행하면 확연한 차이가 있습니다.

초안은 시작점입니다. 직접 편집하고 조정해야 합니다. 편집 후 `/analyze` 실행을 추천합니다.

### 6. /predict -- 바이럴 예측

게시물 작성 후 게시 24시간 후의 성과를 예측합니다.

```
/predict

[게시물 내용 붙여넣기]
```

보수적/기준/낙관적 3구간 예측 (views / likes / replies / reposts / shares). 예측 근거와 불확실성 요인 함께 제시.

### 7. /review -- 게시 후 리뷰

게시 후 실제 성과 데이터를 수집하고 예측과 비교하고 시스템 데이터를 업데이트합니다.

```
/review
```

수행 내용:
- 실제 성과 데이터 수집
- 예측과 비교, 편차 원인 분석
- tracker와 스타일 가이드 업데이트
- 최적 게시 시간 제안

---

## 지식 베이스

AK-Threads-Booster에는 3개의 지식 베이스가 내장되어 있으며, 분석의 참조 기준으로 사용됩니다.

### 소셜 미디어 심리학 (psychology.md)

출처: 학술 연구 정리. Hook 심리적 트리거 메커니즘, 댓글 유발 심리학, 공유 동기와 확산 메커니즘(STEPPS 프레임워크), 신뢰 구축(Pratfall Effect, Parasocial Relationship), 인지 편향 활용(Anchoring, Loss Aversion, Social Proof, IKEA Effect), 감정 곡선과 각성 수준 포함.

용도: `/analyze` 심리학 분석 차원의 이론적 기반. 심리학은 분석 렌즈이지 글쓰기 규칙이 아닙니다.

### Meta 알고리즘 (algorithm.md)

출처: Meta 특허 문서, Facebook Papers, 공식 정책 성명, KOL 관찰(보충용). 레드라인 리스트(12가지 페널티 행위), 랭킹 시그널(DM 공유, 깊은 댓글, 체류 시간 등), 게시 후 전략, 계정 수준 전략 포함.

용도: `/analyze` 알고리즘 정렬 체크의 규칙 기반. 레드라인 항목은 해당 시 경고, 시그널 항목은 어드바이저리 톤으로 제공.

### AI 톤 감지 (ai-detection.md)

문장 수준 AI 흔적(10종), 구조 수준 AI 흔적(5종), 콘텐츠 수준 AI 흔적(5종), AI 톤 저감 방법(7종), 스캔 트리거 조건, 심각도 정의 포함.

용도: `/analyze` AI 톤 스캔의 감지 기준. AI 흔적을 식별하여 직접 수정할 수 있게 합니다. 자동 수정은 하지 않습니다.

---

## 일반적인 워크플로우

```
1. /setup              -- 첫 사용, 시스템 초기화
2. /voice              -- Brand Voice 심층 구축 (한 번 실행)
3. /topics             -- 주제 추천 확인
4. /draft [주제]       -- 초안 생성
5. /analyze [게시물]   -- 초안 또는 직접 작성한 게시물 분석
6. (분석을 바탕으로 직접 수정)
7. /predict [게시물]   -- 게시 전 성과 예측
8. (게시)
9. /review             -- 게시 24시간 후 데이터 수집
10. 3단계로 돌아가기
```

사이클을 반복할수록 시스템의 분석과 예측 정확도가 올라갑니다. `/voice`는 한 번만 실행하면 됩니다(게시물이 쌓인 후 다시 실행하여 업데이트 가능). `/draft`는 Brand Voice 파일을 자동으로 참조합니다.

---

## 자주 묻는 질문

**Q: AK-Threads-Booster가 게시물을 대신 써주나요?**
`/draft` 모듈로 초안을 생성할 수 있지만, 초안은 시작점일 뿐입니다. 직접 편집하고 다듬어야 합니다. 초안 품질은 Brand Voice 데이터의 완성도에 따라 달라집니다. 다른 모듈은 분석과 조언만 하며, 대필하지 않습니다.

**Q: 데이터가 적을 때 분석이 정확한가요?**
솔직히 정확도가 높지 않습니다. 시스템이 그 점을 솔직하게 알려줍니다. 데이터가 쌓일수록 정확해집니다.

**Q: 제안을 반드시 따라야 하나요?**
아닙니다. 모든 제안은 참고용이며 최종 결정은 당신에게 있습니다. 유일한 직접 경고는 알고리즘 레드라인(강등을 유발하는 패턴)뿐입니다.

**Q: Threads 외 다른 플랫폼도 지원하나요?**
현재 주로 Threads용으로 설계되었습니다. 지식 베이스의 심리학 원리는 범용적이지만, 알고리즘 지식 베이스는 Meta 플랫폼에 특화되어 있습니다.

**Q: 일반 AI 글쓰기 도구와 뭐가 다른가요?**
일반 도구는 범용 모델에서 콘텐츠를 생성합니다. AK-Threads-Booster의 분석과 제안은 모두 당신의 과거 데이터에 기반하기 때문에 사용자마다 결과가 다릅니다. 컨설턴트이지 대필자가 아닙니다. 당신의 오디언스에 맞는 Threads 전략을 세우는 핵심입니다.

**Q: Instagram에서 Threads로의 크로스 플랫폼 전략에도 도움이 되나요?**
AK-Threads-Booster는 Threads 게시물 분석에 특화되어 있지만, 과거 데이터 분석을 통해 어떤 유형의 콘텐츠가 Threads에서 잘 되는지 파악할 수 있습니다. Instagram 콘텐츠를 Threads용으로 변환할 때 어떤 요소를 조정해야 하는지 데이터가 보여줍니다.

**Q: SNS AI 도구로서 스레드 팔로워 늘리기에 직접적인 효과가 있나요?**
AK-Threads-Booster는 팔로워를 자동으로 늘려주는 도구가 아닙니다. 각 게시물의 성과를 최적화하기 위한 분석과 제안을 합니다. 팔로워 성장은 양질의 콘텐츠를 꾸준히 게시한 결과입니다.

**Q: 이걸 쓰면 스레드 성장이 보장되나요?**
보장은 없습니다. Threads의 알고리즘은 매우 복잡한 시스템이며, 바이럴을 보장할 수 있는 도구는 없습니다. AK-Threads-Booster가 하는 일은 당신의 과거 데이터를 기반으로 더 나은 판단을 내리고, 알려진 알고리즘 레드라인을 피하고, 심리학과 데이터 분석 관점에서 각 게시물의 성과 확률을 높이는 것입니다. 현재 가장 포괄적인 Threads 콘텐츠 제작 Skill이지만, 게시물의 바이럴 여부를 결정하는 요인(타이밍, 주제 관련성, 오디언스 상태, 그 시점의 알고리즘 배분 로직)은 어떤 도구로도 완전히 통제할 수 없습니다. 데이터 컨설턴트로 활용하세요.

---

## 디렉토리 구조

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

MIT License. [LICENSE](./LICENSE) 참조.
