"""
  scenariogeneration
  https://github.com/pyoscx/scenariogeneration
 
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.
 
  Copyright (c) 2022 The scenariogeneration Authors.

    example of creating OpenSCENARIO and OpenDRIVE file, with the parameters defined outside the class structure

    Example usage: when a iterative procedure is defined and the parameters to the Scenario will change

    Will generate 9 scenarios
"""

from scenariogeneration import xodr
from scenariogeneration import xosc, prettyprint
from scenariogeneration import ScenarioGenerator
from scenariogeneration import esmini
import numpy as np
import json


class Scenario(ScenarioGenerator):
    def __init__(self):
        ScenarioGenerator.__init__(self)
        self.naming = "numerical"
        self.open_scenario_version = 2

    def road(self, **kwargs):
        roads = []
        numintersections = 3
        angles = []
        nlanes = 1
        for i in range(numintersections):
            roads.append(
                xodr.create_road(
                [xodr.Line(100)],
                i,
                center_road_mark=xodr.STD_ROADMARK_BROKEN,
                left_lanes=nlanes,
                right_lanes=nlanes,
            )
            )
        angles = [0, np.pi/2, 3*np.pi/2]
        junction_roads = xodr.create_junction_roads(roads, angles, [20])
        junction = xodr.create_junction(junction_roads, 1, roads)

        odr = xodr.OpenDrive("myroad")
        odr.add_junction(junction)

        for r in roads:
            odr.add_road(r)

        for j in junction_roads:
            odr.add_road(j)

        odr.adjust_roads_and_lanes()
        return odr

    def scenario(self, **kwargs):
        road = xosc.RoadNetwork(self.road_file)
        egoname = "Ego"
        entities = xosc.Entities()


        ### create catalogs
        catalog = xosc.Catalog()
        catalog.add_catalog("VehicleCatalog", "../xosc/Catalogs/Vehicles")

        ### create parameters
        paramdec = xosc.ParameterDeclarations()

        ## create entities

        egoname = "Ego"
        targetname = "Target"

        entities = xosc.Entities()
        entities.add_scenario_object(
            egoname, xosc.CatalogReference("VehicleCatalog", "car_red")
        )

        ### create init

        init = xosc.Init()

        init.add_init_action(
            egoname, xosc.TeleportAction(xosc.LanePosition(10, 0, 1, 2)) #Teleport the vehicle to a start point
        )
        init.add_init_action(
            egoname,
            xosc.AbsoluteSpeedAction(
                10,
                xosc.TransitionDynamics(
                    xosc.DynamicsShapes.step, xosc.DynamicsDimension.time, 1
                ),
            ),
        )

        # create a router

        ego_route = xosc.Route("ego_route")
        ego_route.add_waypoint(
            xosc.LanePosition(30, 0, 1, 0), xosc.RouteStrategy.fastest
        )
        ego_route.add_waypoint(
            xosc.LanePosition(10, 0, -1, 1), xosc.RouteStrategy.fastest
        )

        # create action
        ego_action = xosc.AssignRouteAction(ego_route)

        ego_event = xosc.Event("ego_event", xosc.Priority.overwrite)
        ego_event.add_action("ego_route", ego_action)
        ego_event.add_trigger(
            xosc.ValueTrigger(
                "target_start",
                0,
                xosc.ConditionEdge.none,
                xosc.SimulationTimeCondition(1, xosc.Rule.greaterThan),
            )
        )

        ## create the storyboard
        ego_man = xosc.Maneuver("ego_man")
        ego_man.add_event(ego_event)

        sb = xosc.StoryBoard(
            init,
            xosc.ValueTrigger(
                "stop_simulation",
                0,
                xosc.ConditionEdge.rising,
                xosc.SimulationTimeCondition(10, xosc.Rule.greaterThan),
                "stop",
            ),
        )
        sb.add_maneuver(ego_man, egoname)

        ## create the scenario
        sce = xosc.Scenario(
            "adaptspeed_example",
            "User",
            paramdec,
            entities=entities,
            storyboard=sb,
            roadnetwork=road,
            catalog=catalog,
            osc_minor_version=self.open_scenario_version,
        )
        return sce


if __name__ == "__main__":
    s = Scenario()

    #with open('config.json') as json_file:
    #    data = json.load(json_file)

    parameters = {}
    parameters["speed"] = [10]

    s.generate("my_scenarios", parameters)