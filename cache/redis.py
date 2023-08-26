"""
Extending langchain class RedisSemanticCache to support Question and Answering retrieval.
This class overrides `lookup` and `update` methods, to extract que query from the prompt.
The prompt must have the query between <query> </query> tags
We only need to cache the query, not the whole prompt with the chunks.
"""
from __future__ import annotations

import warnings
from typing import (
    Optional,
    Sequence,
)

import re

from langchain.schema import ChatGeneration, Generation

from langchain.cache import RedisSemanticCache

RETURN_VAL_TYPE = Sequence[Generation]


class RedisSemanticCacheOnlyPrompt(RedisSemanticCache):
    def lookup(self, prompt: str, llm_string: str) -> Optional[RETURN_VAL_TYPE]:
        """Look up based on prompt and llm_string."""
        llm_cache = self._get_llm_cache(llm_string)
        generations = []
        filtered_prompt = self.extract_query_from_prompt(prompt)
        # Read from a Hash
        results = llm_cache.similarity_search_limit_score(
            query=filtered_prompt,
            k=1,
            score_threshold=self.score_threshold,
        )
        if results:
            print("Cache hit")
            for document in results:
                for text in document.metadata["return_val"]:
                    generations.append(Generation(text=text))
        return generations if generations else None

    def update(self, prompt: str, llm_string: str, return_val: RETURN_VAL_TYPE) -> None:
        """Update cache based on prompt and llm_string."""
        for gen in return_val:
            if not isinstance(gen, Generation):
                raise ValueError(
                    "RedisSemanticCache only supports caching of "
                    f"normal LLM generations, got {type(gen)}"
                )
            if isinstance(gen, ChatGeneration):
                warnings.warn(
                    "NOTE: Generation has not been cached. RedisSentimentCache does not"
                    " support caching ChatModel outputs."
                )
                return
        llm_cache = self._get_llm_cache(llm_string)
        # Write to vectorstore
        filtered_prompt = self.extract_query_from_prompt(prompt)
        metadata = {
            "llm_string": llm_string,
            "prompt": filtered_prompt,
            "return_val": [generation.text for generation in return_val],
        }
        llm_cache.add_texts(texts=[filtered_prompt], metadatas=[metadata])

    def extract_query_from_prompt(self, prompt:str):
        reg_str = "<query>(.*?)</query>"
        # TODO - make sure the line below doesn't throw an exception
        return str(re.findall(reg_str, prompt)[0])