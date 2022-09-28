"""Console script for swpclib."""
import argparse
import sys
from . import swpclib
import asyncio


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


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
    string = f"""\n{bcolors.OKBLUE}Current Space Weather:{bcolors.ENDC}

\tSFI: {data['sfi_data']['sfi']}
\tKP Index: {data['kp_index_data']['kp_index']}
\tA Index: {data['a_index_data']['a_index']}
\tSunspot Number: {adjusted_ssn}
\tX-Class Probability: {data['probabilities_data'][0]['x_class_1_day']}
    """
    print(string)
    alerts = [alert for alert in data["alerts"]]
    if "active" in data:
        alert_string = f"{bcolors.OKBLUE}Recent Alerts{bcolors.WARNING} (ACTIVE){bcolors.OKBLUE}:{bcolors.ENDC}\n\n"
    else:
        alert_string = f"{bcolors.OKBLUE}Recent Alerts:{bcolors.ENDC}\n\n"
    for alert in alerts:
        if "active" in alert:
            alert_string += (
                f"{bcolors.WARNING}{alert['formatted_message']}{bcolors.ENDC}"
            )
        else:
            alert_string += alert["formatted_message"]
        alert_string += "\n\n\n"
    alert_string += "Via NOAA Space Weather Prediction Center"
    print(alert_string)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
