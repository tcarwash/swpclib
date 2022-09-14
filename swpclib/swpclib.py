import requests

url = "https://services.swpc.noaa.gov/json/f107_cm_flux.json"
base_url = "https://services.swpc.noaa.gov/json/"


class Runner:
    def __init__(self):
        self.base_url = base_url

    def get_sfi(self):
        response = requests.get(base_url + "f107_cm_flux.json").json()
        data = {
            "sfi": int(response[0]["flux"]),
            "timestamp": response[0]["time_tag"],
        }

        return data


if __name__ == "__main__":
    swpc = Runner()
    print(swpc.get_sfi())
