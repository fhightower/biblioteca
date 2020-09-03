import datetime
import os
from typing import Tuple

from democritus_core import json_write, pdf_read, is_url, lowercase, url_file_name, url_domain, get, html_text, map_first_arg, home_directory_join, file_write, file_name_escape, DictStrKeyStrVal

BASE_PATH = home_directory_join('biblioteca/')


def get_data(new_data: str) -> Tuple[str, str, DictStrKeyStrVal]:
    """Enrich the given data appropriately for its type."""
    raw_data = None
    enriched_data = None
    meta_data = {
        'first_collected': str(datetime.date.today())
    }

    if is_url(new_data):
        meta_data['url'] = new_data
        url_file_ending = lowercase(url_file_name(new_data))
        domain_name = lowercase(url_domain(new_data))

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
            raw_data = get(new_data)
            enriched_data = html_text(raw_data)
    else:
        raw_data = new_data

    return raw_data, enriched_data, meta_data


@map_first_arg
def add(url: str, name: str = None) -> None:
    """Add the new data to the library."""
    raw_data, enriched_data, meta_data = get_data(url)

    if not name:
        name = file_name_escape(url)

    file_write(os.path.join(BASE_PATH, f'{name}.raw'), raw_data)
    if enriched_data:
        file_write(os.path.join(BASE_PATH, f'{name}.enriched'), enriched_data)
    json_write(os.path.join(BASE_PATH, f'{name}.meta'), meta_data)
