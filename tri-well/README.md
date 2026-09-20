# Tri-well potential

Inputs, models, and simulations for the two-dimensional tri-well benchmark.

## Contents

| Path | Description |
| --- | --- |
| `common/` | Canonical shared simulation inputs |
| `models/unbiased/` | Models trained from unbiased data |
| `models/biased/` | Models trained from biased data |
| `models/std/` | Additional reference models |
| `run_unbiased/` | Unbiased simulation inputs |
| `run_biased/` | Enhanced-sampling inputs using learned collective variables |

The tri-well system provides a low-dimensional benchmark for comparing SelfTICA with reference slow-mode learning approaches and for testing learned collective variables in enhanced sampling.

Large `COLVAR` outputs are archived in the repository's [dataset](https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA) rather than tracked here.

For preparation and launch commands, see the [reproduction guide](../docs/REPRODUCIBILITY.md).
