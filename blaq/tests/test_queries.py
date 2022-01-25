import pytest

from blaq.queries import is_json_dict


json_samples = [
    ("{'key': 'val'}", False),
    (10, False),
    ('10', False),
    ('true', False),
    ('false', False),
    ('10.0', False),
    (1223.3, False),
    ('[1, 2, 3]', False),
    ('{}', True),
    ('{"key": "val"}', True),
    ('{"key": true}', True),
    ('{"key": false}', True),
    ('{"key": 10}', True),
    ('{"key": 10.0}', True),
    ('{"key": "10.0"}', True),
]


@pytest.mark.parametrize("test_inp, exp", json_samples)
def test_is_json(test_inp, exp):
    assert is_json_dict(test_inp) == exp
