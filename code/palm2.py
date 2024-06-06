import pprint
import google.generativeai as palm
palm.configure(api_key='')
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
prompt = """
Write the given query in 10 different ways, with each sentence being unique, but having the same meaning. Don't write serial numbers:
{query}"""

f=open("UP.csv","r")
g=open("UPextra2.csv","w")
f.readline()
x=f.readlines()
bad=["1. ","2. ","3. ","4. ","5. ","6. ","7. ","8. ","9. ","10. ","1.","2.","3.","4.","5.","6.","7.","8.","9.","10."]
c=1
for j in x:
    print(c)
    line=j.split(",")
    ques=line[2]
    print(ques)
    completion = palm.generate_text(
    model=model,
    prompt=prompt.format(query="Who served UP assembly for the longest time?"),
    temperature=0)
    resp=completion.result
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
