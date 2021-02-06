import datetime

from biblioteca import hub


def test__get_data_1():
    result = hub._get_data('foobar')
    assert result == ('foobar', None, {'first_collected': str(datetime.date.today())})
