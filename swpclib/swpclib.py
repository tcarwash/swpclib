import asyncio
import aiohttp

url = "https://services.swpc.noaa.gov/json/f107_cm_flux.json"
base_url = "https://services.swpc.noaa.gov/json/"


class Runner:
    def __init__(self):
        self.base_url = base_url

    async def get_sfi(self, start=0, end=1, step=1):
        # get solar flux index
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url + "f107_cm_flux.json"
            ) as response:
                data = await response.json()
                data_range = slice(start, end, step)
                sfi_data = {
                    "sfi_data": {
                        "sfi": float(item["flux"]),
                        "timestamp": item["time_tag"],
                    }
                    for item in data[data_range]
                }

        return sfi_data

    async def get_ki(self, start=0, end=1, step=1):
        # get boulder K index
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url + "boulder_k_index_1m.json"
            ) as response:
                data = await response.json()
                data_range = slice(start, end, step)
                ki_data = {
                    "k_index_data": {
                        "k_index": float(item["k_index"]),
                        "timestamp": item["time_tag"],
                    }
                    for item in data[data_range]
                }

        return ki_data

    async def get_ssn(self, start=0, end=1, step=1):
        # get smoothed sunspot number
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url + "solar-cycle/sunspots-smoothed.json"
            ) as response:
                data = await response.json()
                data_range = slice(start, end, step)
                ssn_data = {
                    "smoothed_ssn_data": {
                        "smoothed_ssn": float(item["smoothed_ssn"]),
                        "timestamp": item["time-tag"],
                    }
                    for item in data[data_range]
                }
                if ssn_data["smoothed_ssn_data"]["smoothed_ssn"] == -1:
                    last = -1
                    for item in data:
                        last = item["smoothed_ssn"]
                        last_timestamp = item["time-tag"]
                        if last != -1:
                            break
                    ssn_data["smoothed_ssn_data"]["last_ssn"] = {
                        "smoothed_ssn": last,
                        "timestamp": last_timestamp,
                    }

        return ssn_data

    async def get_kp(self, start=0, end=1, step=1):
        # get planetary k index
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url + "planetary_k_index_1m.json"
            ) as response:
                data = await response.json()
                data_range = slice(start, end, step)
                kp_data = {
                    "kp_index_data": {
                        "kp_index": float(item["kp_index"]),
                        "timestamp": item["time_tag"],
                    }
                    for item in data[data_range]
                }

        return kp_data

    async def get_probabilities(self, start=0, end=1, step=1):
        # get solar event probabilities
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url + "solar_probabilities.json"
            ) as response:
                data = await response.json()
                data_range = slice(start, end, step)
                probabilities_data = {
                    "probabilities_data": [item for item in data[data_range]]
                }

        return probabilities_data

    async def get_standard(self, start=0, end=1, step=1):
        standard_group = await asyncio.gather(
            self.get_sfi(),
            self.get_kp(),
            self.get_probabilities(),
            self.get_ssn(),
        )
        data = {}
        for _dict in standard_group:
            data.update(_dict)

        return data


if __name__ == "__main__":
    swpc = Runner()
    print(asyncio.run(swpc.get_standard()))
