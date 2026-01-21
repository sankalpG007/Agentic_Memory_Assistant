# brain.py

def detect_intent(text):
    text = text.lower()

    if "aiml" in text or "ai" in text or "ml" in text:
        return "career"
    if "interview" in text or "job" in text:
        return "career"
    if "learn" in text or "study" in text:
        return "learning"
    if "final year" in text or "student" in text:
        return "education"
    if "india" in text or "live" in text:
        return "personal"

    return "general"


def smart_fake_ai(user_input, memory):
    intent = detect_intent(user_input)

    # Filter relevant memory
    relevant_memory = [m["text"] for m in memory if m["type"] == intent]

    if intent == "career":
        if relevant_memory:
            return (
                f"I remember you mentioned: '{relevant_memory[-1]}'. "
                "You should focus on core concepts, practice problems, and revise daily."
            )
        return "Career growth is important. What role are you preparing for?"

    if intent == "learning":
        if relevant_memory:
            return (
                f"Since you're learning '{relevant_memory[-1]}', "
                "start with basics, then build small projects."
            )
        return "What skill are you trying to learn?"

    if intent == "goal":
        return "That's a great goal. Let's break it into small actionable steps."
    
    if intent == "education":
        if relevant_memory:
            return (
            f"You mentioned you're in '{relevant_memory[-1]}'. "
            "This is a crucial time to focus on skills, projects, and internships."
        )
        return "Are you a student or working professional?"

    if intent == "personal":
        if relevant_memory:
            return (
            f"I know you're based in '{relevant_memory[-1]}'. "
            "I can tailor suggestions relevant to your location."
        )
        return "Where are you currently based?"

    return "Tell me more so I can assist you better."
