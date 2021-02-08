import datetime
import os
from typing import Dict, Optional, Tuple

from democritus_json import json_write
from democritus_pdfs import pdf_read
from democritus_urls import is_url, url_file_name, url_domain, url_scheme_remove
from democritus_networking import get
from democritus_html import html_text
from democritus_file_system import home_directory_join, file_write, file_name_escape
from democritus_utility import map_first_arg

try:
    BASE_PATH = os.environ['BIBLIOTECA_BASE_PATH']
except KeyError as e:
    message = (
        'Biblioteca expects an environment variable named "BIBLIOTECA_BASE_PATH", but it could not find it. '
        + 'Please set this variable and re-run biblioteca. '
        + 'If you have any questions, feel free to raise an issue here: https://github.com/fhightower/biblioteca/issues.'
    )
    raise RuntimeError(message) from e
MetadataType = Dict[str, str]


def _get_data(new_data: str) -> Tuple[str, str, MetadataType]:
    """Enrich the given data appropriately for its type."""
    raw_data = None
    enriched_data = None
    meta_data = {'first_collected': str(datetime.date.today())}

    if is_url(new_data):
        meta_data['url'] = new_data
        url_file_ending = url_file_name(new_data).lower()
        domain_name = url_domain(new_data).lower()

        raw_data = get(new_data, process_response=True)
        if url_file_ending.endswith('.pdf'):
            results = pdf_read(new_data)
            if any(results):
                enriched_data = '\n\n'.join(results)
        else:
            # if domain_name in ['youtube.com', 'youtu.be']:
            #     pass
            # elif domain_name == 'github.com':
            #     pass
            # elif domain_name == 'twitter.com':
            #     pass
            # elif 'wikipedia' in domain_name:
            #     pass
            # else:
            #     pass
            enriched_data = html_text(raw_data)
    else:
        raw_data = new_data

    return raw_data, enriched_data, meta_data


def _save_data(raw_data: str, enriched_data: str, meta_data: MetadataType, name: str):
    """."""
    file_write(os.path.join(BASE_PATH, f'{name}.raw'), raw_data)
    if enriched_data:
        file_write(os.path.join(BASE_PATH, f'{name}.enriched'), enriched_data)
    json_write(os.path.join(BASE_PATH, f'{name}.meta'), meta_data)
    message = f'Done with {name}!'
    print(message)


@map_first_arg
def add(url: str, name: str = None) -> None:
    """Add the new data to the library."""
    if not name:
        cleaner_url = url_scheme_remove(url)
        name = file_name_escape(cleaner_url)

    raw_data, enriched_data, meta_data = _get_data(url)
    _save_data(raw_data, enriched_data, meta_data, name)
