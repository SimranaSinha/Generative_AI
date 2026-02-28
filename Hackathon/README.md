# World Cup 2026 — Squad Builder

A fully grounded, multi-step LangChain reasoning pipeline that builds a 23-player FIFA World Cup squad from real football statistics. Available as both an interactive Jupyter Notebook and a Streamlit chat application.

---

## Overview

This project was built for the **World Cup GenAI Hackathon**. It takes a natural-language description of desired playing style and tactical criteria, retrieves the best-matching players from a real FBRef statistics dataset using semantic search, applies World Cup roster rules, and generates LLM-backed justifications for every selection — all presented in an interactive analytics dashboard.

---

## Project Structure

```
.
├── squad_builder.ipynb           # Full 6-tool LangChain pipeline (notebook)
├── app.py                        # Streamlit chat UI (standalone app)
├── squad_builder.html            # Exported notebook HTML
├── requirements.txt              # Python dependencies
├── .env                          # API keys (not committed)
├── datasets/
│   └── players_data-2024_2025.csv  # FBRef 2024-25 player statistics
├── faiss_index/
│   ├── index.faiss               # FAISS vector index (auto-generated)
│   └── index.pkl                 # FAISS metadata store (auto-generated)
├── cache/                        # Disk-cached HTTP responses + user preferences
└── problemstatement/
    └── World Cup GenAI Hackathon.pdf
```

---

## Dataset

| Property | Detail |
|---|---|
| Source | FBRef — 2024-25 season across 5 major European leagues |
| File | `datasets/players_data-2024_2025.csv` |
| Total rows | 2,854 |
| Unique players | 2,702 |
| Columns | 267 (multi-table merge across standard stats, shooting, passing, defense, possession, GK, misc) |
| Leagues covered | Premier League, La Liga, Serie A, Ligue 1, Bundesliga |

**Key columns used by the pipeline:**

| Column | Description |
|---|---|
| `Player`, `Nation`, `Pos`, `Squad`, `Comp`, `Age` | Identity |
| `Gls`, `Ast`, `G+A`, `xG`, `xAG` | Attacking output |
| `PrgC`, `PrgP`, `PrgR` | Progressive carries/passes/receptions |
| `SCA`, `GCA` | Shot/goal creating actions |
| `Tkl`, `Int`, `Clr` | Defensive actions |
| `MP`, `Starts`, `Min` | Playing time |
| `GA90`, `Save%`, `CS%` | Goalkeeper metrics |
| `MarketValue` | Derived heuristic (computed at load time) |

**Derived `MarketValue` formula:**
```python
MarketValue = (Goals * 2.5) + (Assists * 1.5) + (xG * 1.0) + (SCA * 0.05)
            + (Tackles * 0.1) - (Age - 24).clip(-5, 5) * 1.2
            + (Minutes / 90) * 0.3 + 5
```

---

## Architecture

### 1. Jupyter Notebook — 6-Tool LangChain Agent Pipeline

The notebook implements a sequential reasoning pipeline using six LangChain `@tool`-decorated functions, wired into a `STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION` agent with `ConversationBufferMemory`.

```
[User Criteria + Budget]
         |
    Tool 1: dataset_discovery_tool
         | Catalogues local files and external API/web sources
    Tool 2: data_ingestion_tool
         | Loads CSV, scrapes Wikipedia WC 2026, queries API-Football
    Tool 3: retrieval_or_filter_tool
         | Builds FAISS vector store, runs semantic search per position
    Tool 4: reasoning_or_aggregation_tool
         | Applies 23-player rule, position slots, budget cap, ranks by score
    Tool 5: llm_synthesis_tool
         | LLM chain generates per-player justifications + tactical summary
    Tool 6: report_generation_tool
         | Formatted report + 4 interactive Plotly charts
         |
   [23-Player Squad + Analytics]
```

**Tool details:**

| # | Tool | Responsibility |
|---|---|---|
| 1 | `dataset_discovery_tool` | Inventories local datasets and external data sources with cited URLs |
| 2 | `data_ingestion_tool` | Loads the FBRef CSV, scrapes FIFA WC 2026 Wikipedia context, optionally queries API-Football (RapidAPI) |
| 3 | `retrieval_or_filter_tool` | Converts players to natural-language descriptions, builds/loads FAISS index, runs semantic similarity search per position |
| 4 | `reasoning_or_aggregation_tool` | Enforces World Cup roster rules: exactly 3 GK, 5-7 DF, 5-8 MF, 4-6 FW, total ≤ 23; applies optional budget cap; ranks by composite score |
| 5 | `llm_synthesis_tool` | Calls `LLMChain` with a structured prompt to produce stat-grounded justifications for each player and a tactical summary |
| 6 | `report_generation_tool` | Renders header card, calls `display(Markdown(...))`, and produces 4 Plotly figures |

