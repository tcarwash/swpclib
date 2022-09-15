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
                "sfi": float(item["flux"]),
                "timestamp": item["time_tag"],
            }
            for item in response[data_range]
        ]

        return sfi_data

    def get_ki(self, start=0, end=1, step=1):
        response = requests.get(base_url + "boulder_k_index_1m.json").json()
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
        response = requests.get(
            base_url + "solar-cycle/sunspots-smoothed.json"
        ).json()
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
        response = requests.get(base_url + "planetary_k_index_1m.json").json()
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
        response = requests.get(base_url + "solar_probabilities.json").json()
        data_range = slice(start, end, step)
        probabilities_data = [item for item in response[data_range]]

        return probabilities_data


if __name__ == "__main__":
    swpc = Runner()
    #    print(swpc.get_sfi())
    #    print(swpc.get_ki())
    #    print(swpc.get_kp())
    print(swpc.get_probabilities())
    print(swpc.get_ssn())
