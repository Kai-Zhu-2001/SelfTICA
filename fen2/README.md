# N₂ dissociation on Fe(111)

Inputs, trained models, and simulations for the N₂/Fe(111) dissociation benchmark.

## Contents

| Path | Description |
| --- | --- |
| `common/` | Canonical shared simulation inputs |
| `data/` | Atomic configurations and the MACE potential used by LAMMPS |
| `models/` | Exported neural-network collective-variable model |
| `run_initial/` | Initial OPES sampling |
| `run_biased_explore/` | OPES-Explore simulations using different collective variables |

These simulations use LAMMPS with PLUMED integration and the MACE pair style.

The supplied OPES-Explore inputs have interface-compatibility notes that should be checked before launching them. See the [reproduction guide](../docs/REPRODUCIBILITY.md) for details.
