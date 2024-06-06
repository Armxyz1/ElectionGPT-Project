from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, PromptTemplate
db=SQLDatabase.from_uri("sqlite:///./eci_kr_2023.db")
import os
os.environ["OPENAI_API_KEY"] =""

template = """
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["human_input"], template=template
)
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, memory = ConversationBufferMemory())
f=open("./test.txt","r")
text=f.readlines()
f.close()
for i in range(len(text)):
    res=db_chain(template.format(human_input=text[i][4:]))
    print(res)
    print("\n")