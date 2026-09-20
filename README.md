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

## Training code and tutorials

Training uses **mlcolvar**. The implementations and tutorials are maintained separately:

| Workflow | Implementation | Tutorial |
| --- | --- | --- |
| SelfTICA (`release/2.0`) | [Source code](https://github.com/luigibonati/mlcolvar/blob/release/2.0/mlcolvar/cvs/timelagged/selftica.py) | [Müller–Brown example](https://github.com/luigibonati/mlcolvar/blob/release/2.0/docs/notebooks/tutorials/cvs_SelfTICA.ipynb) |
| Transfer learning (`featurizer`) | [Source code](https://github.com/Kai-Zhu-2001/mlcolvar/tree/featurizer/mlcolvar/featurization/transfer) | [Pretrained representations for downstream tasks](https://github.com/Kai-Zhu-2001/mlcolvar/blob/featurizer/docs/notebooks/tutorials/adv_transfer.ipynb) |

## Data, citation, and license

This GitHub repository intentionally tracks the simulation inputs, trained models, and interfaces needed to reproduce the workflows, while large runtime outputs such as `COLVAR` trajectories are kept in the associated [Hugging Face dataset](https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA). For strict reproduction, use the frozen training-code version identified by the paper and dataset archive.

Please cite the companion paper when using these materials. [CITATION.cff](CITATION.cff) contains the preferred citation. The repository is distributed under the [MIT license](LICENSE); bundled third-party files retain their own license notices.
