# agent.py
from memory import Memory
from tools import python_study_planner, ml_roadmap, data_science_roadmap


class Agent:
    def __init__(self):
        self.memory = Memory()
        self.meaningful_inputs = 0
        self.state = "listening"

    # ---------- HELPERS ----------

    def is_important(self, text):
        keywords = [
            "i am", "i want", "my goal",
            "i like", "i have interest",
            "i live", "i am in"
        ]
        return any(k in text.lower() for k in keywords)

    def is_memory_question(self, text):
        questions = [
            "who am i",
            "what do you know about me",
            "what do you remember",
            "tell me about me",
            "do you remember me"
        ]
        return any(q in text.lower() for q in questions)

    def calculate_confidence(self, used_tool=False):
        score = 40
        memory_count = len(self.memory.get_all())

        if memory_count >= 1:
            score += 15
        if memory_count >= 3:
            score += 15
        if used_tool:
            score += 20

        return min(score, 100)

    # ---------- MEMORY ----------

    def answer_about_user(self):
        memories = self.memory.get_all()

        if not memories:
            return {
                "text": "I don’t know much about you yet. Tell me something about yourself 🙂",
                "confidence": 30,
                "tool": "memory"
            }

        unique = {}
        for m in memories:
            key = m["text"].lower()
            unique[key] = m["text"]

        text = "Here’s what I remember about you:\n"
        for fact in unique.values():
            text += f"- {fact}\n"

        return {
            "text": text,
            "confidence": self.calculate_confidence(),
            "tool": "memory"
        }

    # ---------- TOOLS ----------

    def should_use_tool(self, text):
        t = text.lower()

        if "python" in t and "learn" in t:
            return "python"
        if "machine learning" in t or "ml roadmap" in t:
            return "ml"
        if "data science" in t or "ds roadmap" in t:
            return "ds"

        return None

    def run_tool(self, tool):
        if tool == "python":
            return python_study_planner()
        if tool == "ml":
            return ml_roadmap()
        if tool == "ds":
            return data_science_roadmap()
        return []

    # ---------- AGENTIC BEHAVIOR ----------

    def proactive_recommendation(self):
        memories = self.memory.get_all()
        text_blob = " ".join(m["text"].lower() for m in memories)

        if "football" in text_blob:
            if "fast" in text_blob or "run" in text_blob:
                return (
                    "Since you like football and you’re fast:\n"
                    "- Play as a winger or forward\n"
                    "- Do sprint + dribbling drills\n"
                    "- Practice shooting while running\n"
                )
            return (
                "Since you like football:\n"
                "- Improve ball control\n"
                "- Work on passing and shooting\n"
            )

        if "ai" in text_blob or "ml" in text_blob:
            return (
                "Since you’re interested in AI/ML:\n"
                "- Strengthen Python basics\n"
                "- Learn ML fundamentals\n"
                "- Build small projects"
            )

        return "Based on what you shared, keep practicing and learning consistently."

    # ---------- MAIN ----------

    def respond(self, user_input):
        text = user_input.lower()

        # Memory questions
        if self.is_memory_question(text):
            return self.answer_about_user()

        # Exit
        if text in ["exit", "bye"]:
            return {"text": "Goodbye 👋", "confidence": 100, "tool": None}

        # Save memory
        if self.is_important(user_input):
            self.memory.save("user_fact", user_input)
            self.meaningful_inputs += 1

        # Tool usage
        tool = self.should_use_tool(user_input)
        if tool:
            plan = self.run_tool(tool)
            response = f"{tool.upper()} ROADMAP:\n"
            for step in plan:
                response += f"- {step}\n"

            return {
                "text": response,
                "confidence": self.calculate_confidence(used_tool=True),
                "tool": tool
            }

        # One-time recommendation
        if self.meaningful_inputs >= 2 and self.state != "recommended":
            self.state = "recommended"
            return {
                "text": self.proactive_recommendation(),
                "confidence": self.calculate_confidence(),
                "tool": "recommendation"
            }

        # Default
        return {
            "text": "Tell me more 🙂 I’m learning about you.",
            "confidence": 50,
            "tool": None
        }
