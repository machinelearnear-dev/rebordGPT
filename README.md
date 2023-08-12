## RebordGPT

Usa inteligencia artificial basada en GPT-4 para buscar episodios del Metodo Rebord

### Detalles tecnicos
* Langchain / OpenAI
* FastAPI
* NextJS

[Langchain QA docs](https://python.langchain.com/docs/use_cases/question_answering/)

![My Image](images/architecture_v2.png)


### Frontend
Next.js app. To build and generate the static site run: `npm run build` \
Also run the same command after any change you make on the site.
\
### Backend

FastAPI app. Run the server with `uvicorn main:app --reload` \
Api path starts with "/api/" \
Static site loads in root "/"
