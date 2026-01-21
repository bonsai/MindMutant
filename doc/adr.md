# Decisions

## 1. Document Separation (2026-01-21)
- **Decision**: Separate documentation into `readme.md` (overview), `doc/spec.md` (specifications), `doc/stack.md` (tech stack), and `doc/adr.md` (decisions).
- **Reason**: To improve maintainability and clarity as the project grows.

## 2. Data Format Unification (2026-01-21)
- **Decision**: Use JSON for all data storage (`data/g{n}/*.json`).
- **Reason**: To ensure consistency and ease of parsing/manipulation.

## 3. Renaming (2026-01-21)
- **Decision**: Rename `ideagen_ga` to `gen`, `engine.py` to `evolution.py`, `GAEngine` to `Evolution`, and `cloud` to `wordcrowd`.
- **Reason**: To use more biological/evolutionary terminology and clear naming.

## 4. Responsibility Separation (2026-01-21)
- **Decision**: Split `evolution.py` into `Repository` (I/O), `Analyzer` (Analysis), `Breeder` (Mating/Constraints), and `Starvation` (Disaster).
- **Reason**: To adhere to Single Responsibility Principle and improve testability/modularity.

## 5. Novelty Visualization (2026-01-21)
- **Decision**: Use `wordcrowd` (tag cloud) to visualize generations, with word size/color representing Novelty (surprisingness).
- **Reason**: To provide immediate visual feedback on the "creativity" of the generated ideas.

## 6. Disaster Event (2026-01-21)
- **Decision**: Implement a "Disaster" event that kills 50% of the population every 3 generations (or manually triggered via `--die`). Selection is based on low Novelty (boring ideas die).
- **Reason**: To introduce environmental pressure and prevent stagnation/overpopulation.

## 7. Framework Adoption (2026-01-21)
- **Decision**: Adopt `DEAP` for Genetic Algorithm logic and `Streamlit` for visualization/dashboard.
- **Reason**:
    - **DEAP**: Standard, robust library for evolutionary computation, replacing custom implementation for better maintainability and extensibility.
    - **Streamlit**: Rapid prototyping of data apps to visualize word clouds and control the evolution process interactively.

## 8. Local Visualization Server (2026-01-21)
- **Decision**: Serve `data/` directory via a local Python HTTP server and embed `wordcrowd.html` in Streamlit dashboard via `iframe`.
- **Reason**: To properly render complex HTML/JS visualizations (like WordCloud) within the Streamlit interface without path/CORS issues, and to decouple visualization serving from the dashboard logic.

## 9. Legacy Freeze & Refactoring (2026-01-21)
- **Decision**: Freeze the custom GA implementation into `gen/.ga` (hidden archive) and consolidate the active DEAP implementation into `gen/deap/`.
- **Reason**: To clarify the active codebase, reduce confusion, and officially transition to the DEAP-based engine while preserving legacy code for reference.
