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

Ein Open-Source Claude Code Skill und KI-Schreibassistent, entwickelt speziell fuer Content-Ersteller auf Threads. AK-Threads-Booster analysiert Ihre historischen Beitragsdaten, wendet Forschungsergebnisse aus der Social-Media-Psychologie und Erkenntnisse zum Threads Algorithmus an, um personalisierte Schreibanalysen, Brand Voice Profiling und Entwurfshilfe zu liefern.

Wenn Sie ein datengestuetztes System zur Content-Erstellung fuer Threads suchen, einen KI Schreibassistenten der tatsaechlich aus Ihren eigenen Daten lernt, oder eine fundierte Social Media Strategie auf Basis realer Metriken, dann ist dieses Projekt fuer Sie entwickelt. Kein Template. Kein Regelwerk. Ein Beratungssystem, das Ihnen hilft den Threads Algorithmus zu verstehen und Ihre Daten in eine nachhaltige Wachstumsstrategie umzuwandeln. Funktioniert als Skill / Plugin fuer Claude Code, Cursor, Codex, Windsurf, GitHub Copilot und Google Antigravity.

**Vollstaendig Open-Source. Alle Daten bleiben lokal auf Ihrem Rechner. Keine Cloud-Uebertragung, kein Tracking, keine externen Server.**


## Schnellstart

1. Repo in dein AI-Tool einbinden.
2. `/setup` fuer deine historischen Beitraege ausfuehren.
3. Nach dem Schreiben `/analyze` nutzen, vor dem Posten optional `/predict`.
4. Nach dem Posten `/review` fuer 24h- und 72h-Checkpoints verwenden.
5. Mit Threads API Token kannst du `scripts/update_snapshots.py` fuer Snapshots laufen lassen.

## Datenaktualisierung

- **Checkpoint-Modus**: Fuer alle Nutzer. `/review` sammelt 24h-, 72h- und 7d-Werte und aktualisiert damit die Vorhersagebasis.
- **Snapshot-Modus**: Mit Threads API. `scripts/update_snapshots.py` schreibt laufend `snapshots[]` und aktualisiert die naechsten `performance_windows`.

---

## Was ist AK-Threads-Booster

AK-Threads-Booster ist ein Open-Source Threads Skill -- kein Schreibtemplate, kein Regelwerk und kein KI-Content-Generator, der Sie ersetzt.

Es ist ein methodisches System, das drei Dinge tut:

1. **Analysiert Ihre historischen Daten**, um zu identifizieren, welcher Content auf Ihrem Account das meiste Threads Engagement erzeugt
2. **Nutzt Psychologie und Wissen ueber den Threads Algorithmus als analytische Perspektiven**, um zu erklaeren, warum bestimmte Beitraege gut performen
3. **Praesentiert die Ergebnisse transparent**, damit Sie selbst entscheiden koennen, was der naechste Schritt ist

Jeder Nutzer erhaelt unterschiedliche Ergebnisse, weil jeder Account ein anderes Publikum, einen anderen Stil und einen anderen Datensatz hat. Das ist der grundlegende Unterschied zwischen einer datengestuetzten Threads Strategie und allgemeinen Social-Media-Ratschlaegen.

### Warum das fuer den deutschen Markt relevant ist

Deutsche Nutzer haben spezifische Anforderungen an digitale Werkzeuge, die sich von anderen Maerkten unterscheiden:

- **Datenschutz und Datensicherheit**: Wo werden die Daten verarbeitet? Wer hat Zugriff? AK-Threads-Booster verarbeitet alle Daten ausschliesslich lokal auf Ihrem Rechner. Nichts wird hochgeladen, nichts wird an externe Server uebertragen, nichts wird gespeichert ausser auf Ihrer eigenen Maschine
- **Systematischer Ansatz**: Das System ist modular aufgebaut mit sieben klar definierten Skills. Jeder Skill hat einen definierten Input, Output und Zweck. Keine Blackbox, sondern ein nachvollziehbares Analysesystem
- **Transparenz statt Versprechen**: AK-Threads-Booster gibt keine Garantien. Es zeigt Ihnen, was Ihre Daten hergeben, und ueberlasst die Entscheidung Ihnen. Wenn die Datenbasis zu duenn ist, sagt es das offen

