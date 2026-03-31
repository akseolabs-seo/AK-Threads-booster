[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

# AK-Threads-Booster

Un skill open-source pour Claude Code et assistant d'ecriture IA concu specifiquement pour les createurs de contenu sur Threads. AK-Threads-Booster analyse vos donnees historiques de publications, applique des recherches en psychologie des reseaux sociaux et des connaissances sur l'algorithme de Threads pour fournir une analyse d'ecriture personnalisee, un profilage de Brand Voice et une assistance a la redaction de brouillons.

Si vous cherchez un outil IA pour reseaux sociaux qui apprend reellement de vos propres donnees, une strategie de contenu fondee sur des metriques concretes, ou un moyen d'ameliorer votre creation de contenu sans sacrifier la qualite de votre ecriture, ce projet est fait pour ca. Pas un template. Pas un ensemble de regles. Un systeme de conseil qui vous aide a comprendre l'algorithme de Threads et a transformer vos donnees en engagement reel. Fonctionne comme skill / plugin pour Claude Code, Cursor, Codex, Windsurf, GitHub Copilot et Google Antigravity.

---

## Ce qu'est AK-Threads-Booster

AK-Threads-Booster est un skill open-source pour Threads. Ce n'est pas un modele de publication, pas un ensemble de regles, et pas un generateur de contenu IA qui vous remplace.

C'est un systeme methodologique qui fait trois choses :

1. **Analyse vos donnees historiques** pour identifier quel contenu genere le plus d'engagement sur Threads sur votre compte
2. **Utilise la psychologie et la connaissance de l'algorithme de Threads comme prismes analytiques** pour expliquer pourquoi certaines publications performent mieux
3. **Presente les resultats de maniere transparente** pour que vous decidiez de la suite

Chaque utilisateur obtient des resultats differents parce que chaque compte a une audience, un style et un jeu de donnees different. C'est la difference fondamentale entre une strategie de contenu basee sur les donnees et les conseils generiques sur les reseaux sociaux.

### Pourquoi c'est pertinent pour le marche francophone

Le public francophone a une relation particuliere avec la qualite de l'ecriture. Sur Threads comme ailleurs, les lecteurs francophones sont sensibles a la langue, au style, et surtout a l'authenticite. Le contenu qui sonne creux, generique ou manifestement genere par une machine provoque un rejet rapide.

C'est precisement la que les createurs francophones rencontrent un dilemme :

- **Qualite contre portee** : Comment augmenter votre visibilite sans diluer la qualite de votre ecriture ? Comment toucher plus de monde sans tomber dans le marketing agressif que le public francophone rejette ?
- **L'IA comme menace pour l'authenticite** : Les outils de generation de contenu produisent du texte techniquement correct mais stylistiquement plat. Pour un public habitue a valoriser la langue, c'est un probleme
- **Preserver une voix distinctive** : Dans un flux de contenu de plus en plus homogene, comment maintenir ce qui rend votre ecriture reconnaissable ?

AK-Threads-Booster aborde ces questions differemment. Au lieu de generer du contenu a votre place, il analyse votre propre ecriture pour identifier ce qui fonctionne avec votre audience specifique. La detection de ton IA vous aide a reperer exactement ou votre texte perd en naturalite. Le Brand Voice profiling capture les nuances de votre style pour que les brouillons servent de point de depart credible, pas de produit fini generique.

---

## Principes fondamentaux

**Consultant, pas professeur.** AK-Threads-Booster ne vous dira pas "vous devriez ecrire comme ca." Il vous dira "quand vous avez fait ca avant, les donnees montraient ca -- a vous de voir." Pas de notation, pas de correction, pas de ghostwriting.

**Pilote par les donnees, pas par les regles.** Toutes les suggestions proviennent de vos propres donnees historiques, pas d'une liste generique de "10 Conseils Marketing pour les Reseaux Sociaux." Quand les donnees sont insuffisantes, le systeme vous le dit honnetement au lieu de feindre l'assurance.

**Les red lines sont les seules regles strictes.** Seuls les comportements que l'algorithme de Meta penalise explicitement (engagement bait, clickbait, republications a haute similarite, etc.) declenchent des avertissements directs. Tout le reste est consultatif. Vous gardez toujours le dernier mot.

---

## Support Multi-Outils

AK-Threads-Booster fonctionne avec plusieurs outils de codage IA. Claude Code offre l'experience complete avec 7 Skills ; les autres outils offrent les capacites d'analyse principales.

### Outils supportes et fichiers de configuration

| Outil | Emplacement du fichier | Portee |
|-------|----------------------|--------|
| **Claude Code** | repertoire `skills/` (7 Skills) | Fonctionnalite complete : setup, voice, analyze, topics, draft, predict, review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | Analyse principale (4 dimensions) |
| **Codex** | `AGENTS.md` (racine) | Analyse principale (4 dimensions) |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | Analyse principale (4 dimensions) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Analyse principale (4 dimensions) |
| **Google Antigravity** | repertoire `.agents/` + `AGENTS.md` a la racine | Analyse principale (4 dimensions) |

### Differences de fonctionnalites

- **Claude Code** : Fonctionnalite complete incluant l'initialisation (setup), le profilage Brand Voice (voice), l'analyse d'ecriture (analyze), les recommandations de sujets (topics), l'assistance de brouillon (draft), la prediction de publication virale (predict) et la revue post-publication (review) -- sept Skills independants
- **Autres outils** : Analyse d'ecriture principale avec quatre dimensions (comparaison de style, analyse psychologique, verification d'alignement algorithmique, detection de ton IA), partageant la meme base de connaissances (repertoire `knowledge/`)
- **Google Antigravity** : Lit a la fois l'`AGENTS.md` a la racine (normes de consultant et regles de red line) et le repertoire `.agents/` (fichiers de regles + skills d'analyse)

