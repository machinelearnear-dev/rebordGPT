from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate


def get_generic_prompt_spanish():
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
                        {context}
                        Question: {question}
                        ALWAYS answer in Spanish, in a strong argentinian accent.
                        """
    return PromptTemplate(template=prompt_template, input_variables=["context", "question"])


def get_assistant_prompt_spanish():
    prompt_template = """You are a helpful assistant that accurately answers queries using the following pieces of context: "{context}"
                        Use the context provided to form your answer, but avoid copying word-for-word from the text. Try to use your own words when possible. Keep your answer under 5 sentences.
                        If you don't know the answer, just say that you don't know, don't try to make up an answer.
                        Be accurate, helpful, concise, and clear. Use the given context to provide an answer to the question: "{question}". 
                        ALWAYS answer in Spanish, in a strong argentinian accent.
                        """
    return PromptTemplate(template=prompt_template, input_variables=["context", "question"])


def get_assistant_prompt_spanis_one_shot():
    examples = [{
        "prefix": "You are a helpful assistant that accurately answers queries using the provided context. The context is conversations between two or more people. Every time a person speaks, his or her name will appear in the text followed by colon (:) character and then what this person said. The context can contain different conversations. This is the context:",
        "context": "Nelson G: El agua es asi no? Lisandro M: Asi liquida? Nelson G: Si, liquida y te saca la sed. Nico M: Viste cuando vas al rio, y te queres meter al agua, el agua es algo que te saca el stress. Lisandro M: Depende, yo no se nadar, y el agua no me gusta mucho. Nelson G: Cuando yo voy al agua, me transporto a otro lugar, lo disfruto Nico M: pero no me gusta cuando el agua esta sucia",
        "question": "Use the context provided to form your answer, but avoid copying word-for-word from the text. Try to use your own words when possible. Keep your answer under 5 sentences. If you don't know the answer, just say that you don't know, don't try to make up an answer. Be accurate, helpful, concise, and clear. ALWAYS answer in Spanish and use the given context to provide an answer to the question: Que dijo nelson sobre el el agua?",
        "answer": "Nelson dijo que el agua es algo que lo transporta a otro lugar y que lo disfruta. También mencionó que el agua es líquida y puede saciar la sed."
    }]

    sufix = """
    context: {context} \n
    question: {question}
    """

    example_template = """{prefix}\n{context}\n{question}\n{answer}"""

    example_prompt = PromptTemplate(
        input_variables=["prefix", "context", "question", "answer"],
        template=example_template
    )

    return FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix=sufix,
        input_variables=["context", "question"]
    )
