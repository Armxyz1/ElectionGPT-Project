from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
db=SQLDatabase.from_uri("sqlite:///./eci_kr_2023.db")
import os
os.environ["OPENAI_API_KEY"] =""
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))
template="""
Refer to the table eci_kr_2023 to answer the given query. 
eci_kr_2023 has columns ac_no,ac_name_x,regions,caste,locality,district,s_no,candidate_name,party,evm_votes,postal_votes,votes,vote_share,st_name,st_no,ac_name_y,constituency_code,position,total_votes,margin,margin_percent,vote_share_percent,margin_buckets_percent,margin_buckets_votes.
Winning or victory means position=1.
Victory margin means check position=1 and then check margin.
JD(s) or JD(S) means party=Janata Dal (Secular).
When asked for minimum or maximum respond with all possible choices that have the minimum or maximum value.
Voter Turnout is calculated by dividing the number of votes by the number of voters.
Use margin if query asks to use margin. 
Use votes if query asks to use votes.
Largest means maximum.
Smallest means minimum.
Largest number of candidates means count(candidate_name) as num_candidates group by ac_name_y order by num_candidates.
Less than x votes means votes<x.
Victory margin over x means margin>x and position=1.
Ruling party means party=BJP.

User: {query}
AI:"""
prompt_template = PromptTemplate(input_variables=["query"],template=template)
agent_executor = create_sql_agent(
    llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    template=prompt_template
)
agent_executor.run(prompt_template.format(query="How many candidates were fielded by JD(s) in the 2023 assembly elections?")) 