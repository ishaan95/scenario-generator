import guidance
import sys
import re
import json

# connect to a chat model like GPT-4 or Vicuna
with open('Crashes.json') as file:
    data = json.load(file)

scenario_list = []
count = 1
for key in data.keys():
    if count==23 or 24: 
        scenario = data[key]
        scenario_list.append(scenario)
    count+=1

gpt = guidance.llms.OpenAI("gpt-4")
experts = guidance('''
{{#system~}}
You are a concrete scenario to natural language scenario interface with knowledge of the different kinds of scenarios for testing autonomous vehicles.
A scenario typically contains static elements such as the ones specified in the ASAM OpenDRIVE format and dynamic elements
such as the ones specified in the ASAM OpenSCENARIO format. Many such scenarios occur at intersections. 
A T intersection typically contains three legs with two of them separated by 90 degrees. A Y intersection typically contains three legs with 
two legs separated by 60 degrees and the remaining angles between legs being 150 degree each. If an intersection scenario is under discussion,
typically vehicles are spawned on these legs and drive towards the intersection junction. Every intersection leg is a road with its own unique ID
and typically containing a lane with traffic going towards a road intersection junction (identified with a negative integer ID) and a lane with 
traffic going away from the intersection junction (identified with a positive integer ID).

The concrete scenario is presented as a json dictionary. Some of the key values are explained below - 
"PCF_VIOL_CATEGORY" which indicates the cause of the crash
"00 - Unknown"
"01 - Driving or Bicycling Under the Influence of Alcohol or Drug"
"03 - Unsafe Speed"
"04 - Following Too Closely"
"05 - Wrong Side of Road"
"06 - Improper Passing"
"07 - Unsafe Lane Change"
"08 - Improper Turning"
"09 - Automobile Right of Way"
"10 - Pedestrian Right of Way"
"11 - Pedestrian Violation"
"12 - Traffic Signals and Signs"
"14 - Lights"
"17 - Other Hazardous Violation"
"18 - Other Than Driver (or Pedestrian)"
"21 - Unsafe Starting or Backing"
"22 - Other Improper Driving"

Here's the type of collision information (which indicates how the crash happened) -- A - Head-On
B - Sideswipe
C - Rear End
D - Broadside
E - Hit Object
F - Overturned
G - Vehicle/Pedestrian
H - Other

Here are the values for LIGHTING -- 
A - Daylight
B - Dusk - Dawn
C - Dark - Street Lights
D - Dark - No Street Lights
E - Dark - Street Lights Not functioning

Here is the PED_ACTION possible values - A - No Pedestrian Involved
B - Crossing in Crosswalk at
Intersection
C - Crossing in Crosswalk Not at
Intersection
D - Crossing Not in Crosswalk
E - In Road, Including Shoulder
F - Not in Road
G - Approaching/Leaving School Bus

Here are the values for MVIW (which indicates what the vehicle crashed with) - A - Non-Collision
B - Pedestrian
C - Other Motor Vehicle
D - Motor Vehicle on Other Roadway
E - Parked Motor Vehicle
F - Train
G - Bicycle
H - Animal
I - Fixed Object
J - Other Object

Here are the values for WEATHER_1 - 
A - Clear
B - Cloudy
C - Raining
D - Snowing
E - Fog
F - Other
G - Windy

Here are the values for ROAD_COND_1 - 
A - Holes, Deep Ruts
B - Loose Material on Roadway
C - Obstruction on Roadway
D - Construction or Repair Zone
E - Reduced Roadway Width
F - Flooded
G - Other
H - No Unusual Condition
                   
Here are the values for "LOCATION_TYPE" indicating the site of the accident - 
H - Highway
I - Intersection
R - Ramp (or Collector)
- or blank - Not State Highway
                   
Here are the possible values and meaning for the attribute "TYPE_OF_COLLISION" indicating how the crash happened - 
A - Head-On
B - Sideswipe
C - Rear End
D - Broadside
E - Hit Object
F - Overturned
G - Vehicle/Pedestrian
H - Other

{{~/system}}

{{#user~}}
You are a road safety scientist at a vehicle company with a background in traffic engineering, civil engineering and autonomous vehicles. 
Generate a short lecture explaining concepts in this query below.

{{query}}
                   
{{~/user}}                   
                   
{{#assistant~}}
{{gen 'lecture' temperature=0.7 max_tokens=500}}
{{~/assistant}}

{{#user~}}                   
Now using this lecture, explain logically step by step as a sequence of events why this accident happened. 
In your explanation include the lighting conditions, geometry of the road, the traffic controls, relevant road rules, 
the possible speeds of the vehicles, the possible driver behaviors, effect on other vehicles that would logically happen. 
Write each step as a bullet point. Each bullet point should be logically connected to the next one (cause and effect chain) and each bullet point should have just two sentences.
Each bullet point should also mention the part of the query that it corresponds to. 
{{~/user}}

{{#assistant~}}
{{gen 'explanation' temperature=0.4 max_tokens=500}}
{{~/assistant}}
                

{{#user~}}                   
Carefully answer the following questions about just one vehicle in this explanation. Answer based on the explanation to the best of your abilities. 
If no explicit answer is provided for the questions, reason step by step with your explanation before and infer an answer.
While writing your answer, repeat the question so that it's clear:
1. Is the vehicle at an intersection? Check the "INTERSECTION" attribute and reason step by step and conclude with yes or no.
2. What was the road condition?
3. Was the vehicle moving fast or slow? Write down an approximation of the speed in m/s.
4. What were the lighting conditions like?
5. What was the weather like?
6. What is the cause of the vehicle crash? Use the value for the attribute "PCF_VIOL_CATEGORY" and reason step by step.
7. How did the crash happen? Use the value for the attribute "TYPE_OF_COLLISION" and reason step by step.   
8. What does the vehicle crash with?
9. If the vehicle crashed with a pedestrian, what was the pedestrian doing? Use the value for the attribute "PED_ACTION" and reason step by step.                    
10. Write a one sentence summary of the event taking into account all these answers.
11. Use the "COLLISION_TIME" (24 hour time notation) and "DAY_OF_WEEK" (1 indicating Monday, 2 indicating Tuesday and so on) attributes and describe the traffic on the road. Weekdays and 9am to 7pm hours indicate heavy traffic.
Other times indicate light traffic.                    
{{~/user}}

{{#assistant~}}
{{gen 'question-answer' temperature=0.8 max_tokens=600}}
{{~/assistant}}

{{#user~}}
Write your answers in the form of a json dictionary. The format of the dictionary should be:
{
    "at-intersection": <answer True or False based on the yes or no>
    "road_condition": <enter a string corresponding with the answer and exactly the code as shown in the data>
    "lighting": <enter a string corresponding with the answer and exactly the code as shown in the data>
    "weather": <enter a string corresponding with the answer and exactly the code as shown in the data>
    "speed": <enter a string corresponding with the answer and exactly the code as shown in the data>
    "cause of the crash": <enter a string corresponding with the answer and exactly the code as shown in the data>
    "crash-with": <enter a string corresponding with the answer and exactly the code as shown in the data>   
}
Here, only respond with this dictionary, nothing else, nothing else. 
{{~/user}}

{{#assistant~}}
{{gen 'json-dictionary' temperature=0.8 max_tokens=500}}
{{~/assistant}}
                            
''', llm=gpt)
out2 = experts(query=scenario)
out3 = experts(query=scenario_list[1])
#print(out2['explanation'])
#print(out2['question-answer'])
#print(out2['json-dictionary'])

