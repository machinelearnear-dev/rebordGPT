"""
Extending langchain class RedisSemanticCache to support Question and Answering retrieval.
This class overrides `lookup` and `update` methods, extracting the query from the prompt.
The prompt must have the query between <query> </query> tags
We only need to cache the query, not the whole prompt with the chunks.
"""
from __future__ import annotations
from langchain.vectorstores import Chroma
from langchain.cache import BaseCache

from typing import (
    Optional,
    Sequence,
)

import re

from langchain.schema import Generation

from langchain.embeddings.base import Embeddings

RETURN_VAL_TYPE = Sequence[Generation]

class ChromaSemanticCache(BaseCache):
    """Cache that uses Redis as a vector-store backend."""

    def __init__(self, embedding: Embeddings, score_threshold: float = 0.2):
        """Initialize by passing in the `init` GPTCache func

        Args:
            redis_url (str): URL to connect to Redis.
            embedding (Embedding): Embedding provider for semantic encoding and search.
            score_threshold (float, 0.2):

        Example:

        .. code-block:: python

            import langchain

            from langchain.cache import RedisSemanticCache
            from langchain.embeddings import OpenAIEmbeddings

            langchain.llm_cache = RedisSemanticCache(
                redis_url="redis://localhost:6379",
                embedding=OpenAIEmbeddings()
            )

        """
        self.embedding = embedding
        self.score_threshold = score_threshold

    def clear(self, **kwargs: Any) -> None:
        """Clear semantic cache for a given llm_string."""
        a = ""
        # index_name = self._index_name(kwargs["llm_string"])
        # if index_name in self._cache_dict:
        #     self._cache_dict[index_name].drop_index(
        #         index_name=index_name, delete_documents=True, redis_url=self.redis_url
        #     )
        #     del self._cache_dict[index_name]

    def extract_query_from_prompt(self, prompt:str):
        reg_str = "<query>(.*?)</query>"
        # TODO - make sure the line below doesn't throw an exception
        return str(re.findall(reg_str, prompt)[0])

    def lookup(self, prompt: str, llm_string: str) -> Optional[RETURN_VAL_TYPE]:
        """Look up based on prompt and llm_string."""
        llm_cache = Chroma(persist_directory="cache_chroma", embedding_function=self.embedding)
        generations = []
        filtered_prompt = self.extract_query_from_prompt(prompt)
        print("Searching chroma cache for ", filtered_prompt)
        # Read from a Hash
        results = llm_cache.similarity_search_with_score(
            query=filtered_prompt,
            k=1
        )
        print("Results found in Chroma cache ", results)
        filtered_results = [
            r for r in results if r[1] <= self.score_threshold]
        
        if filtered_results:
            print("CACHE HIT")
            docs = list(map(lambda result: result[0], filtered_results))
            for document in docs:
                # print("NELSOOOOON", document)
                # for text in document.metadata["return_val"]:
                generations.append(Generation(text=document.metadata["return_val"]))
        return generations if generations else None

    def update(self, prompt: str, llm_string: str, return_val: RETURN_VAL_TYPE) -> None:
        """Update cache based on prompt and llm_string."""
        filtered_prompt = self.extract_query_from_prompt(prompt)
        print(return_val)
        metadata = {
            "llm_string": llm_string,
            "prompt": filtered_prompt,
            "return_val": return_val[0].text,
        }
        Chroma.from_texts([filtered_prompt], self.embedding, metadatas=[metadata], persist_directory="cache_chroma")