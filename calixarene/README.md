# OAMe-G2 host-guest system

Inputs, models, and simulations for the OAMe-G2 host-guest binding benchmark.

## Contents

| Path | Description |
| --- | --- |
| `common/` | Canonical shared simulation inputs |
| `data/` | Bound and unbound structures and simulation data |
| `models/SelfTICA/` | SelfTICA GNN models |
| `models/DeepTDA/` | DeepTDA reference models |
| `run_unbiased/` | Unbiased simulations |
| `run_biased_gnn/` | Enhanced-sampling simulations using GNN collective variables |

The GNN simulations use custom PLUMED interfaces provided in [`../plumed/`](../plumed/).

For software requirements and known reproduction limitations, see the [reproduction guide](../docs/REPRODUCIBILITY.md).
