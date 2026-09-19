# SelfTICA

Simulation inputs, trained models, and PLUMED interfaces for learning dynamical representations and sampling molecular rare events with SelfTICA.

**Companion paper:** [SelfTICA: contrastive learning of dynamical representations for rare-event sampling and characterization](https://arxiv.org/abs/2606.15495)

Kai Zhu, Jintu Zhang, Pietro Novelli, Tingjun Hou, and Luigi Bonati (2026).

[Paper](https://arxiv.org/abs/2606.15495) · [Dataset](https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA) · [Reproduction guide](docs/REPRODUCIBILITY.md) · [Citation](CITATION.cff)

## Getting started

1. **Learn the method:** follow the external training tutorials below.
2. **Explore a system:** use the directory table to find its inputs and models.
3. **Prepare simulation inputs:** from the repository root, use `python scripts/prepare_runs.py --list` to see generated-input targets and `python scripts/prepare_runs.py --run REPO_RELATIVE_RUN_DIRECTORY` to prepare one exact run directory.
4. **Run simulations:** follow the [reproduction guide](docs/REPRODUCIBILITY.md) for dependencies, launch commands, and known input limitations.

```bash
git clone https://github.com/Kai-Zhu-2001/SelfTICA.git
cd SelfTICA
python scripts/prepare_runs.py --check
```

Preparation requires Python 3.9 or newer. Canonical shared inputs live in each system's `common/` directory; alanine's generated configurations are defined by `alanine/experiments.csv` and `alanine/templates/`. The preparation command restores generated inputs at their original run paths, where existing launch conventions and run-local outputs continue to work. See the reproduction guide before editing or refreshing a generated file.

## Repository contents

| Directory | System or purpose | Main contents |
| --- | --- | --- |
| [tri-well/](tri-well/) | Two-dimensional tri-well potential | Unbiased and biased simulations; SelfTICA and DeepTICA models |
| [alanine/](alanine/) | Alanine dipeptide in vacuum | Unbiased, multithermal, and neural-network-biased simulations |
| [chignolin/](chignolin/) | Chignolin folding in water | Structures, force field, models, and OPES-Explore inputs |
| [calixarene/](calixarene/) | OAMe–G2 host–guest binding in water | Bound/unbound inputs; SelfTICA and DeepTDA GNN models and simulations |
| [fen2/](fen2/) | N₂ dissociation on Fe(111) | LAMMPS inputs, MACE potential, and OPES-Explore simulations |
| [transfer/](transfer/) | Transfer to committor learning | Tri-well, alanine, and chignolin models and sampling inputs |
| [plumed/](plumed/) | Custom PLUMED actions | GNN and committor-bias C++ interfaces with [usage notes](plumed/README.md) |

Within each system, `data/` holds structural inputs, `models/` holds saved models, and `run_*/` holds simulation inputs where present. Shared PLUMED interfaces live in `plumed/`. CV denotes a collective variable; FNN and GNN denote feed-forward and graph neural networks.

## Training code and tutorials

Training uses **mlcolvar**. The implementations and notebooks are maintained in the external repositories below.

| Workflow | Implementation | Tutorial |
| --- | --- | --- |
| SelfTICA (`release/2.0`) | [Source code](https://github.com/luigibonati/mlcolvar/blob/release/2.0/mlcolvar/cvs/timelagged/selftica.py) | [Müller–Brown example](https://github.com/luigibonati/mlcolvar/blob/release/2.0/docs/notebooks/tutorials/cvs_SelfTICA.ipynb) |
| Transfer learning (`featurizer`) | [Source code](https://github.com/Kai-Zhu-2001/mlcolvar/tree/featurizer/mlcolvar/featurization/transfer) | [Pretrained representations for downstream tasks](https://github.com/Kai-Zhu-2001/mlcolvar/blob/featurizer/docs/notebooks/tutorials/adv_transfer.ipynb) |

## Data availability

The [Hugging Face dataset](https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA) provides the associated training and simulation data. The paper's [code availability statement](https://arxiv.org/html/2606.15495v3#S6) also identifies a frozen training-code version there for reproducing the reported results. Use that version for reproduction and the linked mlcolvar branches for current tutorials.

## Citation and license

Please cite the companion paper when using these materials. [CITATION.cff](CITATION.cff) contains the authors, preprint DOI, and preferred citation.

The repository includes an [MIT license](LICENSE). Bundled third-party files retain their own license notices.
