"""Console script for swpclib."""
import argparse
import sys
from . import swpclib


def main():
    """Console script for swpclib."""
    parser = argparse.ArgumentParser()
    parser.add_argument("_", nargs="*")
    args = parser.parse_args()

    runner = swpclib.Runner()
    print(runner.get_standard())

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
