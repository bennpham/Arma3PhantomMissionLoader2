class Time {
	tag="FHQ";
	file="functions\fhq_misc";

	EXPORTED_FUNCTION(date2String, "Convert a date to a string.")
	EXPORTED_FUNCTION(time2FuzzyString, "Convert current time into a fuzzy string")
};

class Spawning {
	tag="FHQ";
	file="functions\fhq_misc";

	EXPORTED_FUNCTION(checkPresence, "Check presence of an object depending on the difficulty")
	EXPORTED_FUNCTION(debugMarker, "Easily create a marker for debugging purposes")
	EXPORTED_FUNCTION(spawnGroup, "Create a group of vehicles")
	EXPORTED_FUNCTION(deleteGroup, "Delete all units and vehicles in the group, and the group itself")
	EXPORTED_FUNCTION(deleteTagged, "Delete everything tagged with a certain tag")
	EXPORTED_FUNCTION(cloneVehicle, "Clone a vehicle from a template with the same cargo")
};

class Units {
	tag="FHQ";
	file="functions\fhq_misc";

	EXPORTED_FUNCTION(safeAddLoadout, "Add a loadout to a unit, JIP friendly")
	EXPORTED_FUNCTION(enableUnit, "Enable a unit that has been disabled")
	EXPORTED_FUNCTION(disableUnit, "Disable a unit so it minimizes resources used")
	EXPORTED_FUNCTION(disableGroup, "Disables all units in a group, including vehicles and UAV's")
	EXPORTED_FUNCTION(enableGroup, "Enable a previously disabled group")
	EXPORTED_FUNCTION(findLeader, "Find a leader in the given groups. Groups may also be empty")
	EXPORTED_FUNCTION(findBoundingCircle, "Find the circle enclosing all given units in an array")
	EXPORTED_FUNCTION(unitsInTrigger, "Find all units in a given trigger")
	EXPORTED_FUNCTION(areUnitsInTrigger, "Check if all given units are in a trigger")
	EXPORTED_FUNCTION(getOpsLeader, "Get the highest ranking player")
	EXPORTED_FUNCTION(getOtherPlayer, "Get another player")
	EXPORTED_FUNCTION(kbTell, "Locality Aware KBTell")
	EXPORTED_FUNCTION(detectedBy, "Determine if a group of units has been detected")
	EXPORTED_FUNCTION(aceLoadout, "Add a class-specific set of ACE items if ACE is loaded")
	EXPORTED_FUNCTION(kbTellST, "Subtitle Version of kbTell")
	EXPORTED_FUNCTION(getThreatLevel, "Get Threat level from a chemical detector")
};

class Positions {
	tag="FHQ";
	file="functions\fhq_misc";

	EXPORTED_FUNCTION(getPointInMarker, "Generate a random point in a given marker")
	EXPORTED_FUNCTION(getPointInTrigger, "Generate a random point in a given trigger")
	EXPORTED_FUNCTION(getPointInShape, "Generate a random point in a given shape")
	EXPORTED_FUNCTION(isPointInShape, "Check if a given point is inside the given shape")
	EXPORTED_FUNCTION(isPointInMarker, "Check if a given point is inside the given marker")
	EXPORTED_FUNCTION(isPointInTrigger, "Check if a given point is inside the given shape")
	EXPORTED_FUNCTION(getRandomPos, "Generate a random position")
	EXPORTED_FUNCTION(getRoadPosition, "Generate a random position on a road")
	EXPORTED_FUNCTION(findPositionInArea, "Find a position in an area given certain constraints")
	EXPORTED_FUNCTION(isPositionInArea, "Check if a given position is inside the given area")
	EXPORTED_FUNCTION(isPositionValid, "Check if the position is valid, i.e !0 [0, 0, 0]")
	EXPORTED_FUNCTION(getObjectSpeed, "Get object's speed in m/s")
	EXPORTED_FUNCTION(markerFromTrigger, "Create a marker from a trigger with the same shape and area")
	EXPORTED_FUNCTION(dirToCompassText, "Convert a direction to a compass text like NE, S, W etc.")
};

class Intro {
	tag="FHQ";
	file="functions\fhq_misc";

	EXPORTED_FUNCTION(fadeQuote, "Generate title quote")
	EXPORTED_FUNCTION(introDsp, "Generate ticker text")
	EXPORTED_FUNCTION(textQuote, "Generate title quote")
};

class Transport {
	tag="FHQ";
	file="functions\fhq_misc";

	EXPORTED_FUNCTION(createExtraction, "Create extraction vehicle(s) and have them pick up a bunch of units")
	EXPORTED_FUNCTION(createInsertion, "Use existing vehicles to insert a group of people")
	EXPORTED_FUNCTION(createHALOJump, "Set up for a HALO jump including backpack stowage")
};

class Effect {
	tag="FHQ";
	file="functions\fhq_misc";

	EXPORTED_FUNCTION(weatherEffect, "Weather effects like snow and fog")
	EXPORTED_FUNCTION(setWeatherEffect, "Update parameters of weather effects")
};

class Layer {
	tag="FHQ";
	file="functions\fhq_misc";

	EXPORTED_FUNCTION(warpLayer, "Move all objects of a given layer to a given position, keeping relative positions")
	EXPORTED_FUNCTION(deleteLayer, "Delete all objects and markers is given layer")
};

class Camp {
	tag="FHQ";
	file="functions\fhq_misc";

	//EXPORTED_FUNCTION(campStore, "Store a camp composition")
	EXPORTED_FUNCTION(campSpawn, "Spawn a previously stored camp")
}