EN = {
    "trainStatus": {
        "ON_TIME": "On time",
        "CANCELLED": "Cancelled",
        "DELAYED": "Delayed",
        "DEPARTED": "Departed",
        "DELAYED_DEPARTED": "Departed (Delayed)",
    },
    "trainSummary": {
        "operator": "Operator",
        "train-destination": "Train Destination",
        "train-status": "Train Status",
        "train-status-reason": "Reason for Status",
        "train-departure-time": "Departure Time",
        "train-arrival-time": "Arrival Time",
    },
}


def t(key: str, lang: str = "en"):
    key_parts = key.split(".")
    locales = EN

    try:
        for part in key_parts:
            locales = locales.get(part)  # pyrefly: ignore

        if not isinstance(locales, str):
            raise KeyError()

        return locales

    except (KeyError, AttributeError):
        return key


if __name__ == "__main__":
    key = t("trainStatus.ON_TIME")
    print(key)
