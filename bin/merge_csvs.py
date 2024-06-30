#!/usr/bin/env python

import argparse
import sys
import pandas as pd
from datetime import datetime
from pathlib import Path


def command_line_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("workDir", type=Path, help="The directory that contains the csv files that should be merged.")

    return parser


def main():
    parser = command_line_parser()
    args = parser.parse_args()

    allCSVs = list(args.workDir.glob('./*.csv'))
    combined_csv = pd.concat((pd.read_csv(f) for f in allCSVs))

    combined_csv.to_csv("merged_csv.csv", index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    try:
        startTime = datetime.now()
        main()
        print(datetime.now() - startTime)
        sys.exit(0)
    except Exception as ex:
        print(f"Unexpected Error: {ex}")
        sys.exit(1)
