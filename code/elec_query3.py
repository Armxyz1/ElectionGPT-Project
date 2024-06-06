from sqlalchemy import create_engine
from llama_index import SQLDatabase, query_engine
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
# from langchain.chat_models import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] =""
engine = create_engine("sqlite:///./eci_kr_2023.db")
sql_database = SQLDatabase(engine,include_tables=["eci_kr_2023"])
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["eci_kr_2023"]
)
query_str = (
    "How many candidates were fielded by JD(s) in the 2023 assembly elections?"
)
response = query_engine.query(query_str)