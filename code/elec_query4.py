import os
import deepspeed
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain

base_model = LlamaForCausalLM.from_pretrained(
    "chavinlo/alpaca-native",
    load_in_8bit=True,
    device_map='auto',
)

tokenizer = LlamaTokenizer.from_pretrained("chavinlo/alpaca-native")
pipe = pipeline(
    "text-generation",
    model=base_model,
    tokenizer=tokenizer,
    max_length=500,
    temperature=0.3,
    top_p=0.95,
    repetition_penalty=1.2
)
template = """
Write a SQL Query given the table name {Table} and columns as a list {Columns} for the given question : 
{question}.
"""


prompt = PromptTemplate(template=template, input_variables=["Table","question","Columns"])

local_llm = HuggingFacePipeline(pipeline=pipe)
llm_chain = LLMChain(prompt=prompt, llm=local_llm)



def get_llm_response(tble,question,cols):
    llm_chain = LLMChain(prompt=prompt, 
                         llm=local_llm
                         )
    response= llm_chain.run({"Table" : tble,"question" :question, "Columns" : cols})
    print(response)
tble = "eci_kr_2023"
cols = ["ac_no","ac_name_x","regions","caste","locality","district","s_no","candidate_name","party,evm_votes","postal_votes","votes","vote_share","st_name","st_no","ac_name_y","constituency_code","position","total_votes","margin","margin_percent","vote_share_percent","margin_buckets_percent","margin_buckets_votes"]
question = "How many candidates were fielded by JD(s) in the 2023 assembly elections?"
get_llm_response(tble,question,cols)
