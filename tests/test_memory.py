import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from semantic_memory import SemanticMemory


def test_memory_retrieval():
    memory = SemanticMemory()

    results = memory.search(
        "What am I learning?",
        top_k=5
    )

    assert len(results) > 0

    texts = [
        item["text"]
        for item in results
    ]

    assert any(
        "python" in text.lower()
        for text in texts
    )


if __name__ == "__main__":
    test_memory_retrieval()

    print("\nSemantic memory test passed successfully.")