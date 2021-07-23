from sklearn.datasets import load_boston
import pandas as pd
from ..eda import EDA
import pytest

@pytest.fixture(scope="session")
def test_data(request):
    # prepare something ahead of all tests
    data = load_boston()
    data = pd.DataFrame(data['data'], columns=data['feature_names'])
    cat = ['RAD', 'CHAS']
    cont = ['CRIM', 'ZN', 'INDUS', 'NOX', 'RM', 'AGE', 'DIS','TAX', 'PTRATIO', 'B', 'LSTAT']

    for k, v in data.dtypes.items():
        if k in cat:
            data[k] = data[k].astype('int')
        else:
            data[k] = data[k].astype('float')

    data_eda = EDA(data, cat, cont)
    data_eda._calc_number_of_dtypes()
    return data_eda

# _calc_number_of_features_dtypes test
def test_dtypes_len(test_data):
    assert len(test_data.num_dtypes) == 6

def test_dtypes_float_count(test_data):
    assert 11 == test_data.num_dtypes['float']

def test_dtypes_int_count(test_data):
    assert 2 == test_data.num_dtypes['int']

def test_dtypes_other_count(test_data):
    assert 0 == test_data.num_dtypes['other']

# _calculate_number_of_missing_values test
def test_missing_data(test_data):
    missing = test_data._calculate_number_of_missing_values(percentage=False, plot=False)
    assert missing[0] == 0

# head test
def test_head(test_data):
    assert test_data.head(10).shape[0] == 10