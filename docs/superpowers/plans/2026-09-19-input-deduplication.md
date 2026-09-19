# Simulation input deduplication

> For agentic workers: use `superpowers:subagent-driven-development` for independent migration and review tasks.

**Goal:** Implement the user's approved first two simplifications: shared simulation inputs and two alanine templates with an experiment manifest.

**Design:** Keep one canonical copy of each repeated simulation input in a system's `common/` directory. `scripts/shared-inputs.json` maps canonical files to their historical destinations. `alanine/experiments.csv` records all 120 experiments with columns `run_dir,architecture,method,dataset,replica,model`; model paths are repository-relative. `alanine/templates/{fnn,gnn}.dat.in` use a single `@MODEL_PATH@` placeholder. A standard-library Python CLI restores inputs into their original run directories, preserving relative paths and output isolation. Generated inputs are ignored by Git.

**Tech stack:** Python 3.9+ standard library, JSON, CSV, unittest; no simulation software needed for preparation.

**Spec:** The approved design is recorded above and in the conversation: preserve experiment identity, model files, trajectory data, numerical settings, and independent output directories.

## Constraints and interfaces

- Work in the user's current checkout; leave changes uncommitted for review.
- Do not alter models, COLVAR data, third-party force fields, or scientific parameters.
- Shared manifest format: `{"version": 1, "files": [{"source": "system/common/file", "targets": ["historical/run/file"]}]}`.
- The 120 alanine runs obtain `ala2.tpr` from `alanine/common/ala2.tpr`; these targets come from the CSV, not the shared manifest.
- CLI: `python scripts/prepare_runs.py --list`, `--check`, `--run REPO_RELATIVE_DIRECTORY`, or `--all`. Check/list never write inputs. Repeat preparation is safe; any differing existing input blocks the whole selected operation before writes. No force flag.
- Prepared content must match the original archived inputs, allowing CRLF/LF differences for text only.
- All paths must remain inside the repository, including resolved symlinks.

## Tasks

- [x] Snapshot original file hashes outside the repository; write failing behavior tests for preparation, filtering, idempotence, conflict preservation, and path containment.
- [x] Consolidate exact repeated simulation inputs, excluding models/force fields; write shared manifest and precise ignore rules. Verify copies before deleting any original.
- [x] Derive two alanine templates and a CSV from existing configurations; implement preparation CLI and remove the 120 generated source configurations after equivalence validation.
- [x] Update README/reproduction instructions with preparation commands, source locations, and conflict behavior.
- [x] Run `python -m unittest discover -s tests -v`; compare all reconstructed removed files against the original hash snapshot in a disposable copy. Review all changes and fix findings.

## Progress

- Original baseline: commit `882ad8f`, clean worktree, 609 files. Snapshot saved in the system temporary directory as `selftica-inputs-before-882ad8f.json`.
- Current checkout is used because the user asked to simplify this folder; no worktree, commit, or publishing operation is needed.
- Consolidated 178 shared input files into 18 canonical files; replaced 120 configurations with two templates and a 120-row CSV. The catalog reconstructs 298 files in 151 run directories.
- Ten behavior tests passed. In a disposable copy, `--all` created 298 inputs and a second run created zero. All 607 original files other than the two updated documentation files matched the baseline (binary exact, text normalized only for line endings).
- All 254 model, trajectory, and third-party force-field files remained byte-identical. All 298 generated destinations matched the ignore rules. Independent code and documentation reviews reported no actionable findings.
