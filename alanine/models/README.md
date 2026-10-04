# Alanine models

Exported models used in the alanine benchmarks.

| Path | Description |
| --- | --- |
| `model_300K.pt`, `model_450K.pt`, `model_500K.pt`, `model_600K.pt` | Temperature-labelled model exports used in the alanine analyses |
| `across_lagtime/` | Model exports used for the lag-time transfer/comparison study |
| Hugging Face: `alanine/models/replicates/` | 120 repeated SelfTICA and DeepTICA FNN/GNN checkpoints used for benchmark statistics |

The replicate checkpoints are archived in the [SelfTICA Hugging Face dataset](https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA/tree/main/alanine/models/replicates) rather than tracked in Git. To restore them at the paths expected by `alanine/experiments.csv`, run from the repository root:

```bash
hf download Kai-Zhu-2001/SelfTICA --repo-type dataset --include "alanine/models/replicates/**" --local-dir .
```

The downloaded `alanine/models/replicates/` directory is ignored by Git. Use the exact model referenced by the corresponding PLUMED input or analysis workflow.

See the parent [alanine README](../README.md) and the [reproduction guide](../../docs/REPRODUCIBILITY.md).
