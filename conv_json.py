import json
prompts = [
"How many MLA won with more than one lakh votes?"
]
completions = [
    "SELECT COUNT(*) FROM eci_kr_2023 WHERE votes > 100000 AND position=1"
]
data=[{"prompt":p, "completion":c} for p,c in zip(prompts,completions)]
with open("test.json","w") as f:
    json.dump(data,f,indent=4)
