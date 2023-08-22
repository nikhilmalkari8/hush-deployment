import os
import openai
from llama_index import SQLDatabase,ServiceContext
from llama_index.llms import OpenAI
from sqlalchemy import select, create_engine, MetaData, Table,inspect
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from IPython.display import Markdown, display
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType


import nltk
nltk.data.path.append("/Users/nikhilmalkari/Documents/Important Libraries Data")

os.environ['OPENAI_API_KEY'] = "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"
openai.api_key = os.environ.get('OPENAI_API_KEY')

db_user = "personalproject"
db_password = "student" #Enter you password database password here
db_host = "localhost"  
db_name = "hushproject" #name of the database
db_port = "0000" #specify your port here
connection_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(connection_uri)
llm = OpenAI(temperature=0.5, model="gpt-3.5-turbo-16k")
service_context = ServiceContext.from_defaults(llm=llm)
engine = create_engine(connection_uri)
sql_database = SQLDatabase(engine)

inspector = inspect(engine)
table_names = inspector.get_table_names()

response_template = """
## Question

{question}

## Answer
```
{response}
```
## Generated SQL Query
```
{sql}
```
"""

def chat_to_sql(question: str | list[str],tables: list[str] | None = None,synthesize_response: bool = True,):
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=tables,
        synthesize_response=synthesize_response,
        service_context=service_context,
        )
    
    try:
        response = query_engine.query(question)
        response_md = str(response)
        sql = response.metadata["sql_query"]
    except Exception as ex:
        response_md = "Error"
        sql = f"ERROR: {str(ex)}"

   
    display(Markdown(response_template.format(
        question=question,
        response=response_md,
        sql=sql,
    )))

chat_to_sql("What is the profile name",table_names)