"""Command line entry point: `vlmfw <command>`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from vlmfw.config import load_config
from vlmfw.splits import make_split_table


def _cmd_splits(args: argparse.Namespace) -> int:
    cfg = load_config(args.config)
    table = make_split_table(cfg["paths"]["raw_images"], cfg["splits"], cfg["seed"])
    out = Path("data/interim/splits.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out, index=False)
    print(f"{len(table)} photos -> {out}")
    print(table["split"].value_counts().to_string())
    return 0


def _todo(week: int, name: str):
    def run(_: argparse.Namespace) -> int:
        print(f"'{name}' is not implemented yet (planned for Week {week}).", file=sys.stderr)
        return 2

    return run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vlmfw", description=__doc__)
    parser.add_argument("--config", default="configs/default.yaml")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("splits", help="assign each clean photo to train/val/test").set_defaults(
        func=_cmd_splits
    )
    for week, name, text in [
        (1, "sentences", "download and filter attack sentences"),
        (2, "generate", "build the attacked dataset"),
        (3, "baseline", "measure VLM attack success rate"),
        (4, "train-detector", "train the YOLO detector"),
        (5, "train-classifier", "train the trick classifier"),
        (7, "clean", "run the full firewall on an image"),
    ]:
        sub.add_parser(name, help=f"[Week {week}] {text}").set_defaults(func=_todo(week, name))

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
