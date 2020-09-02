import datetime
import uuid

from democritus_core import json_write, pdf_read, is_url, lowercase, url_file_name, url_domain, get, uuid3, html_text, map_first_arg, home_directory_join, file_write

NAMESPACE = uuid.UUID(bytes=b'biblioteca000000')
BASE_PATH = home_directory_join('biblioteca/')


def enrich_data(new_data):
    """Enrich the given data appropriately for its type."""
    raw_data = None
    enrich_data = None
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
                enrich_data = '\n\n'.join(results)
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
def add(new_data, name):
    """Add the new data to the library."""
    raw_data, enriched_data, meta_data = enrich_data(new_data)

    name = uuid3(name, namespace=NAMESPACE)

    file_write(os.path.join(BASE_PATH, f'{name}.raw'), new_data)
    if enriched_data:
        file_write(os.path.join(BASE_PATH, f'{name}.enriched'), enriched_data)
    json_write(os.path.join(BASE_PATH, f'{name}.meta'), meta_data)
