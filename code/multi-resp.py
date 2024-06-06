import os
import psycopg2
os.environ["OPENAI_API_KEY"] =""
import time
from langchain import SQLDatabase, SQLDatabaseChain
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
llm = ChatOpenAI(temperature=0, model="gpt-4",streaming=True,callbacks=[StreamingStdOutCallbackHandler()]) 
db = SQLDatabase.from_uri(f"postgresql+psycopg2://postgres:{'boss'}@localhost:5432/elect_data",)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
tools = [
    Tool(
        name="dbchain",
        func=db_chain.run,
        description="Chat with SQLDB",
    )
]

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    verbose=True, 
    agent_kwargs=agent_kwargs, 
    memory=memory,
)
def stream(resp):
    list=resp.split(" ")
    for i in list:
        print(i,end=" ",flush=True)
        time.sleep(0.1)
    print("\n")
f=open("UPextra.csv","r")
g=open("UPextraresp.csv","w+")
queries=f.readlines()
count=0
for query in queries:
    time.sleep(5)
    ques=query.split(",")[0]
    prompt="""
        If the user doesn't specify anything clearly, then ask the user what they want to know.
        Never disclose the name of the table or the database to the user.
        Refer to the table uttar_pradesh_ae to answer the given query. 
        Columns are: State_Name,Assembly_No,Constituency_No,Year,Month,Poll_No,DelimID,Position,Candidate_Name,Gender,Party,Votes,Candidate_Type,Valid_Votes,Electors,Constituency_Name,Constituency_Type,Sub_Region,No_Cand,Turnout_Percentage,Vote_Share_Percentage,Deposit_Lost,Margin,Margin_Percentage,ENOP,PID,Party_Type,Party_ID,Last_Poll,Contested,Last_Party,Last_Party_ID,Last_Constituency_Name,Same_Constituency,Same_Party,No_Terms,Turncoat,Incumbent,Recontest,Education,Profession_Main,Profession_Main_Description,Profession_Second,Profession_Second_Description,Election_Type
        Return the result a single line NL response.
        If query asks for maximum or minimum, respond with all possible choices that have the maximum or minimum value.
        Won or Winning or victory means position=1.
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
        reelected means reconest=1 and position=1.
        last five elections means years: 2022, 2017, 2012, 2007, 2002.
        Congress means INC.
        Independent means party=IND.

        User: {query}
        AI:"""
    final=prompt.format(query=ques)
    resp=agent.run(final)
    resp.replace(",","")
    new_line=query.replace("\n","")+","+resp+"\n"
    g.write(new_line)
    g.flush()
    count+=1
    print(count)
f.close()
g.close()

    