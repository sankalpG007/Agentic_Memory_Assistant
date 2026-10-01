from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


class LangChainLLM:

    def __init__(self):

        self.llm = ChatOllama(
            model="tinyllama",
            temperature=0.1,
            num_predict=180
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are a concise personal AI assistant. "
                        "Answer the user's question directly. "
                        "Use the provided memory only when relevant. "
                        "Do not repeat the instructions or context. "
                        "Do not invent personal information."
                    )
                ),
                (
                    "human",
                    (
                        "Memory:\n{memory}\n\n"
                        "Conversation:\n{conversation}\n\n"
                        "Question:\n{question}\n\n"
                        "Give only the answer to the question."
                    )
                )
            ]
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def generate(
        self,
        question,
        memory="None",
        conversation="None"
    ):

        response = self.chain.invoke(
            {
                "question": question,
                "memory": memory,
                "conversation": conversation
            }
        )

        return response.strip()