from datetime import datetime
import re

watch_sample = {
    "product_id": "A20F",
    "issue_datetime": "2022-09-27 19:57:05.470",
    "message": "Space Weather Message Code: WATA20\r\nSerial Number: 918\r\nIssue Time: 2022 Sep 27 1957 UTC\r\n\r\nWATCH: Geomagnetic Storm Category G1 Predicted\r\n\r\nHighest Storm Level Predicted by Day:\r\nSep 28:  None (Below G1)   Sep 29:  None (Below G1)   Sep 30:  G1 (Minor)\r\n\r\nTHIS SUPERSEDES ANY\\/ALL PRIOR WATCHES IN EFFECT\r\n\r\nNOAA Space Weather Scale descriptions can be found at\r\nwww.swpc.noaa.gov/noaa-scales-explanation\r\n\r\nPotential Impacts: Area of impact primarily poleward of 60 degrees Geomagnetic Latitude.\r\nInduced Currents - Weak power grid fluctuations can occur.\r\nSpacecraft - Minor impact on satellite operations possible.\r\nAurora - Aurora may be visible at high latitudes, i.e., northern tier of the U.S. such as northern Michigan and Maine.",
}

warn_sample = {
    "product_id": "K05W",
    "issue_datetime": "2022-09-27 09:34:10.330",
    "message": "Space Weather Message Code: WARK05\r\nSerial Number: 1682\r\nIssue Time: 2022 Sep 27 0934 UTC\r\n\r\nEXTENDED WARNING: Geomagnetic K-index of 5 expected\r\nExtension to Serial Number: 1681\r\nValid From: 2022 Sep 27 0122 UTC\r\nNow Valid Until: 2022 Sep 27 1800 UTC\r\nWarning Condition: Persistence\r\n\r\nNOAA Space Weather Scale descriptions can be found at\r\nwww.swpc.noaa.gov/noaa-scales-explanation\r\n\r\nPotential Impacts: Area of impact primarily poleward of 60 degrees Geomagnetic Latitude.\r\nInduced Currents - Weak power grid fluctuations can occur.\r\nSpacecraft - Minor impact on satellite operations possible.\r\nAurora - Aurora may be visible at high latitudes, i.e., northern tier of the U.S. such as northern Michigan and Maine.",
}

alert_sample = {
    "product_id": "K05A",
    "issue_datetime": "2022-09-27 01:32:19.593",
    "message": "Space Weather Message Code: ALTK05\r\nSerial Number: 1394\r\nIssue Time: 2022 Sep 27 0132 UTC\r\n\r\nALERT: Geomagnetic K-index of 5\r\nThreshold Reached: 2022 Sep 27 0131 UTC\r\nSynoptic Period: 0000-0300 UTC\r\n \r\nActive Warning: Yes\r\nNOAA Scale: G1 - Minor\r\n\r\nNOAA Space Weather Scale descriptions can be found at\r\nwww.swpc.noaa.gov/noaa-scales-explanation\r\n\r\nPotential Impacts: Area of impact primarily poleward of 60 degrees Geomagnetic Latitude.\r\nInduced Currents - Weak power grid fluctuations can occur.\r\nSpacecraft - Minor impact on satellite operations possible.\r\nAurora - Aurora may be visible at high latitudes, i.e., northern tier of the U.S. such as northern Michigan and Maine.",
}


def parse_message(output):

    _warning = re.compile(r".+W$")
    _alert = re.compile(r".+A$")
    _watch = re.compile(r".+F$")
    prid = output["product_id"]

    if _warning.match(prid):
        output["type"] = "warning"

    elif _watch.match(prid):
        output["type"] = "watch"

    elif _alert.match(prid):
        output["type"] = "alert"
    message = output["raw_message"]
    try:
        output["message_code"] = re.search(
            r"Space Weather Message Code: (.*)\r", message
        ).group(1)
    except AttributeError:
        pass
    try:
        output["serial_number"] = int(
            re.search(r"Serial Number: (.*)\r", message).group(1)
        )
    except AttributeError:
        pass
    try:
        _watch = re.compile(r"WATCH: (.*)\n.*\:", re.MULTILINE | re.DOTALL)
        output["watch"] = _watch.search(message).group(1)
    except AttributeError:
        pass
    try:
        _impacts = re.compile(
            r"Potential Impacts: (.*).*$", re.DOTALL | re.MULTILINE
        )
        output["impacts"] = _impacts.search(message).group(1)
    except AttributeError:
        pass
    try:
        _desc = re.compile(r"Description: (.*).*$", re.DOTALL | re.MULTILINE)
        output["description"] = _desc.search(message).group(1)
    except AttributeError:
        pass
    try:
        output["synoptic_period"] = re.search(
            r"\n.*Synoptic Period: (.*)\r", message
        ).group(1)
    except AttributeError:
        pass
    try:
        output["estimated_velocity"] = re.search(
            r"\n.*Estimated Velocity: (.*km)", message
        ).group(1)
    except AttributeError:
        pass
    try:
        output["threshold_reached"] = datetime.strptime(
            re.search(r"\nThreshold Reached: (.*)\r", message).group(1),
            "%Y %b %d %H%M %Z",
        )
    except AttributeError:
        pass
    try:
        _alert = re.compile(r"ALERT: (.*)\r")
        output["alert"] = _alert.search(message).group(1)
    except AttributeError:
        pass
    try:
        output["valid_from"] = datetime.strptime(
            re.search(r"Valid From: (.*)\r", message).group(1),
            "%Y %b %d %H%M %Z",
        )
        output["valid_until"] = datetime.strptime(
            re.search(r"\n.*Valid Until: (.*)\r", message).group(1),
            "%Y %b %d %H%M %Z",
        )
    except AttributeError:
        pass
    try:
        _watch = re.compile(r"\n.*WARNING: (.*)\r")
        output["warning"] = _watch.search(message).group(1)
    except AttributeError:
        pass
    try:
        if "valid_until" in output:
            if datetime.now() <= output["valid_until"]:
                output["active"] = True
    except AttributeError:
        pass
    alert_string = ""
    alert_string += f"{output['serial_number']} -- {output['message_code']} -- {output['issue_datetime']} -------\n\n"
    if "alert" in output:
        alert_string += output["alert"] + "\n"
    elif "warning" in output:
        alert_string += output["warning"] + "\n"
    elif "watch" in output:
        alert_string += output["watch"] + "\n"
    if "valid_from" in output:
        alert_string += (
            f"From: {output['valid_from']} --> {output.get('valid_until')}\n"
        )
    if "synoptic_period" in output:
        alert_string += f"Synoptic Period: {output['synoptic_period']}\n"
    if "threshold_reached" in output:
        alert_string += f"Threshold Reached: {output['threshold_reached']}\n"
    if "estimated_velocity" in output:
        alert_string += f"Estimated Velocity: {output['estimated_velocity']}\n"
    if "description" in output:
        alert_string += output["description"] + "\n"
    if "impacts" in output:
        alert_string += output["impacts"] + "\n"
    alert_string += "----------------------------------------------------"
    output["formatted_message"] = alert_string

    return output


def format_message(alert):
    """Return a formatted alert message"""

    output = {}
    output["product_id"] = alert["product_id"]
    output["issue_datetime"] = datetime.strptime(
        alert["issue_datetime"], "%Y-%m-%d %H:%M:%S.%f"
    )
    output["raw_message"] = alert["message"]
    output = parse_message(output)

    return output


if __name__ == "__main__":
    print(format_message(watch_sample))
    print("\n\n\n")
    print(format_message(warn_sample))
    print("\n\n\n")
    print(format_message(alert_sample))
