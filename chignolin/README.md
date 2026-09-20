# Chignolin

Inputs, trained models, and simulation files for the chignolin folding benchmarks used in the SelfTICA study.

## Contents

| Path | Description |
| --- | --- |
| `common/` | Canonical shared simulation inputs |
| `data/` | Structures and simulation data |
| `models/SelfTICA/` | Trained SelfTICA models |
| `models/DeepTICA/` | DeepTICA reference models |
| `run_biased_explore/` | OPES-Explore simulations using learned collective variables |
| `plumed-descriptors.dat` | Descriptor definitions used for training and analysis |

Run simulations from their original directories so that relative paths to models, structures, and PLUMED inputs remain valid.

For dependencies and reproduction notes, see the [reproduction guide](../docs/REPRODUCIBILITY.md).
