# Alanine dipeptide

Inputs, trained models, and simulation files for the alanine dipeptide benchmarks used in the SelfTICA study.

## Contents

| Path | Description |
| --- | --- |
| `common/` | Canonical shared simulation inputs used to prepare individual runs |
| `data/` | Structural and simulation data |
| `models/` | Trained SelfTICA models, including temperature- and lag-time-dependent models |
| `run_unbiased/` | Unbiased simulations at different temperatures |
| `run_biased_multi/` | Multithermal and biased-sampling calculations |
| `templates/` | Templates used to generate repeated FNN and GNN PLUMED inputs |
| `experiments.csv` | Definitions of generated alanine experiments |
| `plumed-descriptors.dat` | Descriptor definitions used for model training and analysis |

Some run inputs are generated from the canonical files and templates. From the repository root, use

```bash
python scripts/prepare_runs.py --list
python scripts/prepare_runs.py --run alanine/...
```

before launching a generated run.

For software requirements, launch commands, and input conventions, see the [reproduction guide](../docs/REPRODUCIBILITY.md).
