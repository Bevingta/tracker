import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tracker import time_to_dhmsm

@pytest.mark.parametrize(
        "seconds, expected", [
            (1234.4, "20m, 34.400s"),
            (28.56, "28.560s"),
            (1395820.8, "16d, 3h, 43m, 40.800s")
            ]) 

def test_time_to_dhmsm(seconds, expected):
    result_string = time_to_dhmsm(seconds)
    assert result_string == expected
