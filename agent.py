# agent.py

from local_llm import generate_response
from tools import (
    python_study_planner,
    ml_roadmap,
    data_science_roadmap
)
from memory import Memory
from brain import detect_intent


class Agent:
    def __init__(self):
        self.memory = Memory()
        self.meaningful_inputs = 0
        self.state = "listening"

    # ---------- TOOL LOGIC ----------

    def should_use_tool(self, user_input):
        text = user_input.lower()

        if "python" in text and ("learn" in text or "study" in text or "plan" in text):
            return "python"

        if ("machine learning" in text or "ml" in text) and ("learn" in text or "roadmap" in text):
            return "ml"

        if ("data science" in text or "ds" in text) and ("learn" in text or "roadmap" in text):
            return "ds"

        return None

    def run_tool(self, tool_name):
        if tool_name == "python":
            return python_study_planner()

        if tool_name == "ml":
            return ml_roadmap()

        if tool_name == "ds":
            return data_science_roadmap()

        return []

    # ---------- MEMORY LOGIC ----------

    def is_important(self, text):
        keywords = [
            "i am", "i want", "my goal",
            "i have interest", "i like",
            "i live", "i am in"
        ]
        return any(k in text.lower() for k in keywords)

    def is_memory_question(self, text):
        questions = [
            "who am i",
            "what do you know about me",
            "do you remember me",
            "what do you remember",
            "tell me about me"
        ]
        text = text.lower()
        return any(q in text for q in questions)


    def answer_about_user(self):
        memories = self.memory.get_all()

        if not memories:
            return "I don’t know much about you yet. You can tell me about your interests or background."

        summary = "Here’s what I remember about you:\n"
        for m in memories:
            summary += f"- {m['text']}\n"

        return summary

    # ---------- AGENT DECISION ----------

    def decide_action(self, user_input):
        text = user_input.lower()

        if any(w in text for w in ["bye", "exit"]):
            return "end"

        if any(w in text for w in ["thank"]):
            return "polite_end"

        if any(w in text for w in ["bad", "useless"]):
            return "recover"

        if self.meaningful_inputs >= 2:
            return "recommend"

        return "listen"

    # ---------- MAIN RESPONSE ----------

    def respond(self, user_input):
        user_input_lower = user_input.lower()

        # 1️⃣ Memory questions
        if self.is_memory_question(user_input_lower):
            return self.answer_about_user()

        # 2️⃣ Exit
        if user_input_lower in ["exit", "bye", "bye bye"]:
            self.state = "ended"
            return "Goodbye 👋"

        if user_input_lower in ["thanks", "thank you"]:
            return "You’re welcome 😊"

        # 3️⃣ Intent
        #intent = detect_intent(user_input)

        if self.is_important(user_input):
            existing_memories = [m["text"].lower() for m in self.memory.get_all()]
            if user_input.lower() not in existing_memories:
                self.memory.save("user_fact", user_input)
                self.meaningful_inputs += 1


        # 5️⃣ TOOL PRIORITY
        tool_to_use = self.should_use_tool(user_input)
        if tool_to_use:
            plan = self.run_tool(tool_to_use)

            title_map = {
                "python": "📘 Python Learning Roadmap",
                "ml": "🤖 Machine Learning Roadmap",
                "ds": "📊 Data Science Roadmap"
            }

            raw_text = title_map.get(tool_to_use, "📘 Learning Roadmap") + ":\n"
            for step in plan:
                raw_text += f"- {step}\n"

            raw_text = f"(Tool used: {tool_to_use.upper()})\n\n" + raw_text
            prompt = f"""
            You are a friendly career mentor.

            TASK:
            Explain the following learning roadmap to a beginner.

            RULES:
            - Keep it simple
            - Use short sentences
            - Do NOT add extra topics
            - Do NOT repeat steps
            - Encourage the learner briefly at the end

            ROADMAP:
            {raw_text}
            """

            return generate_response(prompt)

        # 6️⃣ Other actions
        action = self.decide_action(user_input)

        if action == "recover":
            return "Alright 🙂 Let’s reset. What do you want to talk about?"

        if action == "recommend":
            return "I’ve shared my suggestions. Tell me if you want help with something else."

        # 7️⃣ Default LLM response
        memory_context = "\n".join(
            [f"- {m['text']}" for m in self.memory.get_all()]
        )

        prompt = f"""
        You are a personal AI assistant.
        KNOWN FACTS ABOUT USER:
        {memory_context}

        USER MESSAGE:
        {user_input}

        INSTRUCTIONS:
        - Reply in 2–4 sentences
        - Be clear and friendly
        - Use simple language
        - If unsure, give a suggestion, not a fact
        """

        return generate_response(prompt)
