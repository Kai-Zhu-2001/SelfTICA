# Transfer to committor learning

Models and simulation inputs used to transfer pretrained SelfTICA representations to committor learning.

The transfer benchmarks cover the tri-well potential, alanine dipeptide, and chignolin.

## Contents

| Path | Description |
| --- | --- |
| `tri-well/` | Tri-well pretrained representation, transferred models, and sampling inputs |
| `alanine/` | Alanine pretrained representation, transferred models, and sampling inputs |
| `chignolin/` | Chignolin pretrained representation, transferred models, and sampling inputs |

Each system contains a pretrained SelfTICA checkpoint and task-specific committor models.

Model-name conventions are:

- `*model_state.pt`: pretrained SelfTICA model state used to initialize the transferred representation;
- `*_z.pt`: exported latent-coordinate model used by the Kolmogorov-bias interface;
- `*_q.pt`: corresponding model exposing the transformed committor output.

Alanine and chignolin include multiple refinement iterations where applicable. These model files are not interchangeable: simulation inputs should use the exact model type and iteration referenced by the corresponding PLUMED input.

Large `COLVAR` outputs from the transfer simulations are archived in the repository's [dataset](https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA) rather than tracked here.

For the transfer-learning workflow and simulation requirements, see the [reproduction guide](../docs/REPRODUCIBILITY.md).