Fuer Ersteller, die Threads systematisch und datenbasiert betreiben wollen, ohne die Kontrolle ueber ihre Daten oder ihren Stil abzugeben, ist dieses System konzipiert.




---

## Grundprinzipien

**Berater, kein Lehrer.** AK-Threads-Booster sagt nicht "Sie sollten so schreiben." Es sagt "Als Sie das zuvor gemacht haben, sahen die Daten so aus -- zur Ihrer Information." Keine Bewertung, keine Korrekturen, kein Ghostwriting.

**Datengetrieben, nicht regelgetrieben.** Alle Vorschlaege basieren auf Ihren eigenen historischen Daten, nicht auf einer generischen Liste von "10 Social-Media-Marketing-Tipps." Bei unzureichender Datenlage informiert das System Sie ehrlich, anstatt Sicherheit vorzutaeuschen.

**Red Lines sind die einzigen festen Regeln.** Nur Verhaltensweisen, die der Algorithmus von Meta explizit abstraft (Engagement Bait, Clickbait, Wiederveroeffentlichungen mit hoher Aehnlichkeit etc.), loesen direkte Warnungen aus. Alles andere ist beratend. Sie behalten immer die Entscheidungshoheit.




---

## Multi-Tool-Unterstuetzung

AK-Threads-Booster funktioniert mit mehreren KI-Coding-Tools. Claude Code bietet die vollstaendige 7-Skill-Erfahrung; andere Tools bieten die Kernanalysefunktionen.

### Unterstuetzte Tools und Konfigurationsdateien

| Tool | Konfigurationsort | Umfang |
|------|-------------------|--------|
| **Claude Code** | `skills/`-Verzeichnis (7 Skills) | Voller Funktionsumfang: setup, voice, analyze, topics, draft, predict, review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | Kernanalyse (4 Dimensionen) |
| **Codex** | `AGENTS.md` (Wurzelverzeichnis) | Kernanalyse (4 Dimensionen) |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | Kernanalyse (4 Dimensionen) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Kernanalyse (4 Dimensionen) |
| **Google Antigravity** | `.agents/`-Verzeichnis + `AGENTS.md` im Wurzelverzeichnis | Kernanalyse (4 Dimensionen) |

### Funktionsunterschiede

- **Claude Code**: Voller Funktionsumfang einschliesslich Initialisierung (setup), Brand Voice Profiling (voice), Schreibanalyse (analyze), Themenempfehlungen (topics), Entwurfshilfe (draft), Viralitaetsprognose (predict) und Nachveroeffentlichungs-Review (review) -- sieben eigenstaendige Skills
- **Andere Tools**: Kernschreibanalyse mit vier Dimensionen (Stilabgleich, psychologische Analyse, Algorithmus-Alignment-Pruefung, KI-Ton-Erkennung), unter Nutzung derselben Wissensbasis (`knowledge/`-Verzeichnis)
- **Google Antigravity**: Liest sowohl die `AGENTS.md` im Wurzelverzeichnis (Beraternormen und Red-Line-Regeln) als auch das `.agents/`-Verzeichnis (Regeldateien + Analyse-Skills)

Alle Tool-Versionen enthalten:
- Richtlinien zum Beraterton (keine Bewertung, keine Korrekturen, kein Ghostwriting)
- Algorithmus-Red-Line-Regeln (Warnung bei Treffer)
- Wissensbasis-Referenzen (Psychologie, Algorithmus, KI-Ton-Erkennung)




---

## Installation

### Option 1: Installation ueber GitHub

