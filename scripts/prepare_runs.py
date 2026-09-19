#!/usr/bin/env python3
"""Restore shared inputs and render alanine experiments in their original paths."""

import argparse
import csv
import json
import os
from pathlib import Path, PurePosixPath
import re


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = "@MODEL_PATH@"
FIELDS = ["run_dir", "architecture", "method", "dataset", "replica", "model"]


def repo_path(root, name):
    """Accept only repository-relative paths, including after symlink resolution."""
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise ValueError(f"Invalid repository-relative path: {name!r}")
    relative = PurePosixPath(name)
    path = root.joinpath(*relative.parts)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ValueError(f"Path must stay inside the repository: {name}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path resolves outside the repository: {name}")
    return path


def verify_template_references(root, run_dir, rendered):
    """Check input references while leaving PRINT output names to the simulation."""
    for line in rendered.splitlines():
        line = line.split("#", 1)[0].strip()
        if line.startswith("PRINT"):
            continue
        for reference in re.findall(r"\b(?:FILE|MODEL|STRUCTURE|REFERENCE)=([^\s]+)", line):
            path = (run_dir / reference).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                raise ValueError(f"Missing or out-of-repository template input: {reference}")


def build_inputs(root):
    """Validate the source catalog and return destination paths and file contents."""
    inputs = {}
    sources = set()

    def add(name, content):
        path = repo_path(root, name)
        if path in inputs:
            raise ValueError(f"Duplicate generated destination: {name}")
        inputs[path] = content

    manifest = json.loads((root / "scripts/shared-inputs.json").read_text(encoding="utf-8"))
    if manifest.get("version") != 1 or not isinstance(manifest.get("files"), list):
        raise ValueError("Expected shared-inputs.json version 1 with a files list")
    for entry in manifest["files"]:
        source = repo_path(root, entry["source"])
        sources.add(source.resolve())
        content = source.read_bytes()
        if not isinstance(entry["targets"], list) or not entry["targets"]:
            raise ValueError(f"No target list for {entry['source']}")
        for target in entry["targets"]:
            add(target, content)

    templates = {}
    for architecture in ("FNN", "GNN"):
        source = repo_path(root, f"alanine/templates/{architecture.lower()}.dat.in")
        sources.add(source.resolve())
        template = source.read_text(encoding="utf-8")
        if template.count(PLACEHOLDER) != 1:
            raise ValueError(f"{source.name} must contain exactly one {PLACEHOLDER}")
        templates[architecture] = template
    tpr_path = repo_path(root, "alanine/common/ala2.tpr")
    sources.add(tpr_path.resolve())
    tpr = tpr_path.read_bytes()
    with (root / "alanine/experiments.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"experiments.csv columns must be {','.join(FIELDS)}")
        count = 0
        for row in reader:
            count += 1
            if set(row) != set(FIELDS) or any(not row[field] for field in FIELDS):
                raise ValueError(f"Incomplete experiment at CSV line {reader.line_num}")
            architecture = row["architecture"]
            if architecture not in templates or not row["replica"].isdigit():
                raise ValueError(f"Invalid architecture or replica at CSV line {reader.line_num}")
            expected_model = (f"alanine/models/std/{row['method']}/{architecture}/"
                              f"{row['dataset']}/model_{row['replica']}.pt")
            if row["model"] != expected_model:
                raise ValueError(f"Model does not match experiment identity: {row['model']}")
            model = repo_path(root, row["model"])
            if not model.is_file():
                raise ValueError(f"Missing model: {row['model']}")
            sources.add(model.resolve())
            run_dir = repo_path(root, row["run_dir"])
            relative_model = Path(os.path.relpath(model, run_dir)).as_posix()
            rendered = templates[architecture].replace(PLACEHOLDER, relative_model)
            verify_template_references(root, run_dir, rendered)
            add(row["run_dir"] + "/plumed.dat", rendered.encode("utf-8"))
            add(row["run_dir"] + "/ala2.tpr", tpr)
        if not count:
            raise ValueError("experiments.csv contains no experiments")
    for path in inputs:
        if path.resolve() in sources:
            raise ValueError(f"Generated destination overlaps a source: {path.relative_to(root)}")
    return inputs


def prepare(inputs):
    """Preflight the whole selection; never replace an existing differing input."""
    missing = []
    for path, content in sorted(inputs.items()):
        if path.exists():
            if not path.is_file() or path.read_bytes() != content:
                raise ValueError(f"Existing input differs; move it aside before preparing: {path}")
        else:
            for parent in path.parents:
                if parent.exists() and not parent.is_dir():
                    raise ValueError(f"Input directory is blocked by a file: {parent}")
            missing.append((path, content))
    for path, content in missing:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also prevents overwriting a file created after preflight.
        with path.open("xb") as stream:
            stream.write(content)
    return len(missing)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--list", action="store_true", help="list run directories with generated inputs")
    action.add_argument("--check", action="store_true", help="validate sources and models without writing")
    action.add_argument("--run", metavar="DIRECTORY", help="prepare one repository-relative run directory")
    action.add_argument("--all", action="store_true", help="prepare every run in the catalog")
    args = parser.parse_args()
    try:
        inputs = build_inputs(ROOT)
        runs = sorted({path.parent.relative_to(ROOT).as_posix() for path in inputs})
        if args.list:
            print("\n".join(runs))
        elif args.check:
            print(f"Validated {len(inputs)} generated inputs in {len(runs)} run directories; no files written.")
        else:
            if args.run:
                run_dir = repo_path(ROOT, args.run.replace("\\", "/"))
                if run_dir.relative_to(ROOT).as_posix() not in runs:
                    raise ValueError(f"Unknown preparation target: {args.run}; use --list")
                inputs = {path: data for path, data in inputs.items() if path.parent == run_dir}
            created = prepare(inputs)
            print(f"Prepared {len(inputs)} inputs: {created} created, {len(inputs) - created} already present.")
    except (OSError, ValueError, KeyError, TypeError, csv.Error) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
