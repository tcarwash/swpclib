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

''' 
A dictionary of URL groups, keys of this dict are assumed to be names of valid groups to generate animations from
values should be a list of tuples where the 0th element is the url of the swpc endpoint, and the 1st element is a 
filename excluding the file extension, which will always be .gif
'''
urls = {
    'solar_images': [
        ('/products/animations/suvi-primary-094.json', 'goes_094'),
        ('/products/animations/suvi-primary-195.json', 'goes_195'),
        ('/products/animations/suvi-primary-304.json', 'goes_304'),
        ('/products/animations/suvi-primary-map.json', 'suvi-map'),
    ],
    'graphs': [
        ('/products/animations/d-rap_f15_global.json', 'd-rap_f15'),
        ('/products/animations/wam-ipe/wfs_ionosphere_new.json', 'global_ionosphere')
    ],
    'cme': [
        ('/products/animations/lasco-c2.json', 'lasco-c2'),
        ('/products/animations/lasco-c3.json', 'lasco-c3'),
    ],

    'aurora': [
        ('/products/animations/ovation_north_24h.json', 'ovation_north'),
        ('/products/animations/ovation_south_24h.json', 'ovation_south'),
    ],
    'geomagnetic': [
        ('/products/animations/geoelectric/US-Canada-1D.json', 'geomagnetic_north_america'),
    ],
}

async def get_animations(urls):
    swpc = swpclib.Runner()
    await asyncio.gather(*[swpc.gen_gif(endpoint=url[0], name=url[1], write=True) for url in urls], return_exceptions=False)

def animations():
    if len(sys.argv) > 1 and sys.argv[1] in urls.keys():
        group = sys.argv[1]
        url_group = urls.get(group, [])
        print(f"Generating {len(url_group)} animations for group: {group}")
        asyncio.run(get_animations(url_group))
    else:
        if group:
            print(f"{group} is not a valid group. valid groups are: {[group for group in urls.keys()]}")
        else:
            print(f"Must provide a valid group. valid groups are: {[group for group in urls.keys()]}")


def space_weather():
    """Console script for swpclib."""
    parser = argparse.ArgumentParser()
    parser.add_argument("_", nargs="*")
    args = parser.parse_args()

    runner = swpclib.Runner()
    data = asyncio.run(runner.get_standard())
    string = f"""\n{bcolors.OKBLUE}Current Space Weather:{bcolors.ENDC}

\tSFI: {data.get('sfi_data', {}).get('sfi')}
\tKP Index: {data.get('kp_index_data', {}).get('kp_index')}
\tA Index: {data['a_index_data']['a_index']}
\tSunspot Number: {data.get("ssn_data",{}).get("ssn")}
\tX-Class Probability: {data.get('probabilities_data',{})[0].get('x_class_1_day')}
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
    sys.exit(space_weather())  # pragma: no cover
