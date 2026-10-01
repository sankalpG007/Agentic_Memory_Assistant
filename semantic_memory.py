import os
import json
import re

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


MEMORY_FILE = ".streamlit/memory.json"
INDEX_FILE = ".streamlit/memory.index"


class SemanticMemory:

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.dimension = (
            self.model.get_embedding_dimension()
        )

        if os.path.exists(INDEX_FILE):
            self.index = faiss.read_index(
                INDEX_FILE
            )
        else:
            self.index = faiss.IndexFlatIP(
                self.dimension
            )

        self.sync_index()

    # =========================================================
    # LOAD MEMORIES
    # =========================================================

    def load_memories(self):

        if not os.path.exists(MEMORY_FILE):
            return []

        try:
            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except Exception:
            return []

    # =========================================================
    # SAVE INDEX
    # =========================================================

    def save_index(self):

        os.makedirs(
            os.path.dirname(INDEX_FILE),
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            INDEX_FILE
        )

    # =========================================================
    # SYNCHRONIZE FAISS INDEX
    # =========================================================

    def sync_index(self):

        memories = self.load_memories()

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        if not memories:
            self.save_index()
            return

        texts = [
            memory.get("text", "")
            for memory in memories
            if memory.get("text")
        ]

        if not texts:
            self.save_index()
            return

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(
            embeddings
        )

        self.save_index()

    # =========================================================
    # QUERY CATEGORY
    # =========================================================

    def infer_query_category(self, query):

        text = query.lower().strip()

        # -----------------------------------------------------
        # CAREER / GOALS
        # -----------------------------------------------------

        career_terms = [
            "goal",
            "goals",
            "career",
            "become",
            "aspire",
            "aim",
            "future",
            "want to be",
            "want to become"
        ]

        if any(
            term in text
            for term in career_terms
        ):
            return "career_goal"

        # -----------------------------------------------------
        # LEARNING
        # -----------------------------------------------------

        learning_terms = [
            "learning",
            "learn",
            "studying",
            "study",
            "education",
            "skill",
            "skills"
        ]

        if any(
            term in text
            for term in learning_terms
        ):
            return "learning"

        # -----------------------------------------------------
        # PREFERENCES
        # -----------------------------------------------------

        preference_terms = [
            "like",
            "love",
            "enjoy",
            "prefer",
            "favorite",
            "favourite",
            "interest",
            "hobby"
        ]

        if any(
            term in text
            for term in preference_terms
        ):
            return "preference"

        # -----------------------------------------------------
        # PERSONAL
        # -----------------------------------------------------

        personal_terms = [
            "name",
            "live",
            "from",
            "location",
            "personal"
        ]

        if any(
            term in text
            for term in personal_terms
        ):
            return "personal"

        return None

    # =========================================================
    # KEYWORD SCORE
    # =========================================================

    def keyword_score(self, query, memory_text):

        query_words = set(
            re.findall(
                r"\b[a-zA-Z]{3,}\b",
                query.lower()
            )
        )

        memory_words = set(
            re.findall(
                r"\b[a-zA-Z]{3,}\b",
                memory_text.lower()
            )
        )

        if not query_words or not memory_words:
            return 0.0

        overlap = (
            query_words & memory_words
        )

        return len(overlap) / len(
            query_words
        )

    # =========================================================
    # ADD MEMORY
    # =========================================================

    def add_memory(self, intent, text):

        memories = self.load_memories()

        normalized_text = (
            text.strip().lower()
        )

        for memory in memories:

            existing = (
                memory.get("text", "")
                .strip()
                .lower()
            )

            if existing == normalized_text:
                return

        memories.append({
            "intent": intent,
            "text": text
        })

        os.makedirs(
            os.path.dirname(MEMORY_FILE),
            exist_ok=True
        )

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                memories,
                file,
                indent=4
            )

        self.sync_index()

    # =========================================================
    # HYBRID MEMORY SEARCH
    # =========================================================

    def search(
        self,
        query,
        top_k=5
    ):

        memories = self.load_memories()

        if not memories:
            return []

        # -----------------------------------------------------
        # SEMANTIC SEARCH
        # -----------------------------------------------------

        semantic_scores = {}

        if self.index.ntotal > 0:

            embedding = self.model.encode(
                [query],
                normalize_embeddings=True
            )

            embedding = np.asarray(
                embedding,
                dtype="float32"
            )

            # Retrieve more candidates than required.
            candidate_k = min(
                max(top_k * 3, 10),
                self.index.ntotal
            )

            scores, indices = (
                self.index.search(
                    embedding,
                    candidate_k
                )
            )

            for score, index in zip(
                scores[0],
                indices[0]
            ):

                if index < 0:
                    continue

                if index >= len(memories):
                    continue

                semantic_scores[index] = float(
                    score
                )

        # -----------------------------------------------------
        # QUERY CATEGORY
        # -----------------------------------------------------

        query_category = (
            self.infer_query_category(query)
        )

        # -----------------------------------------------------
        # RERANK ALL RELEVANT CANDIDATES
        # -----------------------------------------------------

        candidates = []

        for index, memory in enumerate(
            memories
        ):

            text = memory.get(
                "text",
                ""
            ).strip()

            if not text:
                continue

            # Don't return an exact copy of the query.
            if text.lower() == query.lower():
                continue

            semantic_score = (
                semantic_scores.get(
                    index,
                    0.0
                )
            )

            memory_category = memory.get(
                "intent",
                "general"
            )

            # Category match
            category_score = 0.0

            if (
                query_category
                and memory_category
                == query_category
            ):
                category_score = 1.0

            # Keyword overlap
            keyword_score = self.keyword_score(
                query,
                text
            )

            # -------------------------------------------------
            # HYBRID SCORE
            # -------------------------------------------------

            combined_score = (
            (semantic_score * 0.50)
            + (category_score * 0.40)
            + (keyword_score * 0.10)
        )

            candidates.append({
                "intent": memory_category,
                "text": text,
                "score": float(
                    combined_score
                ),
                "semantic_score": float(
                    semantic_score
                ),
                "category_score": float(
                    category_score
                ),
                "keyword_score": float(
                    keyword_score
                )
            })

        # -----------------------------------------------------
        # SORT
        # -----------------------------------------------------

        candidates.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return candidates[:top_k]

    # =========================================================
    # CLEAR MEMORY
    # =========================================================

    def clear(self):

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.save_index()