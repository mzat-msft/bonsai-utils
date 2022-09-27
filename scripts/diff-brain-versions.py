#!/usr/bin/env python
"""Compare two brain inkling versions."""

import argparse
import difflib
import sys

from bonsai_cli.exceptions import BrainServerError
from bonsai_cli.utils import api


def get_inkling(brain_name, brain_version, verbose):
    try:
        response = api(use_aad=True).get_brain_version(
            brain_name, brain_version, debug=verbose
        )
    except BrainServerError as exc:
        if exc.exception["statusCode"] == 404:
            print(f"Brain {brain_name} version {brain_version} not found.")
            exit()
    return response['inkling'].splitlines(keepends=True)


def main(brainA: str, versionA: int, brainB: str, versionB: int, verbose: bool):
    inklingA = get_inkling(brainA, versionA, verbose)
    inklingB = get_inkling(brainB, versionB, verbose)
    delta = difflib.unified_diff(inklingA, inklingB)
    sys.stdout.writelines(delta)


if __name__ == "__main__":

    epilog_text = """Examples:
 diff-brain-versions mybrain 2 3
    Compare versions 2 and 3 of the brain mybrain.
 diff-brain-versions mybrain 2 otherbrain 3
    Compare version 2 of mybrain to version 3 of otherbrain.
"""

    parser = argparse.ArgumentParser(
        description="Compare the inkling of two brain versions.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=epilog_text,
    )

    parser.add_argument(
        "brainA", type=str, help="The brain name containing the first version."
    )
    parser.add_argument("versionA", type=int, help="The first version number.")
    parser.add_argument(
        "brainB",
        nargs="?",
        type=str,
        help="Optional: brain name with versionB. If not specified, use brainA.",
    )
    parser.add_argument("versionB", type=int, help="The second version number.")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    main(
        args.brainA,
        args.versionA,
        args.brainB if args.brainB else args.brainA,
        args.versionB,
        args.verbose,
    )
