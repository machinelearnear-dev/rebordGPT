"""
Semantic cache class using Chroma. It implements langchain BaseCache interface.
The prompt must have the query between <query> </query> tags
We only need to cache the query, not the whole prompt with the chunks.
"""
from __future__ import annotations
from langchain.vectorstores import Chroma
from langchain.cache import BaseCache

from typing import (
    Optional,
    Sequence,
    Dict
)

import re

from langchain.schema import Generation

from langchain.embeddings.base import Embeddings
import hashlib

RETURN_VAL_TYPE = Sequence[Generation]

def _hash(_input: str) -> str:
    """Use a deterministic hashing approach."""
    return hashlib.md5(_input.encode()).hexdigest()

class ChromaSemanticCache(BaseCache):
    """Cache that uses Chroma as a vector-store backend."""

    def __init__(self, embedding: Embeddings, score_threshold: float = 0.2, persist_directory="cache_chroma"):
        """Initialize

        Args:
            embedding (Embedding): Embedding provider for semantic encoding and search.
            score_threshold (float, 0.2):
        """
        self.embedding = embedding
        self.persist_directory = persist_directory
        self.score_threshold = score_threshold
        self._cache_dict: Dict[str, Chroma] = {}

    def _index_name(self, llm_string: str) -> str:
        hashed_index = _hash(llm_string)
        return f"cache_{hashed_index}"
    
    def _get_llm_cache(self, llm_string: str) -> Chroma:
        index_name = self._index_name(llm_string)

        # return vectorstore client for the specific llm string
        if index_name in self._cache_dict:
            return self._cache_dict[index_name]

        # create new vectorstore client for the specific llm string
        try:
            self._cache_dict[index_name] = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding, collection_name=index_name)
        except Exception as e:
            print("ERROR", e)
           
        return self._cache_dict[index_name]

    def clear(self, **kwargs: Any) -> None:
        """Clear semantic cache for a given llm_string."""
        index_name = self._index_name(kwargs["llm_string"])
        if index_name in self._cache_dict:
            self._cache_dict[index_name].delete_collection()

    def extract_query_from_prompt(self, prompt:str) -> str:
        reg_str = "<query>(.*?)</query>"
        if(len(re.findall(reg_str, prompt)) == 0):
            return ""
        return str(re.findall(reg_str, prompt)[0])
        

    def lookup(self, prompt: str, llm_string: str) -> Optional[RETURN_VAL_TYPE]:
        """Look up based on prompt"""
        llm_cache = self._get_llm_cache(llm_string)
        generations = []
        filtered_prompt = self.extract_query_from_prompt(prompt)
        print("Searching chroma cache for ", filtered_prompt)
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
                generations.append(Generation(text=document.metadata["return_val"]))
        return generations if generations else None

    def update(self, prompt: str, llm_string: str, return_val: RETURN_VAL_TYPE) -> None:
        """Update cache based on prompt"""
        filtered_prompt = self.extract_query_from_prompt(prompt)
        metadata = {
            "llm_string": llm_string,
            "prompt": filtered_prompt,
            "return_val": return_val[0].text,
        }
        llm_cache = self._get_llm_cache(llm_string)
        llm_cache.add_texts(texts=[filtered_prompt], metadatas=[metadata])