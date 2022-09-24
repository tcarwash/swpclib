"""Console script for swpclib."""
import argparse
import sys
from . import swpclib
import asyncio


def main():
    """Console script for swpclib."""
    parser = argparse.ArgumentParser()
    parser.add_argument("_", nargs="*")
    args = parser.parse_args()

    runner = swpclib.Runner()
    data = asyncio.run(runner.get_standard())
    adjusted_ssn = (
        data["smoothed_ssn_data"]["last_ssn"]["smoothed_ssn"]
        or data["smoothed_ssn_data"]["smoothed_ssn"]
    )
    string = f"""\nCurrent Space Weather:

    SFI: {data['sfi_data']['sfi']}
    KP Index: {data['kp_index_data']['kp_index']}
    A Index: {data['a_index_data']['a_index']}
    Sunspot Number: {adjusted_ssn}
    X-Class Probability: {data['probabilities_data'][0]['x_class_1_day']}\n\nVia NOAA Space Weather Prediction Center
    """
    print(string)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
