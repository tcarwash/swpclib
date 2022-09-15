import requests

url = "https://services.swpc.noaa.gov/json/f107_cm_flux.json"
base_url = "https://services.swpc.noaa.gov/json/"


class Runner:
    def __init__(self):
        self.base_url = base_url

    def get(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("An Http Error occurred:" + repr(errh))
            raise
        except requests.exceptions.ConnectionError as errc:
            print("An Error Connecting to the API occurred:" + repr(errc))
            raise
        except requests.exceptions.Timeout as errt:
            print("A Timeout Error occurred:" + repr(errt))
            raise
        except requests.exceptions.RequestException as err:
            print("An Unknown Error occurred" + repr(err))
            raise

        return response.json()

    def get_sfi(self, start=0, end=1, step=1):
        # get solar flux index
        response = self.get(self.base_url + "f107_cm_flux.json")
        data_range = slice(start, end, step)
        sfi_data = [
            {
                "sfi": float(item["flux"]),
                "timestamp": item["time_tag"],
            }
            for item in response[data_range]
        ]

        return sfi_data

    def get_ki(self, start=0, end=1, step=1):
        # get boulder K index
        response = self.get(self.base_url + "boulder_k_index_1m.json")
        data_range = slice(start, end, step)
        ki_data = [
            {
                "k_index": float(item["k_index"]),
                "timestamp": item["time_tag"],
            }
            for item in response[data_range]
        ]

        return ki_data

    def get_ssn(self, start=0, end=1, step=1):
        # get smoothed sunspot number
        response = self.get(
            self.base_url + "solar-cycle/sunspots-smoothed.json"
        )
        data_range = slice(start, end, step)
        ssn_data = [
            {
                "smoothed_ssn": float(item["smoothed_ssn"]),
                "timestamp": item["time-tag"],
            }
            for item in response[data_range]
        ]
        if ssn_data[0]["smoothed_ssn"] == -1:
            last = -1
            for item in response:
                last = item["smoothed_ssn"]
                last_timestamp = item["time-tag"]
                if last != -1:
                    break
            ssn_data[0]["last_ssn"] = {
                "smoothed_ssn": last,
                "timestamp": last_timestamp,
            }

        return ssn_data

    def get_kp(self, start=0, end=1, step=1):
        # get planetary k index
        response = self.get(self.base_url + "planetary_k_index_1m.json")
        data_range = slice(start, end, step)
        kp_data = [
            {
                "kp_index": float(item["kp_index"]),
                "timestamp": item["time_tag"],
            }
            for item in response[data_range]
        ]

        return kp_data

    def get_probabilities(self, start=0, end=1, step=1):
        # get solar event probabilities
        response = self.get(self.base_url + "solar_probabilities.json")
        data_range = slice(start, end, step)
        probabilities_data = [item for item in response[data_range]]

        return probabilities_data

    def get_standard(self):
        out = {
            "sfi": self.get_sfi()[0]["sfi"],
            "ki": self.get_ki()[0]["k_index"],
            "kp": self.get_kp()[0]["kp_index"],
        }

        ssn = self.get_ssn()
        if ssn[0]["last_ssn"]:
            out["ssn"] = ssn[0]["last_ssn"]["smoothed_ssn"]
        else:
            out["ssn"] = ssn[0]["smoothed_ssn"]

        return out


if __name__ == "__main__":
    swpc = Runner()
    print(swpc.get_standard())
