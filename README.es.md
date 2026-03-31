[繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Português](README.pt.md) | [हिन्दी](README.hi.md) | [Bahasa Indonesia](README.id.md) | [ภาษาไทย](README.th.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Tiếng Việt](README.vi.md)

# AK-Threads-Booster

Una skill open-source de Claude Code y asistente de escritura con IA disenada especificamente para creadores de contenido en Threads. Analiza tus datos historicos de publicaciones, aplica investigacion en psicologia de redes sociales y conocimiento del algoritmo de Threads para ofrecerte analisis personalizado de escritura, perfil de Brand Voice y asistencia en la creacion de borradores.

Si vienes de Twitter/X y quieres entender como funciona Threads, si buscas una herramienta IA para redes sociales que aprenda de tus propios datos, o si necesitas una estrategia de contenido respaldada por metricas reales para crecer en Threads, este proyecto es para ti. No es una plantilla. No es un conjunto de reglas. Es un consultor que te ayuda a entender el algoritmo de Threads y convertir tus datos en engagement real. Funciona como skill / plugin para Claude Code, Cursor, Codex, Windsurf, GitHub Copilot y Google Antigravity.

---

## Que Es AK-Threads-Booster

AK-Threads-Booster es una skill open-source para Threads. No es una plantilla de publicaciones, no es un conjunto de reglas, y no es un creador de contenido IA que te reemplaza.

Es un sistema metodologico que hace tres cosas:

1. **Analiza tus datos historicos** para identificar que contenido genera mayor engagement en Threads en tu cuenta
2. **Usa psicologia y conocimiento del algoritmo de Threads como lentes analiticas** para explicar por que ciertas publicaciones funcionan mejor
3. **Presenta los hallazgos de forma transparente** para que tu decidas el siguiente paso

Cada usuario obtiene resultados diferentes porque cada cuenta tiene una audiencia, un estilo y un dataset distinto. Esa es la diferencia fundamental entre una estrategia de contenido basada en datos y los consejos genericos de redes sociales.

### El Contexto Latinoamericano

La comunidad hispanohablante en Threads tiene una energia particular. Comparte con Brasil esa cultura de alta interaccion, pero con un enfoque distinto: mas peso en la expresion escrita, mas gusto por el contenido con profundidad, y una relacion compleja con la autenticidad. Muchos creadores llegan desde Twitter/X con habitos y estrategias que no necesariamente funcionan igual en Threads, y el proceso de adaptacion no siempre es obvio.

Los desafios mas comunes para creadores en espanol:

- **Transicion desde Twitter/X**: Las mecanicas son diferentes. Lo que funcionaba alla no siempre funciona aca, y entender por que requiere datos, no intuicion
- **Construir una imagen profesional**: En un entorno donde todos parecen informales, como destacar sin parecer rigido ni perder autenticidad
- **Detectar contenido con sabor a IA**: La audiencia hispanohablante es sensible a lo artificial. Si tu texto suena a maquina, la gente lo nota

AK-Threads-Booster ataca estos puntos desde los datos de tu propia cuenta, no desde consejos genericos.

---

## Principios Fundamentales

**Consultor, no profesor.** AK-Threads-Booster no te va a decir "deberias escribir asi." Te va a decir "cuando hiciste esto antes, los datos mostraron esto -- queda a tu criterio." Sin calificaciones, sin correcciones, sin ghostwriting.

**Basado en datos, no en reglas.** Todas las sugerencias vienen de tus propios datos historicos, no de una lista generica de "10 Tips de Marketing Digital." Cuando los datos son insuficientes, el sistema te lo dice honestamente en lugar de fingir seguridad.

**Las red lines son las unicas reglas fijas.** Solo los comportamientos que el algoritmo de Meta penaliza explicitamente (engagement bait, clickbait, republicaciones con alta similitud, etc.) generan advertencias directas. Todo lo demas es consultivo. Tu siempre tienes la ultima palabra.

---

## Soporte Multi-Herramienta

AK-Threads-Booster funciona con multiples herramientas de codificacion con IA. Claude Code ofrece la experiencia completa con 7 Skills; otras herramientas ofrecen las capacidades de analisis principal.

### Herramientas Soportadas y Archivos de Configuracion

