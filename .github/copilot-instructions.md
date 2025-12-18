<!-- Short, actionable instructions for AI coding assistants working on this repo -->
# Copilot instructions — projet-opendata-ia

Purpose: Help AI agents quickly understand the app, common workflows, conventions, and safe edit areas.

- Quick start (dev):
  - Install deps: `uv sync`
  - Create env: copy `env.example` / `env.example.txt` -> `.env` and set provider keys.
  - Run locally (preferred):
    - If using Ollama: start `ollama serve` then `uv run streamlit run app.py`
    - Otherwise set `NUTRISCAN_PROVIDER` and run `uv run streamlit run app.py`

- Big picture (files to read first):
  - `app.py`: Streamlit UI, routing (Recherche / Comparateur / Chatbot) and heavy CSS. Most UI changes happen here.
  - `utils/chatbot.py`: `NutriChatbot` wraps `litellm.completion` and implements `analyze_product`, `suggest_alternatives`, `chat`.
  - `utils/data.py`: `OpenFoodFactsAPI` — search/get product and `extract_product_info()` (defines product dict shape).
  - `utils/charts.py`: Plotly chart builders and the `COLORS` palette used across the UI.
  - `pyproject.toml` and `README.md` for dependency and run guidance.

- Important runtime conventions & integrations:
  - Multi-provider LLMs: provider selected via `NUTRISCAN_PROVIDER` (openai | gemini | ollama). Models configured by `NUTRISCAN_MODEL_*` env vars.
  - LiteLLM (`litellm.completion`) is used directly in `utils/chatbot.py`.
  - External APIs: OpenFoodFacts (requests); optional local Ollama endpoint (`OLLAMA_API_BASE`).
  - Streamlit `st.session_state` stores `chat_history`, `comparison_products`, and `chatbot` instance — preserve keys and shapes when modifying state handling.

- Data shapes & expectations (use exact keys):
  - `extract_product_info()` returns a product dict with keys: `name`, `brands`, `nutriscore`, `nova_group`, `image_url`, `ingredients`, `allergens`, `nutriments`, `categories`, `code`.
  - Chart functions expect `nutriments` to have `proteins_100g`, `carbohydrates_100g`, `fat_100g`, `fiber_100g` (fallbacks handled).
  - `create_comparison_chart(products)` expects a list of product dicts with `name` and `nutriscore`.

- Code style and edit guidance (project-specific):
  - UI-heavy edits belong in `app.py`. Keep large CSS blocks intact unless intentionally redesigning the theme.
  - Palette and Plotly theming: modify `utils/charts.py::COLORS` to change colors globally.
  - LLM prompts live in `utils/chatbot.py` — keep prompt structure focused and concise; errors are returned as short strings (e.g. "❌ Erreur...").
  - Avoid renaming `NutriChatbot` methods or changing the `completion(...)` call signature without updating `app.py` usage.

- Developer workflows and debugging tips:
  - Reproduce the app locally with `uv run streamlit run app.py` and watch logs for exceptions in the terminal.
  - If debugging LLM calls with Ollama, ensure `OLLAMA_API_BASE` points to the running server (`http://localhost:11434`).
  - Network/API failures are handled by printing/returning simple messages (look at `utils/data.py` and `utils/chatbot.py` for try/except patterns).

- Safe refactor opportunities:
  - Extract smaller UI components from `app.py` (e.g., product card rendering) but preserve `st.session_state` keys and notebook-style rerun semantics.
  - Centralize prompt templates into `utils/chatbot.py` if adding variants, and keep default temperature values nearby.

- Where to look for missing documentation or tests:
  - No tests currently; changes touching LLM prompts or public functions should be smoke-tested by running the Streamlit app and exercising the three pages.

If anything above is unclear or you want the instructions to include extra examples (prompts, typical bug patterns, or more file links), tell me which area to expand.
