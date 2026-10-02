from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


class LangChainLLM:
    def __init__(self):
        self.llm = ChatOllama(
            model="tinyllama",
            temperature=0.1,
            num_predict=120
        )

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful assistant. Answer the user's question directly. "
                "Do not repeat the instructions or question."
            ),
            (
                "human",
                "{question}"
            )
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    def generate(self, question, memory="None", conversation="None"):
        context = ""

        if memory and memory != "No relevant user memory found.":
            context += f"Relevant user information:\n{memory}\n\n"

        if conversation and conversation != "No previous conversation.":
            context += f"Recent conversation:\n{conversation}\n\n"

        if context:
            prompt = (
                f"{context}"
                f"Answer this user question directly:\n{question}"
            )
        else:
            prompt = question

        response = self.llm.invoke(
            self.prompt.format_messages(question=prompt)
        )

        return response.content.strip()