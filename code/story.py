from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import os
os.environ["OPENAI_API_KEY"] =""
llm=ChatOpenAI(model_name="gpt-4",temperature=0,verbose=True)

template="""
Generate 50 election data related questions about the following paragraph:
{query}
"""
f=open("file.txt","r",encoding="utf-8")
g=open("write.txt","a",encoding="utf-8")
x=f.read()
prompt_template = PromptTemplate(input_variables=["query"],template=template)
chain=LLMChain(llm=llm,prompt=prompt_template)
response=chain.run(query=x)
g.write(response)
f.close()
g.flush()
g.close()