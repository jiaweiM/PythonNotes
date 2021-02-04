from operator import attrgetter
from operator import itemgetter


def test_itemgetter():
    # dict
    assert itemgetter('name')({'name': 'swan', 'age': 18}) == 'swan'
    # string
    assert itemgetter(1)('ABCDEFG') == 'B'
    assert itemgetter(1, 3, 5)('ABCDEFG') == ('B', 'D', 'F')
    assert itemgetter(slice(2, None))('ABCDEFG') == 'CDEFG'


def test_attrgetter():
    class User:
        def __init__(self, name):
            self.name = name

    get_name = attrgetter('name')
    assert get_name(User('swan')) == 'swan'