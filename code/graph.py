from langchain import SQLDatabase, SQLDatabaseChain, PromptTemplate, OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import sqlite3
db=SQLDatabase.from_uri("sqlite:///./UP_AE.db")
import os
# import pandas as pd
os.environ["OPENAI_API_KEY"] =""
llm=ChatOpenAI(model_name="gpt-4",temperature=0,verbose=True)
template1="""
Refer to the table Uttar_Pradesh_AE to answer the given query. 
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




prompt_template = PromptTemplate(input_variables=["query"],template=template1)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)


result=db_chain(prompt_template.format(query="What are the age distributions in intervals of size 10 of all the candidates? Remove candidates with age more than 100 or Empty column."))['result']



llm2=ChatOpenAI(model_name="gpt-4",temperature=0,verbose=True)
temp2="""
Interpret the following statement and output ONLY a Python code using Pandas library to make a suitable plot of the given data:
{query}
"""
prompt_template2 = PromptTemplate(input_variables=["query"],template=temp2)
chain2=LLMChain(llm=llm2,prompt=prompt_template2)
result2=chain2.run(prompt_template2.format(query=result))

while '`' in result2:
    result2=result2.replace('`','')
result2=result2[7:]
f=open("histogram.py","w+")
f.write(result2)
f.flush()
f.close()
with open("histogram.py") as f:
    exec(f.read())