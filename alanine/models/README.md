# Alanine models

Exported models used in the alanine benchmarks.

| Path | Description |
| --- | --- |
| `model_300K.pt`, `model_450K.pt`, `model_500K.pt`, `model_600K.pt` | Temperature-labelled SelfTICA model exports used in the alanine analyses |
| `across_lagtime/` | Model exports used for the lag-time transfer/comparison study |
| `std/SelfTICA/` | SelfTICA model collection used for repeated/reference comparisons |
| `std/DeepTICA/` | DeepTICA reference model collection |

Use the exact model referenced by the corresponding PLUMED input or analysis workflow. The model files are archived outputs rather than interchangeable checkpoints.

See the parent [alanine README](../README.md) and the [reproduction guide](../../docs/REPRODUCIBILITY.md).