Toutes les versions incluent :
- Directives de ton consultatif (pas de notation, pas de correction, pas de ghostwriting)
- Regles de red line algorithmiques (avertissement a la detection)
- References de la base de connaissances (psychologie, algorithme, detection de ton IA)

---

## Installation

### Option 1 : Installation via GitHub

```bash
# Dans le repertoire de votre projet Claude Code
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### Option 2 : Installation manuelle

1. Clonez ce depot localement :
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. Copiez le repertoire `AK-Threads-booster` dans le `.claude/plugins/` de votre projet Claude Code :
   ```bash
   cp -r AK-Threads-booster /chemin/vers/votre/projet/.claude/plugins/
   ```

3. Redemarrez Claude Code. Les Skills seront detectes automatiquement.

### Autres outils

Si vous utilisez Cursor, Windsurf, Codex ou GitHub Copilot, clonez simplement le depot dans le repertoire de votre projet. Chaque outil lira automatiquement son fichier de configuration correspondant.

---

## Initialisation

Avant la premiere utilisation, lancez l'initialisation pour importer vos donnees historiques :

```
/setup
```

L'initialisation vous guide a travers :

1. **Choix de la methode d'importation des donnees**
   - Meta Threads API (recuperation automatique)
   - Export de compte Meta (telechargement manuel)
   - Fournir directement des fichiers de donnees existants

2. **Analyse automatique des publications historiques**, generant trois fichiers :
   - `threads_daily_tracker.json` -- Base de donnees des publications historiques
   - `style_guide.md` -- Guide de style personnalise (vos preferences de Hook, fourchettes de nombre de mots, motifs de conclusion, etc.)
   - `concept_library.md` -- Bibliotheque de concepts (suit les concepts que vous avez deja expliques a votre audience)

3. **Rapport d'analyse** montrant les caracteristiques stylistiques de votre compte et un panorama des donnees

L'initialisation ne doit etre executee qu'une seule fois. Les mises a jour de donnees suivantes s'accumulent via le module `/review`.

---

## Les sept Skills

### 1. /setup -- Initialisation

A executer lors de la premiere utilisation. Importe les publications historiques, genere votre guide de style et construit la bibliotheque de concepts.

```
/setup
```

### 2. /voice -- Profilage Brand Voice

Analyse approfondie de toutes les publications historiques et reponses aux commentaires pour construire un profil Brand Voice complet. Va plus loin que le guide de style de `/setup`, couvrant les preferences de structure de phrase, les changements de ton, le style d'expression emotionnelle, le style d'humour, les expressions proscrites et plus encore.

```
/voice
```

Plus votre Brand Voice est complet, plus les resultats de `/draft` se rapprochent de votre style d'ecriture reel. Recommande apres `/setup`.

Cette fonctionnalite est particulierement pertinente pour les createurs francophones. La langue francaise offre une richesse de nuances stylistiques -- niveau de langue, registre, rythme de phrase -- que les outils generiques ne capturent pas. Le profilage Brand Voice analyse ces subtilites dans votre propre ecriture pour que les brouillons respectent votre voix, pas celle d'un modele generique.

Dimensions d'analyse incluent : preferences de structure de phrase, motifs de transition de ton, style d'expression emotionnelle, presentation des connaissances, differences de ton entre fans et critiques, analogies et metaphores recurrentes, style d'humour et d'esprit, auto-reference et maniere de s'adresser a l'audience, expressions proscrites, micro-caracteristiques du rythme de paragraphe, caracteristiques de ton dans les reponses aux commentaires.

Sortie : `brand_voice.md`, reference automatiquement par le module `/draft`.

### 3. /analyze -- Analyse d'ecriture (Fonctionnalite principale)

Apres avoir redige une publication, collez votre contenu pour une analyse en quatre dimensions :

```
/analyze

