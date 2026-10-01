from typing import TypedDict, Optional, List, Dict, Any

from langgraph.graph import StateGraph, START, END


# ============================================================
# AGENT STATE
# ============================================================

class AgentState(TypedDict, total=False):

    # User input
    user_input: str

    # Routing
    intent: str
    confidence: float

    # Memory
    needs_memory: bool
    retrieved_memories: List[str]
    retrieval_scores: List[float]

    # Tool
    needs_tool: bool
    tool: Optional[str]
    tool_result: Optional[Any]

    # LLM
    llm_response: Optional[str]

    # Final response
    final_response: str


# ============================================================
# ROUTER NODE
# ============================================================

def router_node(state: AgentState, agent):

    print("→ Router node")

    decision = agent.router.route(
        state["user_input"]
    )

    return {
        "intent": decision.intent,
        "confidence": decision.confidence,
        "needs_memory": decision.needs_memory,
        "needs_tool": decision.needs_tool,
        "tool": decision.tool,
    }


# ============================================================
# MEMORY NODE
# ============================================================

def memory_node(state, agent):
    print("→ Memory node")

    query = state["user_input"]

    memories = agent.semantic_memory.search(
        query,
        top_k=5
    )

    retrieved = []
    retrieval_scores = []
    seen = set()

    for memory in memories:
        text = memory.get("text", "").strip()
        score = float(memory.get("score", 0.0))

        if not text:
            continue

        normalized = text.lower()

        # Avoid duplicates
        if normalized in seen:
            continue

        # Don't return the user's question itself
        if normalized == query.lower().strip():
            continue

        # Minimum relevance threshold
        if score < 0.30:
            continue

        seen.add(normalized)

        retrieved.append(text)
        retrieval_scores.append(score)

    return {
        "retrieved_memories": retrieved,
        "retrieval_scores": retrieval_scores
    }

# ============================================================
# TOOL NODE
# ============================================================

def tool_node(state: AgentState, agent):

    print("→ Tool node")

    tool = state.get("tool")

    result = agent.run_tool(tool)

    return {
        "tool_result": result
    }


# ============================================================
# LLM NODE
# ============================================================

def llm_node(state: AgentState, agent):

    print("→ LLM node")

    memories = state.get(
        "retrieved_memories",
        []
    )

    if memories:

        memory_context = "\n".join(
            f"- {memory}"
            for memory in memories
        )

    else:

        memory_context = (
            "No relevant user memory found."
        )

    conversation_context = (
        agent.conversation_memory.get_context()
    )

    response = agent.langchain_llm.generate(
        question=state["user_input"],
        memory=memory_context,
        conversation=conversation_context
    )

    # Keep conversation memory updated
    agent.conversation_memory.add(
        state["user_input"],
        response
    )

    return {
        "llm_response": response
    }


# ============================================================
# RESPONSE NODE
# ============================================================

def response_node(state: AgentState):

    print("→ Response node")

    intent = state.get(
        "intent"
    )

    # --------------------------------------------------------
    # MEMORY RESPONSE
    # --------------------------------------------------------

    if intent == "memory_retrieval":

        memories = state.get(
            "retrieved_memories",
            []
        )

        if memories:

            response = (
                "Here's what I remember about you:\n\n"
            )

            for memory in memories:

                response += (
                    f"- {memory}\n"
                )

        else:

            response = (
                "I don't have any relevant "
                "memories about that yet."
            )

    # --------------------------------------------------------
    # TOOL RESPONSE
    # --------------------------------------------------------

    elif state.get("tool_result") is not None:

        tool = state.get(
            "tool",
            "tool"
        )

        result = state["tool_result"]

        if isinstance(result, list):

            response = (
                f"{tool.upper()} ROADMAP:\n\n"
            )

            for item in result:

                response += (
                    f"- {item}\n"
                )

        else:

            response = (
                f"{tool.upper()} ROADMAP:\n\n"
                f"{result}"
            )

    # --------------------------------------------------------
    # LLM RESPONSE
    # --------------------------------------------------------

    else:

        response = state.get(
            "llm_response",
            "I could not generate a response."
        )

    return {
        "final_response": response
    }


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

def route_after_router(state: AgentState):

    intent = state.get(
        "intent"
    )

    # Memory question
    if intent == "memory_retrieval":

        return "memory"

    # Tool request
    if state.get(
        "needs_tool",
        False
    ):

        return "tool"

    # Normal LLM request
    return "llm"


# ============================================================
# BUILD GRAPH
# ============================================================

def build_agent_graph(agent):

    graph = StateGraph(
        AgentState
    )

    # --------------------------------------------------------
    # NODES
    # --------------------------------------------------------

    graph.add_node(
        "router",
        lambda state: router_node(
            state,
            agent
        )
    )

    graph.add_node(
        "memory",
        lambda state: memory_node(
            state,
            agent
        )
    )

    graph.add_node(
        "tool",
        lambda state: tool_node(
            state,
            agent
        )
    )

    graph.add_node(
        "llm",
        lambda state: llm_node(
            state,
            agent
        )
    )

    graph.add_node(
        "response",
        response_node
    )

    # --------------------------------------------------------
    # START → ROUTER
    # --------------------------------------------------------

    graph.add_edge(
        START,
        "router"
    )

    # --------------------------------------------------------
    # ROUTER → MEMORY / TOOL / LLM
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "router",
        route_after_router,
        {
            "memory": "memory",
            "tool": "tool",
            "llm": "llm"
        }
    )

    # --------------------------------------------------------
    # EXECUTION → RESPONSE
    # --------------------------------------------------------

    graph.add_edge(
        "memory",
        "response"
    )

    graph.add_edge(
        "tool",
        "response"
    )

    graph.add_edge(
        "llm",
        "response"
    )

    # --------------------------------------------------------
    # RESPONSE → END
    # --------------------------------------------------------

    graph.add_edge(
        "response",
        END
    )

    return graph.compile()