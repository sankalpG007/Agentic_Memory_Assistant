# agent.py

from memory import Memory
from brain import smart_fake_ai, detect_intent

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.meaningful_inputs = 0
        self.state = "listening"



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

        response = "Here’s what I remember about you:\n"
        for m in memories:
            response += f"- {m['text']}\n"

        return response



    def respond(self, user_input):
        user_input_lower = user_input.lower()

        # 1️⃣ Answer memory questions
        if self.is_memory_question(user_input_lower):
            return self.answer_about_user()

        # 2️⃣ Exit / polite endings
        if user_input_lower in ["exit", "bye", "bye bye"]:
            self.state = "ended"
            return "Goodbye 👋"

        if user_input_lower in ["thanks", "thank you"]:
            return "You’re welcome 😊"

        # 3️⃣ Detect intent FIRST
        intent = detect_intent(user_input)

        # 4️⃣ SAVE MEMORY BEFORE ANY DECISION
        if self.is_important(user_input):
            self.memory.save(intent, user_input)
            self.meaningful_inputs += 1

        # 5️⃣ Decide action AFTER memory is saved
        action = self.decide_action(user_input)

        if action == "recover":
            self.state = "listening"
            return "Alright 🙂 What would you like to talk about?"

        if action == "recommend":
            self.state = "recommending"
            return self.proactive_recommendation()

        # 6️⃣ Default listening response
        return smart_fake_ai(user_input, self.memory.get_all())

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


    def proactive_summary(self):
            memories = self.memory.get_all()

            if not memories:
                return "Alright 👍 If you need help later, just tell me."

            summary = "Here’s what I know about you so far:\n"
            for m in memories:
                summary += f"- {m['text']}\n"

            summary += "\nBased on this, I can guide you further anytime."
            return summary
        
    def proactive_recommendation(self):
            memories = self.memory.get_all()
            texts = " ".join([m["text"].lower() for m in memories])

            # Football logic
            if "football" in texts:
                if "shoot" in texts or "shooting" in texts:
                    return (
                        "Since you like football and want to improve shooting:\n"
                        "1️⃣ Practice inside-foot shots daily\n"
                        "2️⃣ Do target shooting drills\n"
                        "3️⃣ Watch Lionel Messi’s finishing techniques\n"
                        "4️⃣ Use your speed to create shooting angles"
                    )
                return (
                    "You like football. Start with ball control, passing, and basic drills.\n"
                    "Once comfortable, focus on shooting and positioning."
                )

            # AIML logic
            if "aiml" in texts or "ai" in texts:
                return (
                    "Since you’re interested in AI/ML:\n"
                    "1️⃣ Strengthen Python basics\n"
                    "2️⃣ Learn ML fundamentals\n"
                    "3️⃣ Build small projects\n"
                    "4️⃣ Practice consistently"
                )

            return "Based on what you shared, focus on skill-building and daily practice."