```bash
# In Ihrem Claude Code Projektverzeichnis
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### Option 2: Manuelle Installation

1. Klonen Sie dieses Repository lokal:
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. Kopieren Sie das `AK-Threads-booster`-Verzeichnis in das `.claude/plugins/`-Verzeichnis Ihres Claude Code Projekts:
   ```bash
   cp -r AK-Threads-booster /pfad/zu/ihrem/projekt/.claude/plugins/
   ```

3. Starten Sie Claude Code neu. Die Skills werden automatisch erkannt.

### Andere Tools

Wenn Sie Cursor, Windsurf, Codex oder GitHub Copilot verwenden, klonen Sie das Repository einfach in Ihr Projektverzeichnis. Jedes Tool liest automatisch seine entsprechende Konfigurationsdatei.




---

## Initialisierung

Vor der ersten Nutzung fuehren Sie die Initialisierung durch, um Ihre historischen Daten zu importieren:

```
/setup
```

Die Initialisierung fuehrt Sie durch:

1. **Wahl der Datenimportmethode**
   - Meta Threads API (automatischer Abruf)
   - Meta-Kontoexport (manueller Download)
   - Vorhandene Datendateien direkt bereitstellen

2. **Automatische Analyse historischer Beitraege**, wobei drei Dateien erzeugt werden:
   - `threads_daily_tracker.json` -- Datenbank historischer Beitraege
   - `style_guide.md` -- Personalisierter Stilleitfaden (Ihre Hook-Praeferenzen, Wortanzahlbereiche, Abschlussmuster etc.)
   - `concept_library.md` -- Konzeptbibliothek (verfolgt Konzepte, die Sie Ihrem Publikum bereits erklaert haben)

3. **Analysebericht** mit den Stilmerkmalen Ihres Accounts und einer Datenuebersicht

Die Initialisierung muss nur einmal ausgefuehrt werden. Nachfolgende Datenaktualisierungen kumulieren sich ueber das `/review`-Modul.




---

## Die sieben Skills

### 1. /setup -- Initialisierung

Einmalig bei der ersten Nutzung ausfuehren. Importiert historische Beitraege, erstellt Ihren Stilleitfaden und baut die Konzeptbibliothek auf.

```
/setup
```

### 2. /voice -- Brand Voice Profiling

Tiefgehende Analyse aller historischen Beitraege und Kommentarantworten zum Aufbau eines umfassenden Brand Voice Profils. Geht tiefer als der Stilleitfaden aus `/setup` und umfasst Satzstrukturpraeferenzen, Tonwechsel, emotionalen Ausdruck, Humorstil, Tabuphrasen und mehr.

```
/voice
```

Je vollstaendiger Ihr Brand Voice Profil, desto naeher kommen die Ergebnisse von `/draft` an Ihren tatsaechlichen Schreibstil heran. Empfohlen nach `/setup`.

Analysedimensionen umfassen: Satzstrukturpraeferenzen, Tonuebergangsmuster, Stil des emotionalen Ausdrucks, Wissenspraesentation, Tonunterschiede zwischen Fans und Kritikern, gaengige Analogien und Metaphern, Humor- und Witzstil, Selbstreferenz und Ansprache des Publikums, Tabuphrasen, Mikro-Merkmale des Absatzrhythmus, Tonmerkmale bei Kommentarantworten.

Ausgabe: `brand_voice.md`, wird automatisch vom `/draft`-Modul referenziert.

### 3. /analyze -- Schreibanalyse (Kernfunktion)

Nach dem Verfassen eines Beitrags fuegen Sie Ihren Inhalt fuer die Vier-Dimensionen-Analyse ein:

```
/analyze

[Ihren Beitragsinhalt hier einfuegen]
```

Vier Analysedimensionen:

- **Stilabgleich**: Vergleich mit Ihrem eigenen historischen Stil, markiert Abweichungen und historische Leistungsdaten
- **Psychologische Analyse**: Hook-Mechanismen, emotionaler Bogen, Teilungsmotivation, Vertrauenssignale, kognitive Verzerrungen, Kommentarausloesepotenzial
- **Algorithmus-Alignment**: Red-Line-Scan (Warnung bei Treffer) + Bewertung positiver Signale
- **KI-Ton-Erkennung**: Scanning auf KI-Spuren auf Satz-, Struktur- und Inhaltsebene

### 4. /topics -- Themenempfehlungen

Wenn Sie nicht wissen, worueber Sie als naechstes schreiben sollen. Gewinnt Erkenntnisse aus Kommentaren und historischen Daten fuer Themenempfehlungen.

```
/topics
```

Empfiehlt 3-5 Themen, jeweils mit: Empfehlungsquelle, datengestuetzte Begruendung, Leistung aehnlicher historischer Beitraege, geschaetzter Leistungsbereich.

### 5. /draft -- Entwurfshilfe

Waehlt ein Thema aus Ihrer Themenbank und erstellt einen Entwurf basierend auf Ihrem Brand Voice. Dies ist die direkteste KI-Content-Erstellungsfunktion in AK-Threads-Booster, aber der Entwurf ist nur ein Ausgangspunkt.

```
/draft [Thema]
```

Sie koennen ein Thema angeben oder das System eines aus Ihrer Themenbank empfehlen lassen. Die Entwurfsqualitaet haengt davon ab, wie vollstaendig Ihre Brand Voice Daten sind -- `/voice` vorher auszufuehren macht einen spuerbaren Unterschied.

Der Entwurf ist ein Ausgangspunkt. Sie muessen ihn selbst ueberarbeiten und anpassen. Nach der Bearbeitung wird empfohlen, `/analyze` auszufuehren.

### 6. /predict -- Viralitaetsprognose

Nach dem Verfassen eines Beitrags schaetzen Sie dessen Leistung 24 Stunden nach Veroeffentlichung.

```
/predict