| Herramienta | Ubicacion del Archivo | Alcance |
|-------------|----------------------|---------|
| **Claude Code** | directorio `skills/` (7 Skills) | Funcionalidad completa: setup, voice, analyze, topics, draft, predict, review |
| **Cursor** | `.cursor/rules/ak-threads-booster.mdc` | Analisis principal (4 dimensiones) |
| **Codex** | `AGENTS.md` (raiz) | Analisis principal (4 dimensiones) |
| **Windsurf** | `.windsurf/rules/ak-threads-booster.md` | Analisis principal (4 dimensiones) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Analisis principal (4 dimensiones) |
| **Google Antigravity** | directorio `.agents/` + `AGENTS.md` en raiz | Analisis principal (4 dimensiones) |

### Diferencias de Funcionalidad

- **Claude Code**: Funcionalidad completa incluyendo inicializacion (setup), perfil de Brand Voice (voice), analisis de escritura (analyze), recomendacion de temas (topics), asistencia de borrador (draft), prediccion de publicacion viral (predict) y revision post-publicacion (review) -- siete Skills independientes
- **Otras herramientas**: Analisis de escritura principal con cuatro dimensiones (comparacion de estilo, analisis psicologico, verificacion de alineacion con algoritmo, deteccion de tono IA), compartiendo la misma base de conocimiento (directorio `knowledge/`)
- **Google Antigravity**: Lee tanto el `AGENTS.md` en raiz (normas de consultor y reglas de red line) como el directorio `.agents/` (archivos de reglas + skills de analisis)

Todas las versiones incluyen:
- Guias de tono consultivo (sin calificaciones, sin correcciones, sin ghostwriting)
- Reglas de red line del algoritmo (advertencia al detectar)
- Referencias de la base de conocimiento (psicologia, algoritmo, deteccion de tono IA)

---

## Instalacion

### Opcion 1: Instalar via GitHub

```bash
# En el directorio de tu proyecto Claude Code
claude install-plugin https://github.com/akseolabs-seo/AK-Threads-booster
```

### Opcion 2: Instalacion Manual

1. Clona este repositorio localmente:
   ```bash
   git clone https://github.com/akseolabs-seo/AK-Threads-booster.git
   ```

2. Copia el directorio `AK-Threads-booster` en el `.claude/plugins/` de tu proyecto Claude Code:
   ```bash
   cp -r AK-Threads-booster /ruta/a/tu/proyecto/.claude/plugins/
   ```

3. Reinicia Claude Code. Las Skills se detectaran automaticamente.

### Otras Herramientas

Si usas Cursor, Windsurf, Codex o GitHub Copilot, simplemente clona el repositorio en el directorio de tu proyecto. Cada herramienta leera automaticamente su archivo de configuracion correspondiente.

---

## Inicializacion

Antes del primer uso, ejecuta la inicializacion para importar tus datos historicos:

```
/setup
```

La inicializacion te guia a traves de:

1. **Elegir un metodo de importacion de datos**
   - Meta Threads API (busqueda automatica)
   - Exportacion de cuenta Meta (descarga manual)
   - Proporcionar archivos de datos existentes directamente

2. **Analisis automatico de publicaciones historicas**, generando tres archivos:
   - `threads_daily_tracker.json` -- Base de datos de publicaciones historicas
   - `style_guide.md` -- Guia de estilo personalizada (tus preferencias de Hook, rangos de conteo de palabras, patrones de cierre, etc.)
   - `concept_library.md` -- Biblioteca de conceptos (rastrea conceptos que ya has explicado a tu audiencia)

3. **Reporte de analisis** mostrando las caracteristicas de estilo de tu cuenta y panorama de datos

La inicializacion solo necesita ejecutarse una vez. Las actualizaciones de datos posteriores se acumulan a traves del modulo `/review`.

---

## Las Siete Skills

### 1. /setup -- Inicializacion

Ejecuta en el primer uso. Importa publicaciones historicas, genera tu guia de estilo y construye la biblioteca de conceptos.

```
/setup
```

### 2. /voice -- Perfil de Brand Voice

Analisis profundo de todas las publicaciones historicas y respuestas a comentarios para construir un perfil de Brand Voice completo. Va mas alla de la guia de estilo de `/setup`, cubriendo preferencias de estructura de oraciones, cambios de tono, estilo de expresion emocional, estilo de humor, frases prohibidas y mas.

```
/voice
```

Mientras mas completo sea tu Brand Voice, mas cercanos seran los resultados de `/draft` a tu estilo real de escritura. Recomendado despues de `/setup`.

