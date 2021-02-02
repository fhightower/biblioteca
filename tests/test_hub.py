import datetime

from biblioteca import hub


def test_get_data_1():
    result = hub.get_data('foobar')
    assert result == ('foobar', None, {'first_collected': str(datetime.date.today())})
