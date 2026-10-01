from dataclasses import dataclass
from typing import Optional


@dataclass
class RouteDecision:
    intent: str
    needs_memory: bool
    needs_tool: bool
    tool: Optional[str]
    confidence: float


class AgentRouter:

    def __init__(self):
        pass

    def route(self, user_input):

        text = user_input.lower().strip()

        # =========================================================
        # EXPLICIT MEMORY QUESTIONS
        # =========================================================

        memory_questions = [
            "who am i",
            "what do you know about me",
            "what do you remember",
            "tell me about me",
            "do you remember me",
            "what is my name",
            "what do i like",
            "what am i learning",
            "what do i want to become",
            "what are my goals",

            # Career / goal questions
            "what is my goal",
            "what's my goal",
            "what are my goals",
            "what is my career goal",
            "what's my career goal",
            "what career do i want",
            "what career do i want to pursue",
            "what do i want to be",
            "what am i aiming for",
            "what do i want to achieve"
        ]

        if any(
            phrase in text
            for phrase in memory_questions
        ):
            return RouteDecision(
                intent="memory_retrieval",
                needs_memory=True,
                needs_tool=False,
                tool=None,
                confidence=0.95
            )

        # =========================================================
        # PYTHON
        # =========================================================

        python_requests = [
            "python roadmap",
            "python study plan",
            "python learning plan",
            "roadmap to learn python",
            "how should i learn python",
            "how can i learn python",
            "teach me python",
            "help me learn python",
            "python learning roadmap"
        ]

        if any(
            phrase in text
            for phrase in python_requests
        ):
            return RouteDecision(
                intent="learning_plan",
                needs_memory=True,
                needs_tool=True,
                tool="python",
                confidence=0.95
            )

        # =========================================================
        # MACHINE LEARNING
        # =========================================================

        ml_requests = [
            "machine learning roadmap",
            "ml roadmap",
            "roadmap for machine learning",
            "how should i learn machine learning",
            "how can i learn machine learning",
            "machine learning study plan",
            "ml study plan"
        ]

        if any(
            phrase in text
            for phrase in ml_requests
        ):
            return RouteDecision(
                intent="learning_plan",
                needs_memory=True,
                needs_tool=True,
                tool="ml",
                confidence=0.95
            )

        # =========================================================
        # DATA SCIENCE
        # =========================================================

        ds_requests = [
            "data science roadmap",
            "ds roadmap",
            "roadmap for data science",
            "how should i learn data science",
            "how can i learn data science",
            "data science study plan"
        ]

        if any(
            phrase in text
            for phrase in ds_requests
        ):
            return RouteDecision(
                intent="learning_plan",
                needs_memory=True,
                needs_tool=True,
                tool="ds",
                confidence=0.95
            )

        # =========================================================
        # GENERAL QUESTION
        # =========================================================

        return RouteDecision(
            intent="general_question",
            needs_memory=True,
            needs_tool=False,
            tool=None,
            confidence=0.70
        )