# agent.py
from memory import Memory
from tools import python_study_planner, ml_roadmap, data_science_roadmap


class Agent:
    def __init__(self):
        self.memory = Memory()
        self.meaningful_inputs = 0
        self.state = "listening"
        self.current_topic = None

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
        topic = self.current_topic

        if topic == "dance":
            return (
                "Since you enjoy freestyle dancing:\n"
                "- Practice musicality and rhythm daily\n"
                "- Record yourself to refine movements\n"
                "- Learn styles that complement freestyle (hip-hop, popping)\n"
                "- Freestyle to different genres for creativity"
            )

        if topic == "football":
            return (
                "Since you like football and you’re fast:\n"
                "- Play as a winger or forward\n"
                "- Practice sprint + dribbling drills\n"
                "- Work on finishing while running"
            )

        if topic == "aiml":
            return (
                "Since you’re interested in AI/ML:\n"
                "- Strengthen Python fundamentals\n"
                "- Learn ML basics step by step\n"
                "- Build small projects consistently"
            )

        return "Tell me what you want help with right now 🙂"

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

            if "dance" in user_input.lower():
                self.current_topic = "dance"
            elif "football" in user_input.lower():
                self.current_topic = "football"
            elif "python" in user_input.lower():
                self.current_topic = "python"
            elif "ml" in user_input.lower() or "ai" in user_input.lower():
                self.current_topic = "aiml"

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

        if self.meaningful_inputs >= 2:
            return {
                "text": (
                    "I think I know enough to help you now 🙂\n"
                    "You can ask me for advice, recommendations, or say 'what do you know about me?'."
                ),
                "confidence": self.calculate_confidence(),
                "tool": None
                }

        return {
            "text": "Got it 👍 Tell me one more thing about you if you’d like.",
            "confidence": 45,
            "tool": None
        }

