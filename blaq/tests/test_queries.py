import pandas as pd
import pytest

from blaq.queries import columnify_json, is_json_dict

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


json_dfs = [
    ({'col': [1, 2, 4]}, {'col'}),
    ({'col': []}, {'col'}),
    ({'col': ['{"key": 1}', '{"key": 4}']}, {'key'}),
    ({'col': ['{"foo": 1}', '{"bar": 4}']}, {'foo', 'bar'}),
]


@pytest.mark.parametrize("test_inp, exp", json_dfs)
def test_columnify_json(test_inp, exp):
    df = pd.DataFrame(test_inp)
    assert set(columnify_json(df).columns) == exp
