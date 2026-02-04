import os
import uvicorn  # For start server
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# LangChain and AI
# 1. main chain (RetrievalQA )
from langchain_classic.chains import RetrievalQA
# 2. PromptTemplate
from langchain_classic.prompts import PromptTemplate


# 3. Other components
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

#Create the server for query
app = FastAPI(title="Medbot_Server")

#load values from .env
load_dotenv()
#Handling Error
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("ERROR: Not find GOOGLE_API_KEY of the .env")

#Create LLM
llm_for_bot= ChatGoogleGenerativeAI(model="gemini-flash-latest",temperature=0)


db_path = "embeddings_med"
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Error: Directory '{db_path}' not found!")


# Create embeddings model
embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base"
                                   ,model_kwargs={"device":"cpu"})

#get collection with vectors
vectorstore = Chroma(persist_directory=db_path,
                     embedding_function=embeddings,
                     collection_name="meds_protocols")


template = """ Ти - військовий медик-інструктор.
                Використовуй цей контекст: {context}
                Питання :{question}
                Дай коротку, чітку відповідь (алгоритм дій):
                """
#form prompt
prompt = PromptTemplate(template=template,input_variables=["context","question"])


qa_chain = RetrievalQA.from_chain_type(llm=llm_for_bot,chain_type="stuff",
                                       retriever=vectorstore.as_retriever(search_kwargs={"k":3}),
                                       chain_type_kwargs={"prompt":prompt})
#Data model for request validation
class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
def ask (request: QueryRequest):
    try:
        # Prepend 'query:' for e5-base model optimization
        cleaned_query = f"query: {request.query}"

        # Invoke the chain
        response = qa_chain.invoke(cleaned_query)
        return {"answer": response["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
