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
        print("Agent:", reply)

except KeyboardInterrupt:
    print("\nAgent: Conversation ended safely. Bye 👋")
