import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent import Agent
from semantic_memory import SemanticMemory


def test_existing_memory_retrieval():
    memory = SemanticMemory()

    results = memory.search("What am I learning?", top_k=5)

    assert len(results) > 0

    texts = [item["text"] for item in results]

    assert any("python" in text.lower() for text in texts)


def test_memory_classification():
    agent = Agent()

    assert agent.classify_memory(
        "My favorite programming language is Python."
    ) == "preference"


def test_memory_question_routing():
    agent = Agent()

    decision = agent.router.route(
        "What is my favorite programming language?"
    )

    assert decision.intent == "memory_retrieval"
    assert decision.needs_memory is True


if __name__ == "__main__":
    test_existing_memory_retrieval()
    test_memory_classification()
    test_memory_question_routing()

    print("\nAll memory tests passed successfully.")

def test_end_to_end_preference_memory():
    agent = Agent()

    statement = "My favorite programming language is Python."

    agent.respond(statement)

    results = agent.semantic_memory.search(
        "What is my favorite programming language?",
        top_k=5
    )

    texts = [item["text"] for item in results]

    assert any(
        "favorite programming language" in text.lower()
        and "python" in text.lower()
        for text in texts
    )