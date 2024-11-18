import requests

from datetime import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def parse(_source_url, _elements_per_page, _parsed_fields):
    try:
        response = requests.get(url=_source_url, params={"per_page": _elements_per_page, "_fields": _parsed_fields})
        response.raise_for_status()
        entries = response.json()

        return [{
            "title": entry["title"]["rendered"],
            "date": str(datetime.strptime(entry["date"], '%Y-%m-%dT%H:%M:%S').date()),
            "url": entry["link"],
        } for entry in entries]

    except requests.RequestException as e:
        print(f"Error fetching posts: {e}")
        return []


def post_entries(_destination_url, _entries):
    try:
        res = requests.post(_destination_url, json=_entries)
        res.raise_for_status()
        return "Successfully posted the parsed data"

    except requests.RequestException as e:
        return f"Error fetching posts: {e}"


def lambda_handler(event, context):

    SOURCE_API_URL = getenv('SOURCE_API_URL')
    ELEMENTS_PER_PAGE = int(getenv('ELEMENTS_PER_PAGE'))
    PARSED_FIELDS = getenv('PARSED_FIELDS')
    DESTINATION_API_URL = getenv('DESTINATION_API_URL')

    parsed_entries = parse(SOURCE_API_URL, ELEMENTS_PER_PAGE, PARSED_FIELDS)
    return post_entries(DESTINATION_API_URL, parsed_entries)
