import guidance
import sys
import re
import pandas as pd

# Replace 'your_file.csv' with your actual CSV file path
df = pd.read_csv('2022-Autonomous-Vehicle-Disengagement-Reports-CSV.csv', encoding='unicode_escape')

description = df['DESCRIPTION OF FACTS CAUSING DISENGAGEMENT'].to_list()
description_lim = description[0:3]

# connect to a chat model like GPT-4 or Vicuna
gpt = guidance.llms.OpenAI("gpt-4")
experts = guidance('''
{{#system~}}
You are a world-class scenario designer for testing autonomous vehicles. This involves detailed study of disengagement reports of autonomous vehicles, specifically the description of facts.
Taking a list of descriptions of facts about the disengagement of autonomous vehicles, you will design scenarios for testing autonomous vehicles grounded in the descriptions.
Suggest 3 such scenarios. Also rewrite the description that is closest to this scenario. 
{{~/system}}

{{#user~}}

{{query}}

{{~/user}}

{{#assistant~}}
{{gen 'json' temperature=0.7 max_tokens=500}}
{{~/assistant}}
''', llm=gpt)
out = experts(query=description)
print(description_lim)
print(out['json'])