**World Cup roster constraints enforced:**

| Position | Min | Max |
|---|---|---|
| GK | 3 | 3 |
| DF | 5 | 7 |
| MF | 5 | 8 |
| FW | 4 | 6 |
| **Total** | — | **23** |

**Composite scoring formula:**
```python
score = (goals * 2.5) + (assists * 1.8) + (xg * 1.2) + (xag * 1.0)
      + (sca * 0.12) + (prgp * 0.08)
      + (tackles * 0.25) + (interceptions * 0.25)
```

### 2. Streamlit App — Chat UI

`Stream-lit-squad-builder.py` is a standalone Streamlit application that wraps a simplified version of the same pipeline behind a conversational interface. It does **not** depend on the notebook's global state — they share only the FAISS index on disk.

**App flow:**
1. User enters OpenAI API key and uploads/paths to the FBRef CSV in the sidebar.
2. Clicking **Load Data & Build Index** runs `build_vector_store` (cached via `@st.cache_resource`) — builds or loads the FAISS index.
3. User types squad criteria in the chat input. The app detects intent (squad build vs. general question) by keyword matching.
4. Squad builds trigger `run_squad_pipeline` → `retrieve_candidates` → `build_squad` → `llm_justify` → `make_charts`.
5. The full analytics dashboard renders below the chat.

**Sidebar features:**
- OpenAI API key input (password field)
- CSV file uploader or local path input
- Dataset statistics (player count, league count, position breakdown)
- 5 quick-prompt buttons for common tactical archetypes

**Analytics dashboard (post-build):**
- Constraint status badges (position slot compliance)
- 5 summary stat cards (squad size, total value, avg goals, avg xG, avg age)
- 4 Plotly charts (see Charts section below)
- Full sortable squad table with position badges

---

## Data Sources

