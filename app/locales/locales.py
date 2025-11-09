EN = {
    "trainStatus": {
        "ON_TIME": "On time",
        "CANCELLED": "Cancelled",
        "DELAYED": "Delayed",
        "DEPARTED": "Departed",
        "DELAYED_DEPARTED": "Departed (Delayed)",
    }
}


def t(key: str, lang: str = "en"):
    key_parts = key.split(".")
    locales = EN

    try:
        for part in key_parts:
            locales = locales.get(part)

        if not isinstance(locales, str):
            raise KeyError()

        return locales

    except (KeyError, AttributeError):
        return key


if __name__ == "__main__":
    key = t("trainStatus.ON_TIME")
    print(key)
