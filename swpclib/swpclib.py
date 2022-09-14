import requests

url = "https://services.swpc.noaa.gov/json/f107_cm_flux.json"
base_url = "https://services.swpc.noaa.gov/json/"


class Runner:
    def __init__(self):
        self.base_url = base_url

    def get_sfi(self, start=0, end=1, step=1):
        response = requests.get(base_url + "f107_cm_flux.json").json()
        data_range = slice(start, end, step)
        sfi_data = [
            {
                "sfi": int(item["flux"]),
                "timestamp": item["time_tag"],
            }
            for item in response[data_range]
        ]

        return sfi_data


if __name__ == "__main__":
    swpc = Runner()
    print(swpc.get_sfi())
