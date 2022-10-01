import asyncio
import aiohttp
from . import alerts

base_url = "https://services.swpc.noaa.gov/"


class Runner:
    def __init__(self):
        self.base_url = base_url

    async def get_data_method(self, url):
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=20.0)
            ) as session:
                async with session.get(self.base_url + url) as response:
                    result = await response.json()
        except Exception as e:
            raise e

        return result

    async def get_sfi(self, start=0, end=1, step=1):
        """get solar flux index"""

        try:
            data = await self.get_data_method("json/f107_cm_flux.json")
            data_range = slice(start, end, step)
            sfi_data = {
                "sfi_data": {
                    "sfi": float(item["flux"] or float("-1")),
                    "timestamp": item["time_tag"],
                }
                for item in data[data_range]
            }
        except Exception as e:
            print(repr(e))
            sfi_data = {"sfi_data": None}

        return sfi_data

    async def get_ki(self, start=0, end=1, step=1):
        """get boulder K index"""

        try:
            data = await self.get_data_method("json/boulder_k_index_1m.json")
            data_range = slice(start, end, step)
            ki_data = {
                "k_index_data": {
                    "k_index": float(item["k_index"]),
                    "timestamp": item["time_tag"],
                }
                for item in data[data_range]
            }
        except Exception as e:
            print(repr(e))
            ki_data = {"ki_data": None}

        return ki_data

    async def get_a(self, start=0, end=1, step=1):
        """get Fredricksburg A index"""

        try:
            data = await self.get_data_method(
                "json/predicted_fredericksburg_a_index.json"
            )
            data_range = slice(start, end, step)
            a_data = {
                "a_index_data": {
                    "a_index": float(item["afred_1_day"]),
                    "a_2_day_index": float(item["afred_2_day"]),
                    "a_3_day_index": float(item["afred_3_day"]),
                    "timestamp": item["date"],
                }
                for item in data[data_range]
            }
        except Exception as e:
            print(repr(e))
            a_data = {"a_data": None}

        return a_data

    async def get_ssn(self, start=0, end=1, step=1):
        """get observed sunspot number"""

        try:
            data = await self.get_data_method(
                "json/solar-cycle/swpc_observed_ssn.json"
            )
            data_range = slice(start, end, step)
            data.reverse()
            ssn_data = {
                "ssn_data": {
                    "ssn": float(item["swpc_ssn"]),
                    "timestamp": item["Obsdate"],
                }
                for item in data[data_range]
            }
        except Exception as e:
            print(repr(e))
            ssn_data = {"ssn_data": None}

        return ssn_data

    async def get_kp(self, start=0, end=1, step=1):
        """get planetary k index"""

        try:
            data = await self.get_data_method("json/planetary_k_index_1m.json")
            data_range = slice(start, end, step)
            kp_data = {
                "kp_index_data": {
                    "kp_index": float(item["kp_index"]),
                    "timestamp": item["time_tag"],
                }
                for item in data[data_range]
            }
        except Exception as e:
            print(repr(e))
            kp_data = {"kp_data": None}

        return kp_data

    async def get_probabilities(self, start=0, end=1, step=1):
        """get solar event probabilities"""

        try:
            data = await self.get_data_method("json/solar_probabilities.json")
            data_range = slice(start, end, step)
            probabilities_data = {
                "probabilities_data": [item for item in data[data_range]]
            }
        except Exception as e:
            print(repr(e))
            probabilities_data = {"probabilities_data": None}

        return probabilities_data

    async def get_alerts(self, start=0, end=3, step=1):
        """Returns solar weather alerts"""

        try:
            data = await self.get_data_method("products/alerts.json")
            data_range = slice(start, end, step)
            alerts_data = []
            active = False
            for alert in data[data_range]:
                try:
                    a = alerts.format_message(alert)
                    if "active" in a:
                        active = True
                    alerts_data.append(a)
                except Exception as e:
                    print(repr(e))
            alerts_data = {"alerts": alerts_data}
            if active:
                alerts_data["active"] = True
        except Exception as e:
            print(repr(e))
            alerts_data = {"alerts": None}

        return alerts_data

    async def get_standard(self, start=0, end=1, step=1):
        """return standard output"""

        try:
            standard_group = await asyncio.gather(
                self.get_sfi(),
                self.get_kp(),
                self.get_probabilities(),
                self.get_ssn(),
                self.get_a(),
                self.get_alerts(),
            )
            data = {}
            for _dict in standard_group:
                data.update(_dict)
        except Exception as e:
            print(repr(e))
            data = None
        return data


if __name__ == "__main__":
    swpc = Runner()
    print(asyncio.run(swpc.get_standard()))