[collez le contenu de votre publication]
```

Quatre dimensions d'analyse :

- **Comparaison de style** : Compare avec votre propre style historique, signale les ecarts et les performances historiques
- **Analyse psychologique** : Mecanismes de Hook, arc emotionnel, motivation de partage, signaux de confiance, biais cognitifs, potentiel de declenchement de commentaires
- **Alignement algorithmique** : Scan des red lines (avertissements a la detection) + evaluation des signaux positifs
- **Detection de ton IA** : Scan des traces d'IA aux niveaux de la phrase, de la structure et du contenu

La detection de ton IA merite une attention particuliere dans le contexte francophone. Le public francais et francophone est parmi les plus sensibles au contenu qui sonne artificiel. Cette dimension identifie avec precision ou votre texte perd en naturalite, que ce soit par des formulations trop lisses, des structures trop symetriques, ou un ton trop neutre.

### 4. /topics -- Recommandations de sujets

Quand vous ne savez pas quoi ecrire ensuite. Extrait des insights des commentaires et des donnees historiques pour recommander des sujets.

```
/topics
```

Recommande 3-5 sujets, chacun avec : source de la recommandation, raisonnement appuye par les donnees, performance de publications historiques similaires, fourchette de performance estimee.

### 5. /draft -- Assistance de brouillon

Selectionne un sujet de votre banque de sujets et genere un brouillon base sur votre Brand Voice. C'est la fonction de creation de contenu IA la plus directe d'AK-Threads-Booster, mais le brouillon n'est qu'un point de depart.

```
/draft [sujet]
```

Vous pouvez specifier un sujet ou laisser le systeme en recommander un de votre banque de sujets. La qualite du brouillon depend de la completude de vos donnees de Brand Voice -- executer `/voice` au prealable fait une difference notable.

Le brouillon est un point de depart. Vous devez le reviser et l'ajuster vous-meme. Apres revision, executer `/analyze` est recommande.

### 6. /predict -- Prediction de publication virale

Apres avoir redige une publication, estimez sa performance 24 heures apres sa mise en ligne.

```
/predict

