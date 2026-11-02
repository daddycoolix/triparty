# Triparty data collection

Runs data collection for new Triparty cities on GitHub Actions, because the Claude build environment cannot reach OpenStreetMap directly.

- `collect/collect.py`: the collector (Overpass with 4 endpoints and retries, Wikidata, Wikivoyage, Nominatim).
- `jobs/<city>.json`: what to collect for a city (written by the city build).
- `data/<city>/`: results, committed by the workflow.

Trigger: Actions > collect > Run workflow (job = city), or from the API:
`gh api repos/<owner>/triparty/actions/workflows/collect.yml/dispatches -f ref=main -f inputs[job]=<city>`
