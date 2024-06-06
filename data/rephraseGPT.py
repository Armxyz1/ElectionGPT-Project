from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import os
os.environ["OPENAI_API_KEY"] =""
llm=ChatOpenAI(model_name="gpt-4",temperature=0,verbose=True)

template="""
Write the given query in 10 different ways, with each sentence being unique, but having the same meaning. Don't write serial numbers:
{query}
"""
f=open("UP.csv","r")
g=open("UPextra.csv","w")
f.readline()
x=f.readlines()
prompt_template = PromptTemplate(input_variables=["query"],template=template)
chain=LLMChain(llm=llm,prompt=prompt_template)
bad=["1. ","2. ","3. ","4. ","5. ","6. ","7. ","8. ","9. ","10. ","1.","2.","3.","4.","5.","6.","7.","8.","9.","10."]
c=1
for j in x:
    print(c)
    line=j.split(",")
    ques=line[2]
    print(ques)
    resp=chain.run(prompt_template.format(query=ques))
    g.write(ques)
    g.write("\n")
    list=resp.split("\n")
    for i in list:
        for x in bad:
            i=i.replace(x,"")
        while "," in i:
            i=i.replace(",","")
        if i!="":
            g.write(i)
            g.write("\n")
    g.flush()
    c+=1
f.close()
g.close()

# template="""
# Write the given query in 10 different ways, with each sentence being unique, but having the same meaning. Don't write serial numbers:
# {query}
# """
# x="In which year did the maximum number of women contested in UP elections?"
# res=chain.run(prompt_template.format(query=x)).split("\n")
# for i in res:
#     for j in bad:
#         i=i.replace(j,"")
#     print(i)
