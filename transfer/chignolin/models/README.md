# Chignolin transfer models

Models used to transfer the pretrained chignolin SelfTICA representation to committor learning.

| File pattern | Description |
| --- | --- |
| `chignolin_selftica_model_state.pt` | Pretrained SelfTICA model state |
| `transfer_0_z.pt`, `transfer_1_z.pt` | Exported latent-coordinate models for refinement iterations 0 and 1 |
| `transfer_0_q.pt`, `transfer_1_q.pt` | Corresponding committor-output models |

The `z` and `q` exports serve different roles and should not be interchanged. Use the exact iteration referenced by the corresponding simulation input.

See the [transfer overview](../../README.md) and the [reproduction guide](../../../docs/REPRODUCIBILITY.md).