| Source | Method | Purpose |
|---|---|---|
| `datasets/players_data-2024_2025.csv` | Local CSV load | Primary player statistics (FBRef, 5 leagues) |
| [Wikipedia — 2026 FIFA World Cup](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup) | BeautifulSoup4 HTML scraping | Tournament context for LLM prompt |
| [API-Football (RapidAPI)](https://rapidapi.com/heisenbug/api/free-api-live-football-data) | REST API (free tier) | Player search, live scores, league catalogue |

All HTTP responses are disk-cached under `cache/` (keyed by MD5 of URL, TTL configurable per call). The Wikipedia page has a 72-hour TTL; API responses use 24 hours by default.

---

## Memory & Persistence

The notebook maintains a `SquadBuilderMemory` class backed by `cache/user_preferences.json`:

- **`criteria_history`** — rolling log of the last 5 squad criteria strings with timestamps
- **`budget_preference`** — most recently used budget cap
- **`squad_history`** — summaries of the last 3 squads built

This is separate from the LangChain `ConversationBufferMemory` that tracks the agent's chat history.

---

## Visualisations

All charts are built with **Plotly** and use a dark theme (`paper_bgcolor="#161b22"`).

| Chart | Type | Content |
|---|---|---|
| 1 | Bar chart | Market value per player, coloured by position |
| 2 | Pie chart | Budget split by position group |
| 3 | Radar chart | Average stat profile — Forwards vs Defenders (Goals, Assists, xG, SCA, Tackles, Interceptions) |
| 4 | Histogram | Squad age distribution by position |

The notebook also includes two additional innovation charts:

| Chart | Type | Content |
|---|---|---|
| Multi-scenario comparison | Grouped bar | Avg Goals, Assists, xG, Tackles, SCA across 3 tactical scenarios |
| Explainability overlay | Horizontal bar | Percentile rank of individual players vs the full dataset on 7 key metrics |

---

## Installation

### Prerequisites

- Python 3.10+
- An OpenAI API key (`gpt-4o-mini` or `gpt-4o`)
- Optionally a RapidAPI key for API-Football live data

### Setup

```bash
# Clone or download the project
cd <project-directory>

# Create and activate a virtual environment
python3 -m venv spovenv
source spovenv/bin/activate       # macOS/Linux
# spovenv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-proj-...
RAPIDAPI_KEY=your-rapidapi-key-here   # optional
```

---

## Running the Notebook

```bash
jupyter notebook squad_builder.ipynb
```

1. Run **Cell 0 (Setup & Imports)** through **Cell 4 (Configuration)** to set your criteria and budget.
2. Run all cells sequentially — each tool cell prints its own status output.
3. To re-run with different criteria, edit `USER_CRITERIA` / `BUDGET` in the config cell and re-execute from **Cell 12** onwards, or call `run_pipeline(criteria="...", budget=None)` directly from Cell 25.

**Key configuration (Cell 4):**

```python
USER_CRITERIA = "fast defenders with high interceptions, clinical strikers with xG > 5, creative midfielders"
BUDGET        = None          # e.g. 400.0 for a €400M cap, None for unlimited
LLM_MODEL     = "gpt-4o-mini"
DATA_PATH     = "datasets/players_data-2024_2025.csv"
```

---

## Running the Streamlit App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

**First-time setup in the sidebar:**
1. Enter your OpenAI API key.
2. Upload the FBRef CSV or paste the local path (`datasets/players_data-2024_2025.csv`).
3. Click **Load Data & Build Index** (builds the FAISS index — takes 1-2 minutes on first run; subsequent runs load from disk instantly).
4. Type your squad criteria in the chat box and click **Send**.

**Example prompts:**
- `"Build a squad with clinical strikers with xG > 10 and fast defenders with high interceptions"`
- `"Give me a budget squad under €400M with the best young talent under 25"`
- `"Defensive fortress — high save% keepers, dominant defenders with most tackles"`
- `"High-press forwards, box-to-box midfielders, aggressive full-backs"`

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `langchain` | 0.3.14 | Core LangChain framework, chains, memory, agents |
| `langchain-openai` | 0.3.1 | `ChatOpenAI`, `OpenAIEmbeddings` |
| `langchain-community` | 0.3.14 | `FAISS` vector store integration |
| `faiss-cpu` | 1.9.0 | Semantic similarity search index |
| `openai` | 1.59.6 | OpenAI API client |
| `pandas` | 2.2.3 | Data loading, manipulation, filtering |
| `plotly` | 5.24.1 | Interactive charts |
| `tiktoken` | 0.8.0 | Token counting for LLM context management |
| `beautifulsoup4` | 4.12.3 | HTML scraping (Wikipedia) |
| `lxml` | 5.3.0 | HTML parser backend for BeautifulSoup |
| `requests` | 2.32.3 | HTTP client for external data sources |
| `python-dotenv` | 1.0.1 | `.env` file loading |
| `streamlit` | — | Web UI framework (install separately if needed) |
| `ipywidgets` | 8.1.5 | Notebook widget support |
| `nbformat` | 5.10.4 | Notebook format utilities |

---

## FAISS Index

The FAISS index is built the first time the pipeline runs and saved to `faiss_index/`. It is shared between the notebook and the Streamlit app — if you build the index in the notebook, the Streamlit app will load it directly without rebuilding.

Each player is embedded as a natural-language description, for example:
```
Erling Haaland is a FW for Manchester City, age 24, 31 matches (2790 mins).
Goals=27, Assists=5, xG=24.3, xAG=3.1. Tackles=12, Interceptions=4, SCA=48.
ProgCarries=89, ProgPasses=21. Market value ~€62.4M.
```

Embeddings are generated using `OpenAIEmbeddings` (`text-embedding-ada-002`). The index stores full metadata for all players and supports cosine similarity search.

---

## Multi-Scenario Comparison (Notebook)

The notebook includes a pre-built comparison across three tactical archetypes:

| Scenario | Focus | Budget |
|---|---|---|
| Attacking Blitz | Highest goals + xG strikers, pacey wingers, attacking midfielders | Unlimited |
| Defensive Fortress | Most tackles/interceptions defenders, sweeper keepers (high Save%), disciplined midfielders | Unlimited |
| Value XI | Best G+A per minute, young talent under 26, efficient performers | €150M cap |

A grouped bar chart compares Avg Goals, Assists, xG, Tackles, and SCA across all three squads.

---

## Explainability (Notebook)

For any selected player, the `explainability_overlay` function plots their percentile rank across 7 metrics (Goals, Assists, xG, SCA, Tackles, Interceptions, Progressive Passes) compared to the full 2,702-player dataset. Bars below the 50th percentile are shown in red; above in green.

---

## Limitations

- Player statistics are sourced from the **5 major European leagues only** — players from other leagues (MLS, Liga MX, Saudi Pro League, etc.) are not in the dataset.
- **Market value is heuristic-based**, derived from stats, not official transfer market valuations.
- **International tournament performance** is not factored in — club form is used as a proxy.
- The FAISS semantic search matches on natural-language player descriptions; niche statistical criteria may not retrieve optimally without exact column filters.
- The free tier of API-Football has limited endpoints; live match data and full squad history are not available without a paid key.

---

## License

This project was developed for the World Cup GenAI Hackathon. See `problemstatement/World Cup GenAI Hackathon.pdf` for the original problem statement.
