from sklearn.datasets import load_boston
import pandas as pd

@pytest.fixture(scope="session")
def test_data(request):
    # prepare something ahead of all tests
    data = load_boston()
    return pd.DataFrame(data['data'], columns=data['feature_names'])
