from memory import Memory
from semantic_memory import SemanticMemory
from conversation_memory import ConversationMemory
from router import AgentRouter
from langchain_llm import LangChainLLM
from graph import build_agent_graph
from tools import (
    python_study_planner,
    ml_roadmap,
    data_science_roadmap
)

from local_llm import generate_response


class Agent:

    def __init__(self):

        # =====================================================
        # LONG-TERM MEMORY
        # =====================================================

        self.memory = Memory()

        self.semantic_memory = SemanticMemory()

        # =====================================================
        # SHORT-TERM MEMORY
        # =====================================================

        self.conversation_memory = ConversationMemory(
            max_messages=6
        )

        # =====================================================
        # AGENT ROUTER
        # =====================================================

        self.router = AgentRouter()

        self.langchain_llm = LangChainLLM()

        self.graph = build_agent_graph(self)

        # =====================================================
        # AGENT STATE
        # =====================================================

        self.meaningful_inputs = 0
        self.state = "listening"
        self.current_topic = None


    # =========================================================
    # MEMORY DETECTION
    # =========================================================

    def is_important(self, text):

        keywords = [
            "i am",
            "i want",
            "my goal",
            "i like",
            "i have interest",
            "i live",
            "i am in"
        ]

        text = text.lower()

        return any(
            keyword in text
            for keyword in keywords
        )


    # =========================================================
    # MEMORY QUESTION DETECTION
    # =========================================================

    def is_memory_question(self, text):

        questions = [
            "who am i",
            "what do you know about me",
            "what do you remember",
            "tell me about me",
            "do you remember me"
        ]

        text = text.lower()

        return any(
            question in text
            for question in questions
        )


    # =========================================================
    # CONFIDENCE
    # =========================================================

    def calculate_confidence(self, used_tool=False):

        score = 40

        memory_count = len(
            self.memory.get_all()
        )

        if memory_count >= 1:
            score += 15

        if memory_count >= 3:
            score += 15

        if used_tool:
            score += 20

        return min(score, 100)


    # =========================================================
    # LLM + MEMORY
    # =========================================================

    def generate_llm_response(self, user_input):

        # ========================================================
        # SEMANTIC MEMORY RETRIEVAL
        # ========================================================

        retrieved_memories = self.semantic_memory.search(
            user_input,
            top_k=5
        )

        relevant_memories = []

        for memory in retrieved_memories:

            score = memory.get("score", 0)
            text = memory.get("text", "").strip()

            if not text:
                continue

            if score < 0.30:
                continue

            relevant_memories.append({
                "text": text,
                "score": score
            })

        # ========================================================
        # BUILD MEMORY CONTEXT
        # ========================================================

        if relevant_memories:

            memory_context = "\n".join(
                f"- {item['text']}"
                for item in relevant_memories
            )

        else:

            memory_context = "No relevant user memory found."

        # ========================================================
        # SHORT-TERM CONVERSATION
        # ========================================================

        conversation_context = (
            self.conversation_memory.get_context()
        )

        # ========================================================
        # LANGCHAIN GENERATION
        # ========================================================

        response = self.langchain_llm.generate(
            question=user_input,
            memory=memory_context,
            conversation=conversation_context
        )

        # ========================================================
        # SAVE CONVERSATION
        # ========================================================

        self.conversation_memory.add(
            user_input,
            response
        )

        return response.strip()

    # =========================================================
    # ANSWER MEMORY QUESTION
    # =========================================================

        # =========================================================
    # ANSWER MEMORY QUESTION
    # =========================================================

    def answer_about_user(self, user_input):

        retrieved = self.semantic_memory.search(
            user_input,
            top_k=5
        )

        if not retrieved:

            return {
                "text": (
                    "I don't have any stored "
                    "information about that yet."
                ),
                "confidence": 50,
                "tool": "memory",
                "intent": "memory_retrieval"
            }

        # -----------------------------------------------------
        # KEEP RELEVANT RESULTS
        # -----------------------------------------------------

        relevant = []

        for memory in retrieved:

            score = memory.get(
                "score",
                0
            )

            if score >= 0.30:

                relevant.append(
                    memory
                )

        if not relevant:

            return {
                "text": (
                    "I don't have enough "
                    "stored information to "
                    "answer that yet."
                ),
                "confidence": 50,
                "tool": "memory",
                "intent": "memory_retrieval"
            }

        # -----------------------------------------------------
        # BUILD RESPONSE
        # -----------------------------------------------------

        response = (
            "Based on what I remember:\n\n"
        )

        for memory in relevant:

            response += (
                f"- {memory['text']}\n"
            )

        return {
            "text": response.strip(),
            "confidence": 95,
            "tool": "memory",
            "intent": "memory_retrieval"
        }

    # =========================================================
    # TOOL EXECUTION
    # =========================================================

    def run_tool(self, tool):

        if tool == "python":

            return python_study_planner()


        if tool == "ml":

            return ml_roadmap()


        if tool == "ds":

            return data_science_roadmap()


        return []


    # =========================================================
    # TOPIC TRACKING
    # =========================================================

    def update_topic(self, text):

        text = text.lower()


        if "dance" in text:

            self.current_topic = "dance"


        elif "football" in text:

            self.current_topic = "football"


        elif "python" in text:

            self.current_topic = "python"


        elif (
            "machine learning" in text
            or "ml" in text
            or "ai" in text
        ):

            self.current_topic = "aiml"


    # =========================================================
    # PROACTIVE RECOMMENDATION
    # =========================================================

    def proactive_recommendation(self):

        if self.current_topic == "dance":

            return (
                "Since you enjoy freestyle dancing:\n"
                "- Practice musicality and rhythm daily\n"
                "- Record yourself to refine movements\n"
                "- Learn complementary styles"
            )


        if self.current_topic == "football":

            return (
                "Since you like football:\n"
                "- Practice sprint drills\n"
                "- Work on dribbling\n"
                "- Improve finishing"
            )


        if self.current_topic == "aiml":

            return (
                "Since you're interested in AI/ML:\n"
                "- Strengthen Python\n"
                "- Learn ML fundamentals\n"
                "- Build practical projects"
            )


        return (
            "Tell me what you want help with right now 🙂"
        )


    # =========================================================
    # MAIN AGENT LOOP
    # =========================================================

        # =========================================================
    # MAIN AGENT LOOP
    # =========================================================

    def respond(self, user_input):

        text = user_input.lower().strip()

        # -----------------------------------------------------
        # EXIT
        # -----------------------------------------------------

        if text in [
            "exit",
            "bye",
            "quit"
        ]:

            return {
                "text": "Goodbye 👋",
                "confidence": 100,
                "tool": None,
                "intent": "exit"
            }

        # -----------------------------------------------------
        # UPDATE TOPIC
        # -----------------------------------------------------

        self.update_topic(
            text
        )

        # -----------------------------------------------------
        # SAVE IMPORTANT USER INFORMATION
        # -----------------------------------------------------

        if (
            self.is_important(user_input)
            and self.is_memory_candidate(user_input)
        ):

            self.memory.save(
                "user_fact",
                user_input
            )

            memory_type = (
                self.classify_memory(
                    user_input
                )
            )

            self.semantic_memory.add_memory(
                memory_type,
                user_input
            )

            self.meaningful_inputs += 1

        # -----------------------------------------------------
        # LANGGRAPH EXECUTION
        # -----------------------------------------------------

        initial_state = {
            "user_input": user_input
        }

        result = self.graph.invoke(
            initial_state
        )

        # -----------------------------------------------------
        # FINAL RESPONSE
        # -----------------------------------------------------

        return {
            "text": result.get(
                "final_response",
                "I could not generate a response."
            ),

            "confidence": int(
                result.get(
                    "confidence",
                    0.70
                ) * 100
            ),

            "tool": (
                result.get("tool")
                or (
                    "memory"
                    if result.get("intent")
                    == "memory_retrieval"
                    else "llm"
                )
            ),

            "intent": result.get(
                "intent",
                "general_question"
            )
        }
        # =========================================================
    # MEMORY CLASSIFICATION
    # =========================================================

    def classify_memory(self, text):
        text = text.strip().lower()

        # -----------------------------------------------------
        # CAREER / GOALS
        # -----------------------------------------------------

        if any(phrase in text for phrase in [
            "i want to become",
            "i want to be",
            "my goal is",
            "i want a career",
            "my career",
            "i aspire to"
        ]):
            return "career_goal"

        # -----------------------------------------------------
        # LEARNING
        # -----------------------------------------------------

        if any(phrase in text for phrase in [
            "i am learning",
            "i'm learning",
            "i want to learn",
            "i am studying",
            "i'm studying"
        ]):
            return "learning"

        # -----------------------------------------------------
        # PREFERENCES
        # -----------------------------------------------------

        if any(phrase in text for phrase in [
            "i like",
            "i love",
            "i enjoy",
            "i prefer"
        ]):
            return "preference"

        # -----------------------------------------------------
        # PERSONAL INFORMATION
        # -----------------------------------------------------

        if any(phrase in text for phrase in [
            "my name is",
            "i am from",
            "i live in"
        ]):
            return "personal"

        return "general"

    # =========================================================
    # MEMORY CANDIDATE DETECTION
    # =========================================================

    def is_memory_candidate(self, user_input):

        text = user_input.strip().lower()

        # -----------------------------------------------------
        # QUESTIONS SHOULD NOT BECOME LONG-TERM MEMORIES
        # -----------------------------------------------------

        question_starters = (
            "what ",
            "who ",
            "where ",
            "when ",
            "why ",
            "how ",
            "do i ",
            "did i ",
            "am i ",
            "can you ",
            "tell me ",
            "what's ",
            "whats "
        )

        if text.endswith("?"):
            return False

        if text.startswith(question_starters):
            return False

        # -----------------------------------------------------
        # PERSONAL FACT PATTERNS
        # -----------------------------------------------------

        memory_phrases = (
            "i am ",
            "i'm ",
            "i like ",
            "i love ",
            "i want ",
            "i enjoy ",
            "i prefer ",
            "my name is ",
            "my goal is ",
            "i'm learning ",
            "i am learning "
        )

        return text.startswith(memory_phrases)