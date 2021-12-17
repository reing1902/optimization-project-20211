from project9.data_model import Data
import os

if __name__ == '__main__':
    data = Data.generated_with(6, 2)
    assert data.N == 6
    assert data.K == 2
    assert len(data.d) == 6
    assert len(data.t) == 7
    assert len(data.t[0]) == 7