[collez le contenu de votre publication]
```

Produit des estimations conservatrice/base/optimiste (views / likes / replies / reposts / shares) avec justification et facteurs d'incertitude.

### 7. /review -- Revue post-publication

Apres avoir publie, utilisez ceci pour collecter les donnees de performance reelles, comparer avec les predictions et mettre a jour les donnees du systeme.

```
/review
```

Ce qu'il fait :
- Collecte les donnees de performance reelles
- Compare avec les predictions et analyse les ecarts
- Met a jour le tracker et le guide de style
- Suggere les horaires de publication optimaux

---

## Base de connaissances

AK-Threads-Booster inclut trois bases de connaissances integrees qui servent de points de reference analytiques :

### Psychologie des reseaux sociaux (psychology.md)

Source : Compilation de recherche academique. Couvre les mecanismes de declenchement psychologique des Hooks, la psychologie du declenchement de commentaires, la motivation de partage et la viralite (framework STEPPS), la construction de confiance (Pratfall Effect, Parasocial Relationship), les applications des biais cognitifs (Anchoring, Loss Aversion, Social Proof, IKEA Effect), l'arc emotionnel et les niveaux d'activation.

Objectif : Fondement theorique pour la dimension d'analyse psychologique dans `/analyze`. La psychologie est un prisme analytique, pas une regle d'ecriture.

### Algorithme Meta (algorithm.md)

Source : Documents de brevet Meta, Facebook Papers, declarations de politique officielle, observations de KOLs (uniquement en complement). Couvre la liste des red lines (12 comportements penalises), les signaux de classement (partage en DM, commentaires approfondis, temps de consultation, etc.), strategie post-publication, strategie au niveau du compte.

Objectif : Base de regles pour la verification d'alignement algorithmique dans `/analyze`. Les elements red line declenchent des avertissements ; les elements de signal sont presentes sur un ton consultatif.

### Detection de ton IA (ai-detection.md)

Couvre les traces d'IA au niveau de la phrase (10 types), les traces d'IA au niveau de la structure (5 types), les traces d'IA au niveau du contenu (5 types), les methodes de reduction du ton IA (7 types), les conditions de declenchement du scan et les definitions de severite.

Objectif : Ligne de base de detection pour le scan de ton IA dans `/analyze`. Signale les traces d'IA pour que vous les corrigiez vous-meme ; ne corrige pas automatiquement.

---

## Flux de travail typique

```
1. /setup              -- Premiere utilisation, initialiser le systeme
2. /voice              -- Profilage Brand Voice approfondi (executer une fois)
3. /topics             -- Voir les recommandations de sujets
4. /draft [sujet]      -- Generer un brouillon
5. /analyze [post]     -- Analyser le brouillon ou votre propre texte
6. (Reviser en fonction de l'analyse)
7. /predict [post]     -- Estimer la performance avant publication
8. (Publier)
9. /review             -- Collecter les donnees 24h apres publication
10. Retour a l'etape 3
```

Chaque cycle rend les analyses et predictions du systeme plus precises. `/voice` n'a besoin d'etre execute qu'une fois (ou re-execute apres avoir accumule plus de publications). `/draft` reference automatiquement votre fichier Brand Voice.

---

## Questions frequentes

**Q : AK-Threads-Booster ecrit-il des publications a ma place ?**
Le module `/draft` genere des brouillons initiaux, mais les brouillons ne sont qu'un point de depart. Vous devez les reviser et les affiner vous-meme. La qualite du brouillon depend de la completude de vos donnees de Brand Voice. Les autres modules analysent et conseillent uniquement -- pas de ghostwriting.

**Q : La detection de ton IA fonctionne-t-elle bien avec le francais ?**
Les principes de detection sont universels (structures trop symetriques, formulations generiques, ton anormalement neutre), et l'analyse compare avec votre propre style historique. Si vous ecrivez en francais, le systeme apprend de votre style en francais et detecte les ecarts par rapport a votre propre voix, pas par rapport a un modele abstrait.

**Q : L'analyse est-elle precise avec peu de donnees ?**
Pas vraiment. Le systeme vous le dit honnetement. La precision s'ameliore a mesure que les donnees s'accumulent.

**Q : Faut-il suivre toutes les suggestions ?**
Non. Toutes les suggestions sont purement consultatives. Vous gardez toujours le dernier mot. Les seuls avertissements directs concernent les red lines algorithmiques (motifs d'ecriture qui declenchent une retrogradation).

**Q : Comment ca se compare aux outils de marketing qui promettent des "hacks de croissance" ?**
AK-Threads-Booster ne promet pas de hacks. Il ne vous dit pas "postez a telle heure" ou "utilisez ces mots magiques." Il analyse vos propres donnees et vous montre ce qui fonctionne pour votre audience specifique. Pas de formules, pas de recettes. Des donnees.

**Q : Supporte-t-il des plateformes autres que Threads ?**
Actuellement concu principalement pour Threads. Les principes de psychologie dans la base de connaissances sont universels, mais la base de connaissances algorithmique se concentre sur la plateforme Meta.

**Q : En quoi est-ce different d'un outil d'ecriture IA classique ?**
Les outils generiques produisent du contenu a partir de modeles generaux. Les analyses et suggestions d'AK-Threads-Booster proviennent entierement de vos propres donnees historiques, donc chaque utilisateur obtient des resultats differents. C'est un consultant, pas un ghostwriter. C'est la cle pour construire une strategie de contenu sur Threads qui correspond reellement a votre audience.

**Q : Cela garantit-il que mes publications deviendront virales ?**
Non. L'algorithme de Threads est un systeme extremement complexe, et aucun outil ne peut garantir des publications virales. Ce que fait AK-Threads-Booster, c'est vous aider a prendre de meilleures decisions basees sur vos propres donnees historiques, a eviter les red lines connues de l'algorithme, et a ameliorer la probabilite que chaque publication performe bien grace a une analyse psychologique et pilotee par les donnees. C'est le skill de creation de contenu pour Threads le plus complet disponible actuellement, mais les facteurs qui determinent si une publication devient virale -- le timing, la pertinence du sujet, l'etat de l'audience, la logique de distribution de l'algorithme a ce moment -- sont trop nombreux pour qu'un outil les controle entierement. Considerez-le comme votre consultant en donnees, pas comme une machine a garantir la viralite.

---

## Structure des repertoires

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

## Licence

MIT License. Voir [LICENSE](./LICENSE).
