[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

# AK-Threads-Booster

> **English Summary:** AK-Threads-booster is a Claude Code and Codex skill and AI writing assistant built specifically for Threads creators. This open-source Threads skill analyzes your historical post data, leverages social media psychology research and the Threads algorithm to provide personalized writing analysis, Brand Voice profiling, and draft assistance. Works as a skill / plugin for Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, and Google Antigravity.

AI Skill dựa trên dữ liệu, thiết kế riêng cho creator Threads. Hỗ trợ Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, Google Antigravity. Phân tích dữ liệu bài đăng lịch sử của bạn, sử dụng nghiên cứu tâm lý mạng xã hội và thuật toán Threads để cung cấp phân tích viết bài cá nhân hóa, xây dựng Brand Voice và hỗ trợ soạn nháp.

Threads đang phát triển nhanh tại Việt Nam, đặc biệt trong nhóm người dùng trẻ. Nhiều creator bắt đầu xây dựng kênh Threads nhưng vẫn đang tìm câu trả lời cho những câu hỏi cơ bản: thuật toán Threads hoạt động như thế nào, làm sao để tăng follow Threads từ con số 0, nội dung kiểu gì thì được đẩy, và chiến lược nội dung nên bắt đầu từ đâu.

AK-Threads-Booster trả lời những câu hỏi đó từ chính dữ liệu của bạn. Không phải template chung chung. Không phải mẹo Threads copy từ internet. Đây là hệ thống tư vấn dựa trên dữ liệu, phân tích tài khoản của bạn, tìm ra cái gì hiệu quả, và giải thích lý do từ góc nhìn tâm lý học và thuật toán. Nếu bạn đang tìm một công cụ AI viết bài thực sự học từ dữ liệu của bạn, đây là công cụ đó.

---

## AK-Threads-Booster là gì

AK-Threads-Booster là open-source Threads Skill. Không phải template viết bài, không phải bộ quy tắc, không phải AI viết thay bạn.

Là hệ thống Skill cài đặt và dùng ngay, làm 3 việc chính:

1. **Phân tích dữ liệu lịch sử của bạn** để tìm ra loại nội dung nào mang lại engagement cao nhất trên tài khoản của bạn
2. **Dùng tâm lý học và kiến thức thuật toán Threads làm lăng kính phân tích** để giải thích tại sao nội dung đó hiệu quả
3. **Trình bày kết quả phân tích minh bạch** để bạn tự quyết định bước tiếp theo

Mỗi người dùng nhận kết quả khác nhau vì đối tượng, phong cách viết và dữ liệu mỗi người khác nhau. Đây là sự khác biệt cốt lõi giữa template chung và chiến lược Threads dựa trên dữ liệu.

---

## Nguyên tắc cốt lõi

**Tư vấn viên, không phải giáo viên.** AK-Threads-Booster không nói "bạn nên viết thế này." Nó nói "lần trước bạn viết kiểu này, dữ liệu ra thế này, tham khảo nhé." Không chấm điểm, không sửa bài, không viết thay.

**Dựa trên dữ liệu, không dựa trên quy tắc.** Mọi đề xuất đều đến từ dữ liệu lịch sử của chính bạn, không phải "10 mẹo marketing mạng xã hội" chung chung. Khi dữ liệu chưa đủ, hệ thống sẽ nói thẳng thay vì giả vờ tự tin.

**Red line là quy tắc cứng duy nhất.** Chỉ những hành vi bị thuật toán Meta phạt rõ ràng (engagement bait, clickbait, đăng lại nội dung tương tự cao, v.v.) mới bị cảnh báo trực tiếp. Tất cả phân tích khác chỉ mang tính tham khảo. Bạn luôn có quyền quyết định cuối cùng.

---

## Hỗ trợ nhiều công cụ

AK-Threads-Booster hoạt động với nhiều AI coding tool. Claude Code cung cấp đầy đủ 7 Skill, các công cụ khác cung cấp khả năng phân tích cốt lõi.

### Công cụ được hỗ trợ và file cấu hình

| Công cụ | Vị trí file cấu hình | Phạm vi tính năng |
|---------|----------------------|-------------------|
| **Claude Code** | `skills/` directory (7 Skill) | Đầy đủ: setup, voice, analyze, topics, draft, predict, review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | Phân tích cốt lõi (4 chiều) |
| **Codex** | `AGENTS.md` (root) | Phân tích cốt lõi (4 chiều) |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | Phân tích cốt lõi (4 chiều) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Phân tích cốt lõi (4 chiều) |
| **Google Antigravity** | `.agents/` directory + root `AGENTS.md` | Phân tích cốt lõi (4 chiều) |

### Khác biệt tính năng

- **Claude Code**: Đầy đủ tính năng gồm khởi tạo (setup), xây dựng Brand Voice (voice), phân tích bài viết (analyze), gợi ý chủ đề (topics), hỗ trợ nháp (draft), dự đoán viral (predict), và review sau đăng bài (review) -- bảy Skill độc lập
- **Công cụ khác**: Phân tích viết bài cốt lõi 4 chiều (so khớp phong cách, phân tích tâm lý, kiểm tra alignment thuật toán, phát hiện tone AI), dùng chung knowledge base (`knowledge/` directory)
- **Google Antigravity**: Đọc cả root `AGENTS.md` (quy chuẩn tư vấn và quy tắc red line) và `.agents/` directory (rules + skills)

Tất cả phiên bản đều bao gồm:
- Hướng dẫn giọng tư vấn (không chấm điểm, không sửa bài, không viết thay)
- Quy tắc red line thuật toán (cảnh báo ngay khi phát hiện)
- Tham chiếu knowledge base (tâm lý học, thuật toán, phát hiện tone AI)

---

## Cách cài đặt

### Cách 1: Cài qua GitHub

```bash
# Trong thư mục dự án Claude Code của bạn
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### Cách 2: Cài thủ công

1. Clone repo về máy:
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. Copy thư mục `AK-Threads-booster` vào `.claude/plugins/` của dự án Claude Code:
   ```bash
   cp -r AK-Threads-booster /path/to/your/project/.claude/plugins/
   ```

3. Khởi động lại Claude Code. Skill sẽ được phát hiện tự động.

### Công cụ khác

Nếu bạn dùng Cursor, Windsurf, Codex hoặc GitHub Copilot, chỉ cần clone repo vào thư mục dự án. Mỗi công cụ sẽ tự động đọc file cấu hình tương ứng.

---

## Khởi tạo

Trước khi dùng lần đầu, chạy khởi tạo để import dữ liệu lịch sử:

```
/setup
```

Quá trình khởi tạo hướng dẫn bạn qua:

1. **Chọn phương thức import dữ liệu**
   - Meta Threads API (lấy tự động)
   - Meta account export (tải thủ công)
   - Cung cấp file dữ liệu có sẵn

2. **Tự động phân tích bài đăng lịch sử**, tạo 3 file:
   - `threads_daily_tracker.json` -- Database bài đăng lịch sử
   - `style_guide.md` -- Hướng dẫn phong cách cá nhân (xu hướng Hook, khoảng số từ, mẫu kết bài, v.v.)
   - `concept_library.md` -- Thư viện khái niệm (theo dõi các khái niệm bạn đã giải thích cho audience)

3. **Báo cáo phân tích** cho thấy đặc điểm phong cách tài khoản và tổng quan dữ liệu

Khởi tạo chỉ cần chạy một lần. Cập nhật dữ liệu sau đó tích lũy qua module `/review`.

---

## Bảy Skill

### 1. /setup -- Khởi tạo

Chạy lần đầu sử dụng. Import bài đăng lịch sử, tạo hướng dẫn phong cách, xây dựng thư viện khái niệm.

```
/setup
```

Đây là bước quan trọng nhất cho người mới bắt đầu. Hệ thống cần dữ liệu của bạn để hoạt động, và `/setup` là cách nhanh nhất để bắt đầu.

### 2. /voice -- Xây dựng Brand Voice

Phân tích sâu tất cả bài đăng lịch sử và reply comment để xây dựng hồ sơ Brand Voice toàn diện. Chi tiết hơn hướng dẫn phong cách từ `/setup`, bao gồm xu hướng cấu trúc câu, chuyển đổi giọng, biểu đạt cảm xúc, phong cách hài hước, từ ngữ cần tránh và các đặc điểm vi mô khác.

```
/voice
```

Brand Voice càng đầy đủ, output của `/draft` càng giống phong cách viết thật của bạn. Nên chạy sau `/setup`.

Chiều phân tích: xu hướng cấu trúc câu, mẫu chuyển đổi giọng, cách biểu đạt cảm xúc, cách trình bày kiến thức, khác biệt giọng với fan vs người chỉ trích, ẩn dụ hay dùng, phong cách hài hước, cách xưng hô, từ ngữ cấm kỵ, nhịp đoạn văn, đặc điểm giọng reply comment.

Output: `brand_voice.md`, được module `/draft` tự động tham chiếu.

### 3. /analyze -- Phân tích bài viết (Tính năng cốt lõi)

Sau khi viết bài, dán nội dung để phân tích 4 chiều:

```
/analyze

[dán nội dung bài đăng]
```

4 chiều phân tích:

- **So khớp phong cách**: So sánh với phong cách lịch sử của chính bạn, đánh dấu điểm lệch và hiệu suất lịch sử
- **Phân tích tâm lý**: Cơ chế Hook, đường cong cảm xúc, động lực chia sẻ, tín hiệu tin cậy, thiên kiến nhận thức, tiềm năng kích hoạt comment
- **Alignment thuật toán**: Quét red line (cảnh báo ngay khi phát hiện) + đánh giá tín hiệu tích cực
- **Phát hiện tone AI**: Quét dấu vết AI ở cấp câu, cấu trúc và nội dung

### 4. /topics -- Gợi ý chủ đề

Khi không biết viết gì tiếp. Khai thác insight từ comment và dữ liệu lịch sử để gợi ý chủ đề.

```
/topics
```

Gợi ý 3-5 chủ đề, mỗi chủ đề kèm: nguồn gợi ý, lý do dựa trên dữ liệu, hiệu suất bài đăng lịch sử tương tự, khoảng hiệu suất dự kiến.

### 5. /draft -- Hỗ trợ soạn nháp

Chọn chủ đề từ topic bank và tạo nháp dựa trên Brand Voice của bạn. Đây là tính năng AI viết bài trực tiếp nhất của AK-Threads-Booster, nhưng bản nháp chỉ là điểm khởi đầu.

```
/draft [chủ đề]
```

Có thể chỉ định chủ đề hoặc để hệ thống gợi ý từ topic bank. Chất lượng nháp phụ thuộc vào độ đầy đủ của dữ liệu Brand Voice. Chạy `/voice` trước sẽ tạo ra khác biệt rõ rệt.

Bản nháp là điểm khởi đầu. Bạn cần chỉnh sửa và điều chỉnh. Sau khi chỉnh, nên chạy `/analyze`.

### 6. /predict -- Dự đoán viral

Sau khi viết bài, ước tính hiệu suất 24 giờ sau khi đăng.

```
/predict

[dán nội dung bài đăng]
```

Đưa ra ước tính conservative / baseline / optimistic (views / likes / replies / reposts / shares) kèm căn cứ và yếu tố bất định.

### 7. /review -- Review sau đăng bài

Sau khi đăng, dùng để thu thập dữ liệu hiệu suất thực tế, so sánh với dự đoán và cập nhật dữ liệu hệ thống.

```
/review
```

Những gì thực hiện:
- Thu thập dữ liệu hiệu suất thực tế
- So sánh với dự đoán, phân tích nguyên nhân chênh lệch
- Cập nhật tracker và hướng dẫn phong cách
- Đề xuất thời gian đăng bài tối ưu

---

## Knowledge Base

AK-Threads-Booster tích hợp 3 knowledge base, dùng làm cơ sở tham chiếu cho phân tích:

### Tâm lý mạng xã hội (psychology.md)

Nguồn: Tổng hợp nghiên cứu học thuật. Bao gồm cơ chế kích hoạt tâm lý Hook, tâm lý kích hoạt comment, động lực chia sẻ và cơ chế lan truyền (framework STEPPS), xây dựng niềm tin (Pratfall Effect, Parasocial Relationship), ứng dụng thiên kiến nhận thức (Anchoring, Loss Aversion, Social Proof, IKEA Effect), đường cong cảm xúc và mức độ kích thích.

Mục đích: Nền tảng lý thuyết cho chiều phân tích tâm lý trong `/analyze`. Tâm lý học là lăng kính phân tích, không phải quy tắc viết bài.

### Thuật toán Meta (algorithm.md)

Nguồn: Tài liệu bằng sáng chế Meta, Facebook Papers, tuyên bố chính sách chính thức, quan sát KOL (bổ sung). Bao gồm danh sách red line (12 hành vi bị phạt), tín hiệu xếp hạng (chia sẻ qua DM, comment sâu, thời gian ở lại, v.v.), chiến lược sau đăng bài, chiến lược cấp tài khoản.

Mục đích: Nền tảng quy tắc cho kiểm tra alignment thuật toán trong `/analyze`. Mục red line phát hiện là cảnh báo ngay; mục tín hiệu trình bày dạng tư vấn.

### Phát hiện tone AI (ai-detection.md)

Bao gồm dấu vết AI cấp câu (10 loại), dấu vết AI cấp cấu trúc (5 loại), dấu vết AI cấp nội dung (5 loại), phương pháp giảm tone AI (7 loại), điều kiện kích hoạt quét, định nghĩa mức độ nghiêm trọng.

Mục đích: Cơ sở phát hiện cho quét tone AI trong `/analyze`. Đánh dấu dấu vết AI để bạn tự sửa; không tự động sửa.

---

## Quy trình sử dụng

```
1. /setup              -- Lần đầu sử dụng, khởi tạo hệ thống
2. /voice              -- Xây dựng Brand Voice sâu (chạy một lần)
3. /topics             -- Xem gợi ý chủ đề
4. /draft [chủ đề]     -- Tạo bản nháp
5. /analyze [bài đăng]  -- Phân tích nháp hoặc bài tự viết
6. (Chỉnh sửa theo phân tích)
7. /predict [bài đăng]  -- Ước tính hiệu suất trước khi đăng
8. (Đăng bài)
9. /review             -- Thu thập dữ liệu 24h sau đăng
10. Quay lại bước 3
```

Mỗi vòng lặp giúp phân tích và dự đoán của hệ thống chính xác hơn. `/voice` chỉ cần chạy một lần (hoặc chạy lại sau khi có thêm bài đăng). `/draft` tự động tham chiếu file Brand Voice.

---

## Câu hỏi thường gặp

**Q: AK-Threads-Booster có viết bài thay tôi không?**
Module `/draft` tạo bản nháp, nhưng nháp chỉ là điểm khởi đầu. Bạn cần chỉnh sửa và hoàn thiện. Chất lượng nháp phụ thuộc vào độ đầy đủ của dữ liệu Brand Voice. Các module khác chỉ phân tích và tư vấn, không viết thay.

**Q: Dữ liệu ít thì phân tích có chính xác không?**
Nói thẳng là chưa chính xác lắm. Hệ thống sẽ nói thẳng điều đó. Độ chính xác tăng khi dữ liệu tích lũy nhiều hơn.

**Q: Có bắt buộc làm theo đề xuất không?**
Không. Mọi đề xuất chỉ mang tính tham khảo. Bạn luôn có quyền quyết định cuối cùng. Cảnh báo trực tiếp duy nhất là cho red line thuật toán (mẫu viết bị giảm reach).

**Q: Có hỗ trợ nền tảng khác ngoài Threads không?**
Hiện tại thiết kế chủ yếu cho Threads. Nguyên lý tâm lý trong knowledge base là phổ quát, nhưng knowledge base thuật toán tập trung vào nền tảng Meta.

**Q: Khác gì so với công cụ AI viết bài thông thường?**
Công cụ thông thường tạo nội dung từ model chung. Phân tích và đề xuất của AK-Threads-Booster đều đến từ dữ liệu lịch sử của chính bạn, nên mỗi người dùng nhận kết quả khác nhau. Đây là tư vấn viên, không phải người viết thuê. Đó là chìa khóa để xây dựng chiến lược Threads phù hợp với audience của bạn.

**Q: Phù hợp cho người mới bắt đầu trên Threads không?**
Rất phù hợp. `/setup` giúp bạn khởi tạo nhanh chóng, và `/voice` xây dựng Brand Voice ngay cả khi bạn mới có ít bài đăng. Hệ thống sẽ thẳng thắn cho biết khi dữ liệu chưa đủ để đưa ra phân tích chính xác, nhưng vẫn cung cấp hướng dẫn dựa trên kiến thức tâm lý học và thuật toán.

**Q: Làm sao để tăng follow Threads với công cụ này?**
AK-Threads-Booster không phải công cụ tăng follow tự động. Nó phân tích và đề xuất để mỗi bài đăng có cơ hội đạt hiệu suất tốt hơn. Tăng follow là kết quả của việc đăng nội dung chất lượng một cách nhất quán.

**Q: Dùng rồi có đảm bảo bài đăng viral không?**
Không đảm bảo. Thuật toán Threads là hệ thống cực kỳ phức tạp, không có công cụ nào đảm bảo bài đăng viral. AK-Threads-Booster giúp bạn đưa ra quyết định tốt hơn dựa trên dữ liệu lịch sử, tránh red line thuật toán đã biết, và tăng xác suất mỗi bài đăng đạt hiệu suất tốt qua phân tích tâm lý và dữ liệu. Đây là Threads content creation Skill toàn diện nhất hiện có, nhưng các yếu tố quyết định bài đăng có viral hay không -- thời điểm, độ liên quan của chủ đề, trạng thái audience, logic phân phối của thuật toán lúc đó -- quá nhiều để bất kỳ công cụ nào kiểm soát hoàn toàn. Hãy dùng như tư vấn viên dữ liệu, không phải máy đảm bảo viral.

---

## Cấu trúc thư mục

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

MIT License. Xem [LICENSE](./LICENSE).
