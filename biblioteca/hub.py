#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid

from democritus import pdfRead, isUrl, lowercase, urlFileName, urlDomain, reqGet, esAdd, uuid3, html2Text

NAMESPACE = uuid.UUID(bytes=b'biblioteca000000')


def enrich_data(new_data):
    """."""
    es_data = {}

    if isUrl(new_data):
        es_data['url'] = new_data
        url_file_ending = lowercase(urlFileName(new_data))
        domain_name = lowercase(urlDomain(new_data))

        if url_file_ending.endswith('.pdf'):
            results = pdfRead(new_data)
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
                raw_data = reqGet(new_data)
                if raw_data:
                    es_data['raw'] = html2Text(raw_data)
    else:
        print('Something that was not a url was given and we aren\'t ready for this kind of data yet: {}'.format(new_data))

    return es_data


def add(new_data, entry_type='library', id=None, note=None):
    """Add the new data to the library."""
    # handle incoming data in a list
    if isinstance(new_data, list):
        results = []
        for data in new_data:
            results.append(add(data, entry_type=entry_type, id=id, note=note))
        return results

    enriched_data = enrich_data(new_data)

    if note:
        enriched_data['note'] = note

    # TODO: may want to add a check to see if the item at the given id exists
    # TODO: improve error handling
    if id:
        return esAdd('biblioteca', entry_type, enriched_data, id=id)
    else:
        return esAdd('biblioteca', entry_type, enriched_data, id=uuid3(enriched_data['url'], namespace=NAMESPACE))
