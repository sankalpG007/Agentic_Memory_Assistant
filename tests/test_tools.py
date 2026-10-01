import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tools


def test_python_tool():
    result = tools.python_study_planner()

    assert isinstance(result, list)
    assert len(result) > 0
    assert "Python basics" in result[0]


def test_ml_tool():
    result = tools.ml_roadmap()

    assert isinstance(result, list)
    assert len(result) > 0
    assert "Python + NumPy + Pandas" in result[0]


def test_data_science_tool():
    result = tools.data_science_roadmap()

    assert isinstance(result, list)
    assert len(result) > 0
    assert "Python programming" in result[0]


if __name__ == "__main__":
    test_python_tool()
    test_ml_tool()
    test_data_science_tool()

    print("\nAll tool tests passed successfully.")