scenario_dictionary = json.loads(out2['json-dictionary'])

total_points = 6
score = 0
grade = 0.0

# if scenario_dictionary['at-intersection']==False and scenario["INTERSECTION"]=='N': score+=1
# elif scenario_dictionary['at-intersection']==True and scenario["INTERSECTION"]=='Y': score+=1

# if scenario_dictionary["road_condition"]==scenario["ROAD_COND_1"]: score+=1 
# else: print("road_condition was incorrect")

# if scenario_dictionary["lighting"]==scenario["LIGHTING"]: score+=1
# else: print("lighting was incorrect")

# if scenario_dictionary["weather"]==scenario["WEATHER_1"]: score+=1
# else: print("weather was incorrect")

# if scenario_dictionary["crash-with"]==scenario["MVIW"]: score+=1
# else: print("crash with was incorrect")

# if scenario_dictionary["cause of the crash"]==scenario["PCF_VIOL_CATEGORY"]: score+=1
# else: print("cause of crash was incorrect")

# print("Score is {}".format(score))

# grade = (score/total_points)*100.0
# print('final grade is {}%'.format(grade))

mixer = guidance('''
{{#system~}}
You are a concrete scenario to natural language scenario interface with knowledge of the different kinds of scenarios for testing autonomous vehicles.
A scenario typically contains static elements such as the ones specified in the ASAM OpenDRIVE format and dynamic elements
such as the ones specified in the ASAM OpenSCENARIO format. Many such scenarios occur at intersections. 
A T intersection typically contains three legs with two of them separated by 90 degrees. A Y intersection typically contains three legs with 
two legs separated by 60 degrees and the remaining angles between legs being 150 degree each. If an intersection scenario is under discussion,
typically vehicles are spawned on these legs and drive towards the intersection junction. Every intersection leg is a road with its own unique ID
and typically containing a lane with traffic going towards a road intersection junction (identified with a negative integer ID) and a lane with 
traffic going away from the intersection junction (identified with a positive integer ID).

{{~/system}}

{{#user~}}
You are a road safety scientist at a vehicle company with a background in traffic engineering, civil engineering and autonomous vehicles. 
Here two answers for questions regarding two scenarios are provided in a concatenated manner. Rewrite the summary of the two scenarios. Then carry out the multi-point crossover operation similar to the one in evolutionary algorithms and create two new scenarios. Clearly state how the crossover operation was carried out. 
Write which elements were used for each of the scenarios. Answer the same questions again for this new scenario.

{{query}}
                   
{{~/user}}                   
                   
{{#assistant~}}
{{gen 'mixer' temperature=0.7 max_tokens=500}}
{{~/assistant}}
                            
''', llm=gpt)

print("Scenario 1 answers......")
print(out2['question-answer'])
print("Scenario 2 answers......")
print(out3['question-answer'])

mixed_output = mixer(query=out2['question-answer']+out3['question-answer'])
print("mixer output is......")
print(mixed_output['mixer'])


#11. Now change the answers to some of the questions above. Ensure that the new attributes indicate an absurd, unusual event. Write which answer was changed and what the value was changed to. Write a summary for this event.