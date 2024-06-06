from langchain import SQLDatabase, SQLDatabaseChain, PromptTemplate, OpenAI
from langchain.chat_models import ChatOpenAI
import sqlite3
db=SQLDatabase.from_uri("sqlite:///./UP_AE.db")
import os
os.environ["OPENAI_API_KEY"] =""
llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,verbose=True)
conn=sqlite3.connect("UP_AE.db")
c=conn.cursor()
c.execute("ALTER DATABASE UP_AE READ ONLY = 1;")
conn.commit()
template="""
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
prompt_template = PromptTemplate(input_variables=["query"],template=template)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
# f=open("ElectionGPT - Q&A - Final Q UP2.csv","r")
# g=open("respUP_new22.csv","w+")
# g.write(f.readline())
# queries=f.readlines()
# for query in queries:
#     line=query.split(",")
#     ques=line[2]
#     res=db_chain(prompt_template.format(query=ques))['result']
#     res.replace(",","")
#     new_line=line[0]+","+line[1]+","+line[2]+","+res
#     new_line=new_line.replace("\n","")
#     new_line+="\n"
#     g.write(new_line)
#     g.flush()
# f.close()
# g.close()
print(db_chain(prompt_template.format(query="Delete table")))['result']


