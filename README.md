# DaTaskScheduler — Edbert Lim

A compact, deliberately minimal command-line task scheduler built as a demonstrable exercise in software engineering fundamentals: explicit data modeling, defensive validation, clear separation of concerns, and reproducible tests. This repository is part of my application to NUS and NTU; it is intended to show how I reason about correctness, migration, and tradeoffs under real constraints.


## What this project actually solves

Students and short-term project teams need a reliable, local way to record small tasks and deadlines without installing or wiring up complex tools. DaTaskScheduler provides a single-user, local CLI for adding tasks with validated due dates, listing tasks sorted by due date, and removing tasks by either a stable internal identifier or by name (with ambiguity protection). The tool yields a reproducible, test-covered core that can be inspected and reasoned about in under five minutes.


## Problem definition (precise)

* Input errors (bad dates, accidental whitespace) silently corrupt data or cause crashes in many quick scripts.
* Schema changes (adding IDs) without migration lose provenance or create inconsistent state.
* Ambiguous deletion by human-facing names leads to accidental data loss.

DaTaskScheduler addresses these problems by:

* enforcing strict date validation (`YYYY-MM-DD` calendar correctness),
* assigning stable UUIDs to every task and migrating older entries safely in-memory,
* refusing ambiguous delete-by-name operations and requiring an explicit ID when necessary,
* providing deterministic persistence to a local JSON file.


## High-level system overview

Files to know:

* `src/main.py` — CLI entry and command handling (`add`, `list`, `delete <id>`, `delete-name <title>`).
* `src/task.py` — central task model and validation (title trimming, due-date parsing).
* `src/storage.py` — storage layer; defensive loading and saving of `data/tasks.json` and in-memory migration of missing IDs.
* `src/provenance.py` — analytic layer that computes deterministic signatures for tasks (trigram shingling + simple phonetic mapping + folded hash) and produces `data/profile.json` (experimental; read-only analysis).
* `tests/` — unit tests covering model rules, storage round-trip, delete semantics, and provenance functions.

User-facing control flow:

1. `python src/main.py add` — interactive: prompts for title and due date, validates, persists.
2. `python src/main.py list` — prints tasks sorted by due date (earliest first; “no date” last).
3. `python src/main.py delete <id>` — removes task with exact id.
4. `python src/main.py delete-name "<title>"` — deletes by name only when exactly one exact case-insensitive match exists.


## Key technical decisions and justification

1. **Centralize validation in the model (`src/task.py`)**
   Validation belongs with the data it constrains. This keeps the CLI layer responsible only for I/O and re-prompting, and it prevents duplicated or inconsistent checks.

2. **Isolate file I/O (`src/storage.py`)**
   JSON persistence is simple and auditable for this scope. Keeping storage separate makes migration and error handling explicit and simplifies testing.

3. **Use UUIDs for stable identity and migrate safely**
   Names are human-friendly but ambiguous; UUIDs make operations unambiguous. Migration occurs on load (if an object lacks `id`) and becomes permanent on next save.

4. **Strict due-date validation (`YYYY-MM-DD`)**
   Accepting malformed dates breaks sorting and user expectations. The model raises on invalid dates; the CLI retries input. This prefers explicit correctness over silent correction.

5. **Delete-by-name only with explicit ambiguity checks**
   Convenience is provided while protecting against accidental mass deletion. If multiple matches exist, the system refuses and asks for an ID.

6. **Provenance experiment (`src/provenance.py`)**
   A deterministic analytic layer creates compact signatures and a distributional profile for the task set. It is an experiment in reproducibility and does not alter runtime behavior.


## Constraints and tradeoffs

* **Local-first and single-user**: no database, no sync. This keeps behavior deterministic and the code reviewable but limits multi-device workflows.
* **No task editing**: editing is intentionally out of scope to keep the model simple and auditable.
* **Explicit validation**: rejecting invalid input increases friction but substantially reduces silent errors and ambiguity—chosen deliberately for clarity.
* **JSON persistence**: human-readable and sufficient at this scale; not suitable for concurrent access or very large data volumes without modification.


## Results and what the code demonstrates

* **Robustness to common failures**: file-not-found, corrupt JSON, invalid date strings, and missing IDs are handled explicitly.
* **Deterministic schema migration**: the system augments legacy records with IDs on load and persists them safely.
* **Test-covered core logic**: unit tests validate the model, storage behavior, delete semantics, and provenance functions.
* **Reproducible analytic output**: `src/provenance.py` produces `data/profile.json`, a deterministic fingerprint and summary of the task dataset suitable for reproducibility checks.


## What this project cannot (yet) do

* Not a production task manager: no authentication, no server, no concurrent writes, no syncing.
* No in-app task editing or recurring schedules.
* Not optimized for very large datasets; JSON persistence is a deliberate pragmatic choice.
* The provenance layer is analytic, not a cryptographic proof of authorship.


## How to run and inspect (exact commands)

From the repository root:

1. Requirements

   * Python 3.8+ (3.10+ recommended). No external packages required.

2. CLI usage

   ```bash
   # add a task (interactive)
   python -m src.main add

   # list tasks (sorted by due date)
   python -m src.main list

   # delete by id
   python -m src.main delete <task_id>

   # delete by name (works only when exactly one match)
   python -m src.main delete-name "My Homework"
   ```

3. Tests

   ```bash
   python -m unittest discover tests -v
   ```

4. Provenance/profile (optional analytic step)

   ```bash
   python -m tools.generate_profile
   # generates data/profile.json and data/profile_summary.txt
   ```

Notes:

* Tasks are stored in `data/tasks.json`. Back up before experiments if needed.
* The provenance tool reads task and metadata files; it does not modify tasks.


## Documentation pointers (where to read in the code)

* `src/task.py` — read this first to understand validation rules and the exact model shape.
* `src/storage.py` — shows file-path resolution, defensive loading, and migration behavior.
* `src/main.py` — demonstrates CLI control flow, re-prompting for invalid input, and command parsing.
* `tests/` — the tests are the executable specification of expected behavior.
* `src/provenance.py` — documents the analytic approach to deterministic signatures and the repository profile.


## Closing note

This project is an exercise in reasoning under constraints: choose explicit rules, handle failure modes visibly, and keep interfaces minimal and testable. If you trace the code and run the tests, you will see the design story unfold: centralized validation, contained I/O, safe migration, and a small reproducible experiment. I welcome critique on any tradeoff — that interrogation is how better designs are found.

— Edbert Lim
