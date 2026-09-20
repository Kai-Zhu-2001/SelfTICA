# Tri-well transfer models

Models used to transfer the pretrained tri-well SelfTICA representation to committor learning.

| File | Description |
| --- | --- |
| `selftica_model_state.pt` | Pretrained SelfTICA model state |
| `transfer_z.pt` | Exported latent-coordinate model used by the Kolmogorov-bias workflow |
| `transfer_q.pt` | Corresponding committor-output model |

The checkpoint, `z` export, and `q` export are not interchangeable.

See the [transfer overview](../../README.md) and the [reproduction guide](../../../docs/REPRODUCIBILITY.md).
