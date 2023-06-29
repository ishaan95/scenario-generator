import guidance
import sys
import re

# connect to a chat model like GPT-4 or Vicuna
gpt = guidance.llms.OpenAI("gpt-3.5-turbo")
experts = guidance('''
{{#system~}}
You are a natural language to concrete scenario interface with knowledge of the different kinds of scenarios for testing autonomous vehicles.
A scenario typically contains static elements such as the ones specified in the ASAM OpenDRIVE format and dynamic elements
such as the ones specified in the ASAM OpenSCENARIO format. Many such scenarios occur at intersections. 
A T intersection typically contains three legs with two of them separated by 90 degrees. A Y intersection typically contains three legs with 
two legs separated by 60 degrees and the remaining angles between legs being 150 degree each. If an intersection scenario is under discussion,
typically vehicles are spawned on these legs and drive towards the intersection junction. Every intersection leg is a road with its own unique ID
and typically containing a lane with traffic going towards a road intersection junction (identified with a negative integer ID) and a lane with 
traffic going away from the intersection junction (identified with a positive integer ID). An example of a correct interaction would be:
Prompt: "An three car accident at a 4 way intersection. The road IDs are 9, 17, 10, 18."
Response:
{"vehicle_id": 1, "spawn_road_id": 9, "spawn_lane_id": -1, "target_road_id": 18, "target_lane_id": 1},
{"vehicle_id": 2, "spawn_road_id": 17, "spawn_lane_id": -1, "target_road_id": 10, "target_lane_id": 1},
{"vehicle_id": 3, "spawn_road_id": 10, "spawn_lane_id": -1, "target_road_id": 9, "target_lane_id": 1}

Prompt: "A 2 car accident at a T intersection. The road IDs are 9, 17, 10. Roads 9 and 17 have 4 lanes each, two in each direction."
{"vehicle_id": 1, "spawn_road_id": 9, "spawn_road_length": 200, "spawn_lane_id": -2, "target_road_id": 17, "target_road_length": 50, "target_lane_id": 2},
{"vehicle_id": 2, "spawn_road_id": 17, "spawn_road_length": 100, "spawn_lane_id": -2, "target_road_id": 10, "target_road_length": 60, "target_lane_id": 1}

Prompt: "A bicycle collides with a sloth at a Y intersection. The road IDs are 9, 17, 10. Roads 9 and 10 have 4 lanes each."
{"vehicle_id": 1, "spawn_road_id": 9, "spawn_road_length": 100, "spawn_lane_id": -2, "target_road_id": 10, "target_road_length": 200, "target_lane_id": 2},
{"vehicle_id": 2, "spawn_road_id": 17, "spawn_road_length": 150, "spawn_lane_id": -1, "target_road_id": 17, "target_road_length": 100, "target_lane_id": 1}
{{~/system}}

{{#user~}}
Respond to a natural language description by the user in the exact format as described below.

{{query}}

Generate a json dictionary of the following format for one vehicle: 
{"vehicle_id": <a whole number representing a unique identifier for a vehicle in the scenario>
"spawn_road_id": <an integer value representing road number>,
"spawn_road_length": <a positive integer value representing the length of the road in meters.>, 
"spawn_lane_id": <an integer value representing a lane id where the vehicle begins its journey. This lane id belongs to the aforementioned road id.
Generally a vehicle starts its journey going towards an intersection junction.>,
"target_road_id": <an integer value representing road number. Cannot be the same as spawn_road_id. Cannot be the same as spawn_road_id>,
"target_road_length": <a positive integer value representing the length of the road in meters.>
"target_lane_id": <an integer value representing a lane id where the vehicle ends its journey. This lane id belongs to the target road. 
Generally a vehicle ends its journey going away from an intersection junction.>}

One python dictionary for each vehicle in the scenario separated by a comma, 
nothing else. No additional comments, nothing else.

{{~/user}}

{{#assistant~}}
{{gen 'json' n=number_of_scenarios temperature=0.7 max_tokens=500}}
{{~/assistant}}
''', llm=gpt)
out = experts(query=sys.argv[1], number_of_scenarios=int(sys.argv[2]))
print(out["json"])