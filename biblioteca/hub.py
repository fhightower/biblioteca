#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid

from democritus_core import json_write, pdf_read, is_url, lowercase, url_file_name, url_domain, get, uuid3, html_to_text, map_first_arg

NAMESPACE = uuid.UUID(bytes=b'biblioteca000000')


def enrich_data(new_data):
    """Enrich the given data appropriately for its type."""
    es_data = {}

    if is_url(new_data):
        es_data['url'] = new_data
        url_file_ending = lowercase(url_file_name(new_data))
        domain_name = lowercase(url_domain(new_data))

        if url_file_ending.endswith('.pdf'):
            results = pdf_read(new_data)
            if any(results):
                es_data['raw'] = '\n\n'.join(results)
        else:
            if domain_name in ['youtube.com', 'youtu.be']:
                pass
            elif domain_name == 'github.com':
                pass
            elif domain_name == 'twitter.com':
                pass
            elif 'wikipedia' in domain_name:
                pass
            else:
                raw_data = get(new_data)
                if raw_data:
                    es_data['raw'] = html_to_text(raw_data)
    else:
        print('Something that was not a url was given and we aren\'t ready for this kind of data yet: {}'.format(new_data))

    return es_data


@map_first_arg
def add(new_data):
    """Add the new data to the library."""
    enriched_data = enrich_data(new_data)

    # TODO: need to create a file path somehow
    json_write(enriched_data, )
