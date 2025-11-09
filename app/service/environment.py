import os

from dotenv import load_dotenv

load_dotenv()


def get_departure_token():
    return os.environ.get("PYRAIL_NATIONAL_RAIL_TOKEN")


def get_reference_data_token():
    return os.environ.get("PYRAIL_REFERENCE_DATA_TOKEN")


def get_destination():
    return os.environ.get("PYRAIL_DESTINATION")


def get_origin():
    return os.environ.get("PYRAIL_ORIGIN")
