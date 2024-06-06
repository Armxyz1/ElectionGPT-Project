import pandas as pd
import numpy as np
data = pd.read_csv("test.csv", header=None)
print(data)

data['natural query'] = data['natural query'].str.strip()
data['sql query'] = data['sql query'].str.strip()
data['natural query'] = data['natural query'] + "\n\n###\n\n"
data['sql query'] = " " + data['sql query'] + " STOP"
data.to_json("p_and_c.jsonl",orient='records',lines=True)
import os
os.environ['OPENAI_API_KEY'] = ''
prompt="How many MLA won with more than one lakh votes?"
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
   model="model name",
   prompt=prompt,
   temperature=0.7,
   max_tokens=256,
   top_p=1,
   frequency_penalty=0,
   presence_penalty=0,
   stop= [" STOP"]
 )
print(response['choices'][0]['text'])