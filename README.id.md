[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

# AK-Threads-Booster

> **English Summary:** AK-Threads-booster is a Claude Code and Codex skill and AI writing assistant built specifically for Threads creators. This open-source Threads skill analyzes your historical post data, leverages social media psychology research and the Threads algorithm to provide personalized writing analysis, Brand Voice profiling, and draft assistance. Works as a skill / plugin for Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, and Google Antigravity.

AI Skill berbasis data yang dirancang khusus untuk kreator Threads. Mendukung Claude Code, Cursor, Codex, Windsurf, GitHub Copilot, Google Antigravity. Menganalisis data postingan historis kamu, memanfaatkan riset psikologi media sosial dan algoritma Threads untuk memberikan analisis tulisan yang dipersonalisasi, membangun Brand Voice, dan bantuan pembuatan draft.

Indonesia adalah pasar Threads terbesar di Asia Tenggara. Komunitas di sini aktif, suka berinteraksi, dan gaya kontennya beragam. Tapi pertanyaan yang masih sering muncul di kalangan kreator: bagaimana cara menambah followers Threads secara organik, bagaimana algoritma Threads bekerja, konten seperti apa yang bisa menembus keramaian, dan bagaimana meningkatkan engagement rate.

AK-Threads-Booster menjawab pertanyaan-pertanyaan itu dari data kamu sendiri. Bukan template generik dari internet. Bukan tips Threads yang sama untuk semua orang. Ini adalah sistem konsultan berbasis data yang menganalisis akun kamu, menemukan apa yang berhasil, dan menjelaskan alasannya dari sudut pandang psikologi dan algoritma. Kalau kamu sedang mencari AI konten kreator yang benar-benar belajar dari data kamu, alat ini dibuat untuk itu.

---

## Apa Itu AK-Threads-Booster

AK-Threads-Booster adalah open-source Threads Skill. Bukan template penulisan, bukan kumpulan aturan, bukan AI yang menulis menggantikan kamu.

Sistem Skill yang bisa langsung diinstal dan dipakai, dengan tiga fungsi inti:

1. **Menganalisis data historis kamu** untuk menemukan konten apa yang mendapatkan engagement tertinggi di akunmu
2. **Menggunakan psikologi dan pengetahuan algoritma Threads sebagai lensa analisis** untuk menjelaskan mengapa konten tertentu berhasil
3. **Menyajikan hasil analisis secara transparan** sehingga kamu sendiri yang menentukan langkah selanjutnya

Setiap pengguna mendapatkan hasil yang berbeda karena audiens, gaya penulisan, dan data masing-masing berbeda. Inilah perbedaan mendasar antara template generik dan strategi Threads berbasis data.

---

## Prinsip Inti

**Konsultan, bukan guru.** AK-Threads-Booster tidak akan bilang "kamu harus menulis seperti ini." Yang dilakukan adalah menyampaikan "waktu kamu menulis seperti ini sebelumnya, datanya seperti ini, untuk referensi." Tidak ada penilaian, tidak ada koreksi, tidak ada ghostwriting.

**Berbasis data, bukan berbasis aturan.** Semua saran berasal dari data historis kamu sendiri, bukan dari daftar "10 Tips Marketing Media Sosial" yang generik. Kalau data belum cukup, sistem akan memberitahu dengan jujur.

**Red line adalah satu-satunya aturan keras.** Hanya perilaku yang secara eksplisit dikenai penalti oleh algoritma Meta (engagement bait, clickbait, repost dengan kemiripan tinggi, dll.) yang akan mendapat peringatan langsung. Semua analisis lainnya bersifat rekomendasi. Kamu selalu punya keputusan akhir.

---

## Dukungan Multi-Tool

AK-Threads-Booster bekerja dengan berbagai AI coding tool. Claude Code memberikan pengalaman lengkap 7 Skill, sementara tool lain menyediakan kemampuan analisis inti.

### Tool yang Didukung dan File Konfigurasi

| Tool | Lokasi File Konfigurasi | Cakupan Fitur |
|------|------------------------|---------------|
| **Claude Code** | `skills/` directory (7 Skill) | Fitur lengkap: setup, voice, analyze, topics, draft, predict, review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | Analisis inti (4 dimensi) |
| **Codex** | `AGENTS.md` (root) | Analisis inti (4 dimensi) |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | Analisis inti (4 dimensi) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Analisis inti (4 dimensi) |
| **Google Antigravity** | `.agents/` directory + root `AGENTS.md` | Analisis inti (4 dimensi) |

### Perbedaan Fitur

- **Claude Code**: Fitur lengkap termasuk inisialisasi (setup), pembuatan Brand Voice (voice), analisis tulisan (analyze), rekomendasi topik (topics), bantuan draft (draft), prediksi viral (predict), dan review pasca-posting (review) -- tujuh Skill independen
- **Tool lain**: Analisis tulisan inti dengan empat dimensi (pencocokan gaya, analisis psikologi, pengecekan alignment algoritma, deteksi tone AI), berbagi knowledge base yang sama (`knowledge/` directory)
- **Google Antigravity**: Membaca root `AGENTS.md` (norma konsultan dan aturan red line) dan `.agents/` directory (rules + skills)

Semua versi tool mencakup:
- Pedoman tone konsultan (tidak menilai, tidak mengoreksi, tidak ghostwriting)
- Aturan red line algoritma (langsung peringatan saat terdeteksi)
- Referensi knowledge base (psikologi, algoritma, deteksi tone AI)

---

## Cara Instalasi

### Opsi 1: Instal via GitHub

```bash
# Di directory proyek Claude Code kamu
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### Opsi 2: Instalasi Manual

1. Clone repo ini ke lokal:
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. Salin directory `AK-Threads-booster` ke `.claude/plugins/` di proyek Claude Code kamu:
   ```bash
   cp -r AK-Threads-booster /path/to/your/project/.claude/plugins/
   ```

3. Restart Claude Code. Skill akan terdeteksi secara otomatis.

### Tool Lain

Kalau kamu menggunakan Cursor, Windsurf, Codex, atau GitHub Copilot, cukup clone repo ke directory proyek kamu. Setiap tool akan otomatis membaca file konfigurasi yang sesuai.

---

## Inisialisasi

Sebelum penggunaan pertama, jalankan inisialisasi untuk mengimpor data historis:

```
/setup
```

Inisialisasi akan memandu kamu melalui:

1. **Pilih metode impor data**
   - Meta Threads API (pengambilan otomatis)
   - Meta account export (unduh manual)
   - Berikan file data yang sudah ada

2. **Analisis otomatis postingan historis**, menghasilkan tiga file:
   - `threads_daily_tracker.json` -- Database postingan historis
   - `style_guide.md` -- Panduan gaya personal (preferensi Hook, rentang jumlah kata, pola penutup, dll.)
   - `concept_library.md` -- Pustaka konsep (melacak konsep yang sudah kamu jelaskan ke audiens)

3. **Laporan analisis** yang menunjukkan karakteristik gaya akun dan ringkasan data

Inisialisasi cukup dijalankan sekali. Pembaruan data selanjutnya terakumulasi melalui modul `/review`.

---

## Tujuh Skill

### 1. /setup -- Inisialisasi

Dijalankan saat pertama kali. Mengimpor postingan historis, menghasilkan panduan gaya, dan membangun pustaka konsep.

```
/setup
```

### 2. /voice -- Pembuatan Brand Voice

Analisis mendalam terhadap semua postingan historis dan balasan komentar untuk membangun profil Brand Voice yang komprehensif. Lebih detail dari panduan gaya `/setup`, mencakup preferensi struktur kalimat, pergeseran tone, ekspresi emosi, gaya humor, frasa yang dihindari, dan fitur mikro lainnya.

```
/voice
```

Semakin lengkap Brand Voice, semakin mirip output `/draft` dengan gaya penulisan asli kamu. Disarankan dijalankan setelah `/setup`.

Dimensi analisis: preferensi struktur kalimat, pola transisi tone, gaya ekspresi emosi, cara penyajian pengetahuan, perbedaan tone terhadap fans vs kritikus, analogi dan metafora yang sering dipakai, gaya humor, cara menyebut diri sendiri dan pembaca, frasa terlarang, fitur mikro ritme paragraf, karakteristik tone balasan komentar.

Output: `brand_voice.md`, direferensikan secara otomatis oleh modul `/draft`.

### 3. /analyze -- Analisis Tulisan (Fitur Inti)

Setelah menulis postingan, tempel konten untuk analisis empat dimensi:

```
/analyze

[tempel konten postingan kamu]
```

Empat dimensi analisis:

- **Pencocokan gaya**: Membandingkan dengan gaya historis kamu sendiri, menandai penyimpangan dan performa historis
- **Analisis psikologi**: Mekanisme Hook, kurva emosi, motivasi sharing, sinyal kepercayaan, bias kognitif, potensi pemicu komentar
- **Alignment algoritma**: Scan red line (peringatan langsung saat terdeteksi) + penilaian sinyal positif
- **Deteksi tone AI**: Scan jejak AI di level kalimat, struktur, dan konten

### 4. /topics -- Rekomendasi Topik

Ketika tidak tahu mau menulis apa selanjutnya. Menggali insight dari komentar dan data historis untuk merekomendasikan topik.

```
/topics
```

Merekomendasikan 3-5 topik, masing-masing dengan: sumber rekomendasi, alasan berbasis data, performa postingan historis serupa, estimasi rentang performa.

### 5. /draft -- Bantuan Draft

Memilih topik dari topic bank dan menghasilkan draft berdasarkan Brand Voice kamu. Ini adalah fungsi AI konten kreator paling langsung dari AK-Threads-Booster, tapi draft hanya titik awal.

```
/draft [topik]
```

Bisa menentukan topik sendiri atau biarkan sistem merekomendasikan dari topic bank. Kualitas draft bergantung pada kelengkapan data Brand Voice. Menjalankan `/voice` terlebih dahulu membuat perbedaan yang nyata.

Draft adalah titik awal. Kamu perlu mengedit dan menyesuaikan sendiri. Setelah mengedit, disarankan menjalankan `/analyze`.

### 6. /predict -- Prediksi Viral

Setelah menulis postingan, estimasi performa 24 jam setelah posting.

```
/predict

[tempel konten postingan kamu]
```

Menghasilkan estimasi konservatif/baseline/optimistis (views / likes / replies / reposts / shares) dengan alasan pendukung dan faktor ketidakpastian.

### 7. /review -- Review Pasca-Posting

Setelah memposting, gunakan untuk mengumpulkan data performa aktual, membandingkan dengan prediksi, dan memperbarui data sistem.

```
/review
```

Yang dilakukan:
- Mengumpulkan data performa aktual
- Membandingkan dengan prediksi dan menganalisis penyimpangan
- Memperbarui tracker dan panduan gaya
- Menyarankan waktu posting optimal

---

## Knowledge Base

AK-Threads-Booster menyertakan tiga knowledge base bawaan yang berfungsi sebagai titik referensi analisis:

### Psikologi Media Sosial (psychology.md)

Sumber: Kompilasi riset akademis. Mencakup mekanisme pemicu psikologis Hook, psikologi pemicu komentar, motivasi sharing dan viralitas (framework STEPPS), pembangunan kepercayaan (Pratfall Effect, Parasocial Relationship), aplikasi bias kognitif (Anchoring, Loss Aversion, Social Proof, IKEA Effect), kurva emosi dan level arousal.

Kegunaan: Fondasi teoritis untuk dimensi analisis psikologi di `/analyze`. Psikologi adalah lensa analisis, bukan aturan penulisan.

### Algoritma Meta (algorithm.md)

Sumber: Dokumen paten Meta, Facebook Papers, pernyataan kebijakan resmi, observasi KOL (pelengkap saja). Mencakup daftar red line (12 perilaku yang kena penalti), sinyal ranking (sharing via DM, komentar mendalam, dwell time, dll.), strategi pasca-posting, strategi level akun.

Kegunaan: Fondasi aturan untuk pengecekan alignment algoritma di `/analyze`. Item red line langsung memicu peringatan; item sinyal disajikan dalam tone advisory.

### Deteksi Tone AI (ai-detection.md)

Mencakup jejak AI level kalimat (10 jenis), jejak AI level struktur (5 jenis), jejak AI level konten (5 jenis), metode pengurangan tone AI (7 jenis), kondisi pemicu scan, dan definisi severity.

Kegunaan: Baseline deteksi untuk scan tone AI di `/analyze`. Menandai jejak AI agar kamu bisa memperbaiki sendiri; tidak mengoreksi otomatis.

---

## Alur Kerja Tipikal

```
1. /setup              -- Penggunaan pertama, inisialisasi sistem
2. /voice              -- Pembuatan Brand Voice mendalam (jalankan sekali)
3. /topics             -- Lihat rekomendasi topik
4. /draft [topik]      -- Buat draft
5. /analyze [postingan] -- Analisis draft atau tulisan sendiri
6. (Edit berdasarkan analisis)
7. /predict [postingan] -- Estimasi performa sebelum posting
8. (Posting)
9. /review             -- Kumpulkan data 24 jam setelah posting
10. Kembali ke langkah 3
```

Setiap siklus membuat analisis dan prediksi sistem semakin akurat. `/voice` cukup dijalankan sekali (atau jalankan ulang setelah postingan bertambah). `/draft` secara otomatis mereferensikan file Brand Voice.

---

## FAQ

**Q: Apakah AK-Threads-Booster akan menulis postingan untuk saya?**
Modul `/draft` menghasilkan draft awal, tapi draft hanya titik awal. Kamu perlu mengedit dan menyempurnakan sendiri. Kualitas draft bergantung pada kelengkapan data Brand Voice. Modul lain hanya menganalisis dan memberi saran, tidak ghostwriting.

**Q: Apakah analisis akurat dengan data yang masih sedikit?**
Terus terang, belum terlalu akurat. Sistem akan memberitahu kamu dengan jujur. Akurasi meningkat seiring data bertambah.

**Q: Apakah saya harus mengikuti semua saran?**
Tidak. Semua saran bersifat advisory. Kamu selalu punya keputusan akhir. Satu-satunya peringatan langsung adalah untuk red line algoritma (pola yang menyebabkan penurunan jangkauan).

**Q: Apakah mendukung platform selain Threads?**
Saat ini dirancang utamanya untuk Threads. Prinsip psikologi di knowledge base bersifat universal, tapi knowledge base algoritma fokus pada platform Meta.

**Q: Apa bedanya dengan tool AI menulis biasa?**
Tool generik menghasilkan konten dari model umum. Analisis dan saran AK-Threads-Booster semuanya berasal dari data historis kamu sendiri, jadi setiap pengguna mendapatkan hasil yang berbeda. Ini konsultan, bukan ghostwriter. Itulah kunci membangun strategi Threads yang benar-benar cocok dengan audiens kamu.

**Q: Bisa bantu meningkatkan engagement rate?**
AK-Threads-Booster menganalisis pola interaksi dari data historis kamu, termasuk menggali insight dari komentar (comment mining). Dengan memahami apa yang memicu audiens kamu untuk berkomentar dan berinteraksi, kamu bisa membuat konten yang lebih sesuai. Tapi peningkatan engagement adalah hasil dari penerapan insight, bukan jaminan otomatis.

**Q: Bagaimana cara menambah followers Threads dengan tool ini?**
AK-Threads-Booster bukan tool penambah followers otomatis. Yang dilakukan adalah menganalisis dan memberi saran agar setiap postingan punya peluang performa lebih baik. Pertumbuhan followers adalah hasil dari konsistensi memposting konten berkualitas.

**Q: Apakah ini bisa menjamin postingan viral?**
Tidak. Algoritma Threads adalah sistem yang sangat kompleks, dan tidak ada tool yang bisa menjamin postingan viral. Yang dilakukan AK-Threads-Booster adalah membantu kamu membuat keputusan lebih baik berdasarkan data historis sendiri, menghindari red line algoritma yang sudah diketahui, dan meningkatkan probabilitas performa setiap postingan melalui analisis psikologi dan data. Ini adalah Threads content creation Skill paling komprehensif yang tersedia saat ini, tapi faktor yang menentukan apakah postingan bisa viral -- timing, relevansi topik, kondisi audiens, logika distribusi algoritma pada saat itu -- terlalu banyak untuk dikontrol oleh tool manapun. Gunakan sebagai konsultan data, bukan mesin jaminan viral.

---

## Struktur Direktori

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

MIT License. Lihat [LICENSE](./LICENSE).