Dimensiones de analisis incluyen: preferencias de estructura de oraciones, patrones de transicion de tono, estilo de expresion emocional, presentacion de conocimiento, diferencias de tono entre seguidores y criticos, analogias y metaforas comunes, estilo de humor e ingenio, auto-referencia y forma de dirigirse a la audiencia, frases prohibidas, micro-caracteristicas de ritmo de parrafo, caracteristicas de tono en respuestas a comentarios.

Salida: `brand_voice.md`, referenciado automaticamente por el modulo `/draft`.

### 3. /analyze -- Analisis de Escritura (Funcionalidad Principal)

Despues de escribir una publicacion, pega tu contenido para analisis en cuatro dimensiones:

```
/analyze

[pega el contenido de tu publicacion]
```

Cuatro dimensiones de analisis:

- **Comparacion de estilo**: Compara con tu propio estilo historico, senala desviaciones y rendimiento historico
- **Analisis psicologico**: Mecanismos de Hook, arco emocional, motivacion de compartir, senales de confianza, sesgos cognitivos, potencial de activacion de comentarios
- **Alineacion con algoritmo**: Escaneo de red lines (advertencias al detectar) + evaluacion de senales positivas
- **Deteccion de tono IA**: Escaneo de rastros de IA en los niveles de oracion, estructura y contenido

La deteccion de tono IA es especialmente relevante para la audiencia hispanohablante. Los lectores en espanol tienden a ser particularmente sensibles al contenido que suena artificial o generico, y esta dimension te ayuda a identificar exactamente donde tu texto pierde naturalidad.

### 4. /topics -- Recomendacion de Temas

Cuando no sabes que escribir a continuacion. Extrae insights de comentarios y datos historicos para recomendar temas.

```
/topics
```

Recomienda 3-5 temas, cada uno con: fuente de la recomendacion, razonamiento respaldado por datos, rendimiento de publicaciones historicas similares, rango de rendimiento estimado.

### 5. /draft -- Asistencia de Borrador

Selecciona un tema de tu banco de temas y genera un borrador basado en tu Brand Voice. Esta es la funcion mas directa de creacion de contenido IA en AK-Threads-Booster, pero el borrador es solo un punto de partida.

```
/draft [tema]
```

Puedes especificar un tema o dejar que el sistema recomiende uno de tu banco de temas. La calidad del borrador depende de que tan completos sean tus datos de Brand Voice -- ejecutar `/voice` primero hace una diferencia notable.

El borrador es un punto de partida. Necesitas editarlo y ajustarlo tu mismo. Despues de editar, ejecutar `/analyze` es recomendable.

### 6. /predict -- Prediccion de Publicacion Viral

Despues de escribir una publicacion, estima su rendimiento 24 horas despues de publicar.

```
/predict

[pega el contenido de tu publicacion]
```

Genera estimaciones conservadora/base/optimista (views / likes / replies / reposts / shares) con justificacion y factores de incertidumbre.

### 7. /review -- Revision Post-Publicacion

Despues de publicar, usa esto para recopilar datos de rendimiento real, comparar con predicciones y actualizar los datos del sistema.

```
/review
```

Lo que hace:
- Recopila datos de rendimiento real
- Compara con predicciones y analiza desviaciones
- Actualiza tracker y guia de estilo
- Sugiere horarios optimos de publicacion

---

## Base de Conocimiento

AK-Threads-Booster incluye tres bases de conocimiento integradas que sirven como puntos de referencia analitica:

### Psicologia de Redes Sociales (psychology.md)

Fuente: Compilacion de investigacion academica. Cubre mecanismos de activacion psicologica de Hook, psicologia de activacion de comentarios, motivacion de compartir y viralidad (framework STEPPS), construccion de confianza (Pratfall Effect, Parasocial Relationship), aplicaciones de sesgos cognitivos (Anchoring, Loss Aversion, Social Proof, IKEA Effect), arco emocional y niveles de activacion.

Proposito: Fundamento teorico para la dimension de analisis psicologico en `/analyze`. La psicologia es un lente analitico, no una regla de escritura.

### Algoritmo de Meta (algorithm.md)

Fuente: Documentos de patente de Meta, Facebook Papers, declaraciones de politica oficial, observaciones de KOLs (solo como complemento). Cubre lista de red lines (12 comportamientos penalizados), senales de ranking (compartir via DM, comentarios profundos, tiempo de permanencia, etc.), estrategia post-publicacion, estrategia a nivel de cuenta.

Proposito: Base de reglas para la verificacion de alineacion con algoritmo en `/analyze`. Los items de red line generan advertencias; los items de senal se presentan en tono consultivo.

