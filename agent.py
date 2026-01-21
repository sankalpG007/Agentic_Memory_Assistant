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

    def respond(self, user_input):
            user_input_lower = user_input.lower()

            # Exit phrases
            if user_input_lower in ["exit", "bye", "thanks", "thank you"]:
                self.state = "ended"
                return "You're welcome 😊 All the best!"

            # End-of-input phrases
            if user_input_lower in ["thats it", "that's it", "nothing else", "done"]:
                self.state = "recommending"
                return self.proactive_summary()

            # If agent already recommended, don't repeat
            if self.state == "recommending":
                return "I’ve already shared my suggestions 👍 Let me know if you want help with something else."

            # Normal listening mode
            intent = detect_intent(user_input)

            if self.is_important(user_input):
                self.memory.save(intent, user_input)
                self.meaningful_inputs += 1

            # Switch to recommendation mode ONCE
            if self.meaningful_inputs >= 2:
                self.state = "recommending"
                return self.proactive_recommendation()

            return smart_fake_ai(user_input, self.memory.get_all())


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


