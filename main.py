# main.py

from agent import Agent

agent = Agent()

print("Free Agentic AI Assistant (type 'exit' or Ctrl+C to quit)")

try:
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Agent: Goodbye 👋")
            break

        reply = agent.respond(user_input)
        if isinstance(reply, dict):
            print(f"Agent: {reply['text']}")
            print(f"Confidence: {reply['confidence']}%")
        else:
            print(f"Agent: {reply}")


except KeyboardInterrupt:
    print("\nAgent: Conversation ended safely. Bye 👋")
