# SelfTICA

Simulation inputs, trained models, and PLUMED interfaces for learning dynamical representations and sampling molecular rare events with SelfTICA.

**Companion paper:** [SelfTICA: contrastive learning of dynamical representations for rare-event sampling and characterization](https://arxiv.org/abs/2606.15495)

Kai Zhu, Jintu Zhang, Pietro Novelli, Tingjun Hou, and Luigi Bonati (2026).

[Paper](https://arxiv.org/abs/2606.15495) · [Dataset](https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA) · [Reproduction guide](docs/REPRODUCIBILITY.md) · [Citation](CITATION.cff)

## Quick start

```bash
git clone https://github.com/Kai-Zhu-2001/SelfTICA.git
cd SelfTICA
python scripts/prepare_runs.py --check
```

Input preparation requires Python 3.9 or newer.

Some repeated inputs are generated from canonical shared files before launch. Use

```bash
python scripts/prepare_runs.py --list
python scripts/prepare_runs.py --run REPO_RELATIVE_RUN_DIRECTORY
```

from the repository root when required. Keep simulations in their original directory layout so that relative paths to models, structures, and PLUMED sources remain valid. See the [reproduction guide](docs/REPRODUCIBILITY.md) for software requirements, launch examples, and known input limitations.

## Repository contents

| Directory | System or purpose |
| --- | --- |
| [tri-well/](tri-well/) | Two-dimensional tri-well potential; unbiased and biased sampling |
| [alanine/](alanine/) | Alanine dipeptide; unbiased, multithermal, and learned-CV simulations |
| [chignolin/](chignolin/) | Chignolin folding; learned slow modes and OPES-Explore sampling |
| [calixarene/](calixarene/) | OAMe–G2 host–guest binding with GNN collective variables |
| [fen2/](fen2/) | N₂ dissociation on Fe(111) with LAMMPS, MACE, and OPES-Explore |
| [transfer/](transfer/) | Transfer of pretrained SelfTICA representations to committor learning |
| [plumed/](plumed/) | Custom GNN and committor-bias PLUMED interfaces |
| [docs/](docs/) | Reproduction notes and software/input conventions |

Each system directory contains its own README describing the local data, models, and run directories.

## Method implementations and tutorials

The core SelfTICA and reusable-representation implementations live in **mlcolvar**, while this repository contains the trained models, simulation inputs, and reproduction workflows.

| Component | Source code | Tutorial / development |
| --- | --- | --- |
| SelfTICA | [`mlcolvar/cvs/timelagged/selftica.py`](https://github.com/luigibonati/mlcolvar/blob/release/2.0/mlcolvar/cvs/timelagged/selftica.py) | [SelfTICA tutorial](https://github.com/luigibonati/mlcolvar/blob/release/2.0/docs/notebooks/tutorials/cvs_SelfTICA.ipynb) |
| Reusable representation framework | [`mlcolvar/representation/`](https://github.com/Kai-Zhu-2001/mlcolvar/tree/featurizer/mlcolvar/representation) | [PR #283](https://github.com/luigibonati/mlcolvar/pull/283) |
| MLColvarRepresentation | [`representation/mlcolvar.py`](https://github.com/Kai-Zhu-2001/mlcolvar/blob/featurizer/mlcolvar/representation/mlcolvar.py) | [Transfer-learning tutorial](https://github.com/Kai-Zhu-2001/mlcolvar/blob/featurizer/docs/notebooks/tutorials/adv_transfer_mlcolvar.ipynb) |

The representation framework is currently developed in the `featurizer` branch through PR #283 and targets `mlcolvar` `release/2.0`. Links can be updated to the release branch after that PR is merged.

## Data, citation, and license

This GitHub repository intentionally tracks the simulation inputs, essential trained models, and interfaces needed to reproduce the workflows. Large runtime outputs such as `COLVAR` trajectories and the 120 alanine replicate benchmark checkpoints are kept in the associated [Hugging Face dataset](https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA). For strict reproduction, use the frozen training-code version identified by the paper and dataset archive.

Please cite the companion paper when using these materials. [CITATION.cff](CITATION.cff) contains the preferred citation. The repository is distributed under the [MIT license](LICENSE); bundled third-party files retain their own license notices.
