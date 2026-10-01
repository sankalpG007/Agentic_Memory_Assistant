import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent import Agent


def test_memory_route():
    agent = Agent()

    result = agent.respond("What do I like?")

    assert result["intent"] == "memory_retrieval"
    assert result["tool"] == "memory"
    assert "dance" in result["text"].lower()


def test_python_tool_route():
    agent = Agent()

    result = agent.respond("Give me a Python roadmap.")

    assert result["intent"] == "learning_plan"
    assert result["tool"] == "python"
    assert "Python basics" in result["text"]


def test_ml_tool_route():
    agent = Agent()

    result = agent.respond("Give me a machine learning roadmap.")

    assert result["intent"] == "learning_plan"
    assert result["tool"] == "ml"
    assert "Machine Learning algorithms" in result["text"]


def test_general_llm_route():
    agent = Agent()

    result = agent.respond("Explain recursion.")

    assert result["intent"] == "general_question"
    assert result["tool"] == "llm"
    assert len(result["text"]) > 0


if __name__ == "__main__":
    test_memory_route()
    test_python_tool_route()
    test_ml_tool_route()
    test_general_llm_route()

    print("\nAll graph tests passed successfully.")