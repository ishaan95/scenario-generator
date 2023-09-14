import json

with open('Crashes.json') as file:
    data = json.load(file)

count = 1
keys = data.keys()
for key in keys:
    if count == 20: scenario = data[key]
    count+=1  
    
# answers = {}
# if scenario["INTERSECTION"]=="Y": answers["in_intersection"] = True
# elif scenario["INTERSECTION"]=="N": answers["in_intersection"] = False