### Deteccion de Tono IA (ai-detection.md)

Cubre rastros de IA a nivel de oracion (10 tipos), rastros de IA a nivel de estructura (5 tipos), rastros de IA a nivel de contenido (5 tipos), metodos de reduccion de tono IA (7 tipos), condiciones de activacion de escaneo y definiciones de severidad.

Proposito: Linea base de deteccion para el escaneo de tono IA en `/analyze`. Senala rastros de IA para que tu los corrijas; no corrige automaticamente.

---

## Flujo de Trabajo Tipico

```
1. /setup              -- Primer uso, inicializa el sistema
2. /voice              -- Perfil de Brand Voice profundo (ejecuta una vez)
3. /topics             -- Ve recomendaciones de temas
4. /draft [tema]       -- Genera un borrador
5. /analyze [post]     -- Analiza el borrador o tu propio texto
6. (Edita basandote en el analisis)
7. /predict [post]     -- Estima rendimiento antes de publicar
8. (Publica)
9. /review             -- Recopila datos 24h despues de publicar
10. Vuelve al paso 3
```

Cada ciclo hace que el analisis y las predicciones del sistema sean mas precisos. `/voice` solo necesita ejecutarse una vez (o re-ejecutarse despues de acumular mas publicaciones). `/draft` referencia automaticamente tu archivo de Brand Voice.

---

## Preguntas Frecuentes

**P: AK-Threads-Booster escribe publicaciones por mi?**
El modulo `/draft` genera borradores iniciales, pero los borradores son solo un punto de partida. Necesitas editarlos y refinarlos tu mismo. La calidad del borrador depende de que tan completos sean tus datos de Brand Voice. Los demas modulos solo analizan y aconsejan -- no hacen ghostwriting.

**P: Sirve si vengo de Twitter/X?**
Especialmente. Uno de los desafios mas comunes para creadores que migran desde Twitter/X es entender que las mecanicas de Threads son diferentes. AK-Threads-Booster analiza tus datos en Threads especificamente, asi que te muestra que funciona en esta plataforma para tu audiencia, sin que arrastres suposiciones de otra red.

**P: El analisis es preciso con pocos datos?**
No mucho. El sistema te lo dice honestamente. La precision mejora conforme los datos se acumulan.

**P: Tengo que seguir todas las sugerencias?**
No. Todas las sugerencias son solo consultivas. Tu siempre tienes la ultima palabra. Las unicas advertencias directas son para red lines del algoritmo (patrones de escritura que activan penalizacion).

**P: Detecta si mi texto suena a IA?**
Si. La dimension de deteccion de tono IA escanea tu texto en tres niveles (oracion, estructura, contenido) y senala donde suena artificial. Esto es particularmente util para creadores en espanol, donde la audiencia tiende a ser sensible al contenido generico o que suena a maquina.

**P: Soporta plataformas ademas de Threads?**
Actualmente disenado principalmente para Threads. Los principios de psicologia en la base de conocimiento son universales, pero la base de conocimiento de algoritmo se enfoca en la plataforma de Meta.

**P: Como es diferente de una herramienta de IA generica?**
Las herramientas genericas producen contenido a partir de modelos generales. El analisis y sugerencias de AK-Threads-Booster vienen completamente de tus propios datos historicos, asi que cada usuario obtiene resultados diferentes. Es un consultor, no un ghostwriter. Esa es la clave para construir una estrategia de contenido en Threads que realmente se ajuste a tu audiencia.

**P: Esto garantiza que mis publicaciones se haran virales?**
No. El algoritmo de Threads es un sistema extremadamente complejo, y ninguna herramienta puede garantizar publicaciones virales. Lo que AK-Threads-Booster hace es ayudarte a tomar mejores decisiones basadas en tus propios datos historicos, evitar red lines conocidas del algoritmo, y mejorar la probabilidad de que cada publicacion rinda bien a traves de analisis psicologico y orientado por datos. Es la skill de creacion de contenido para Threads mas completa disponible actualmente, pero los factores que determinan si una publicacion se hace viral -- timing, relevancia del tema, estado de la audiencia, la logica de distribucion del algoritmo en ese momento -- son demasiados para que cualquier herramienta los controle totalmente. Tratalo como tu consultor de datos, no como una maquina de garantizar viralidad.

---

## Estructura de Directorios

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

## Licencia

MIT License. Ver [LICENSE](./LICENSE).