[Ihren Beitragsinhalt hier einfuegen]
```

Liefert konservative/Basis-/optimistische Schaetzungen (Views / Likes / Replies / Reposts / Shares) mit Begruendung und Unsicherheitsfaktoren.

### 7. /review -- Nachveroeffentlichungs-Review

Nach der Veroeffentlichung nutzen Sie dies, um tatsaechliche Leistungsdaten zu sammeln, mit Prognosen zu vergleichen und Systemdaten zu aktualisieren.

```
/review
```

Was es tut:
- Sammelt tatsaechliche Leistungsdaten
- Vergleicht mit Prognosen und analysiert Abweichungen
- Aktualisiert Tracker und Stilleitfaden
- Schlaegt optimale Veroeffentlichungszeiten vor




---

## Wissensbasis

AK-Threads-Booster enthaelt drei integrierte Wissensbasen, die als analytische Referenzpunkte dienen:

### Social-Media-Psychologie (psychology.md)

Quelle: Zusammenstellung akademischer Forschung. Umfasst Hook-Mechanismen der psychologischen Ausloesung, Kommentarausloesepsychologie, Teilungsmotivation und Viralitaet (STEPPS-Framework), Vertrauensaufbau (Pratfall Effect, Parasocial Relationship), Anwendungen kognitiver Verzerrungen (Anchoring, Loss Aversion, Social Proof, IKEA Effect), emotionaler Bogen und Aktivierungsniveaus.

Zweck: Theoretische Grundlage fuer die psychologische Analysedimension in `/analyze`. Psychologie ist eine analytische Perspektive, keine Schreibregel.

### Meta-Algorithmus (algorithm.md)

Quelle: Meta-Patentdokumente, Facebook Papers, offizielle Richtlinienerklaerungen, KOL-Beobachtungen (nur ergaenzend). Umfasst Red-Line-Liste (12 abgestrafte Verhaltensweisen), Ranking-Signale (DM-Teilen, tiefgehende Kommentare, Verweildauer etc.), Strategie nach Veroeffentlichung, Strategie auf Kontoebene.

Zweck: Regelgrundlage fuer die Algorithmus-Alignment-Pruefung in `/analyze`. Red-Line-Eintraege loesen Warnungen aus; Signaleintraege werden im beratenden Ton praesentiert.

### KI-Ton-Erkennung (ai-detection.md)

Umfasst KI-Spuren auf Satzebene (10 Typen), KI-Spuren auf Strukturebene (5 Typen), KI-Spuren auf Inhaltsebene (5 Typen), Methoden zur KI-Ton-Reduzierung (7 Typen), Scan-Ausloesebedingungen und Schweregrad-Definitionen.

Zweck: Erkennungsgrundlinie fuer das KI-Ton-Scanning in `/analyze`. Markiert KI-Spuren, damit Sie diese selbst korrigieren koennen; korrigiert nicht automatisch.




---

## Typischer Arbeitsablauf

```
1. /setup              -- Erstmalige Nutzung, System initialisieren
2. /voice              -- Tiefgehendes Brand Voice Profiling (einmalig ausfuehren)
3. /topics             -- Themenempfehlungen ansehen
4. /draft [Thema]      -- Entwurf erstellen
5. /analyze [Beitrag]  -- Entwurf oder eigenen Text analysieren
6. (Basierend auf der Analyse ueberarbeiten)
7. /predict [Beitrag]  -- Leistung vor Veroeffentlichung schaetzen
8. (Veroeffentlichen)
9. /review             -- 24h nach Veroeffentlichung Daten sammeln
10. Zurueck zu Schritt 3
```

Jeder Zyklus macht die Analysen und Prognosen des Systems praeziser. `/voice` muss nur einmalig ausgefuehrt werden (oder erneut nach Ansammlung weiterer Beitraege). `/draft` referenziert automatisch Ihre Brand Voice Datei.




---

## Haeufig gestellte Fragen

**F: Schreibt AK-Threads-Booster Beitraege fuer mich?**
Das `/draft`-Modul erstellt initiale Entwuerfe, aber Entwuerfe sind nur ein Ausgangspunkt. Sie muessen diese selbst ueberarbeiten und verfeinern. Die Entwurfsqualitaet haengt davon ab, wie vollstaendig Ihre Brand Voice Daten sind. Alle anderen Module analysieren und beraten nur -- kein Ghostwriting.

**F: Wo werden meine Daten gespeichert?**
Ausschliesslich lokal auf Ihrem Rechner. AK-Threads-Booster ist ein Open-Source Skill, der in Ihrer lokalen Entwicklungsumgebung laeuft. Es gibt keinen externen Server, keine Cloud-Uebertragung, kein Tracking. Ihre Beitragsdaten, Ihr Brand Voice Profil, Ihr Tracker -- alles bleibt auf Ihrer Maschine. Der Quellcode ist vollstaendig einsehbar.

**F: Ist die Analyse bei wenigen Daten genau?**
Nicht besonders. Das System teilt Ihnen das offen mit. Die Genauigkeit verbessert sich mit zunehmender Datenmenge.

**F: Muss ich die Vorschlaege befolgen?**
Nein. Alle Vorschlaege sind ausschliesslich beratend. Sie behalten immer die Entscheidungshoheit. Die einzigen direkten Warnungen betreffen Algorithmus-Red-Lines (Schreibmuster, die Herabstufung ausloesen).

**F: Wie systematisch ist das System aufgebaut?**
AK-Threads-Booster besteht aus sieben klar definierten Modulen, die jeweils einen spezifischen Zweck erfuellen. Jedes Modul hat definierte Ein- und Ausgaben. Die drei Wissensbasen (Psychologie, Algorithmus, KI-Erkennung) bilden die analytische Grundlage. Der gesamte Quellcode ist in der Verzeichnisstruktur einsehbar und nachvollziehbar. Kein Teil des Systems ist eine Blackbox.

**F: Unterstuetzt es Plattformen ausser Threads?**
Derzeit primaer fuer Threads konzipiert. Die Psychologieprinzipien in der Wissensbasis sind universell, aber die Algorithmus-Wissensbasis konzentriert sich auf die Meta-Plattform.

**F: Wie unterscheidet es sich von einem typischen KI-Schreibassistenten?**
Generische Tools produzieren Inhalte aus allgemeinen Modellen. Die Analysen und Vorschlaege von AK-Threads-Booster stammen vollstaendig aus Ihren eigenen historischen Daten, sodass jeder Nutzer unterschiedliche Ergebnisse erhaelt. Es ist ein Berater, kein Ghostwriter. Das ist der Schluessel zum Aufbau einer Threads-Strategie, die tatsaechlich zu Ihrem Publikum passt.

**F: Garantiert dies, dass meine Beitraege viral gehen?**
Nein. Der Threads Algorithmus ist ein aeusserst komplexes System, und kein Tool kann virale Beitraege garantieren. Was AK-Threads-Booster tut, ist Ihnen zu helfen, auf Basis Ihrer eigenen historischen Daten bessere Entscheidungen zu treffen, bekannte Algorithmus-Red-Lines zu vermeiden und die Wahrscheinlichkeit zu erhoehen, dass jeder Beitrag gut performt -- durch psychologische und datengestuetzte Analyse. Es ist derzeit das umfassendste Threads Content-Erstellungs-Skill, aber die Faktoren, die darueber entscheiden, ob ein Beitrag viral geht -- Timing, Themenrelevanz, Zustand des Publikums, die Verteilungslogik des Algorithmus in dem Moment -- sind zu zahlreich, als dass ein Tool sie vollstaendig kontrollieren koennte. Betrachten Sie es als Ihren Datenberater, nicht als Viralitaetsgarantie.




---

## Verzeichnisstruktur

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

## Lizenz

MIT License. Siehe [LICENSE](./LICENSE).


