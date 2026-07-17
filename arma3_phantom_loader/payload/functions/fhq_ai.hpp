class Tasks
{
	tag="FHQ";
	file="functions\fhq_ai";

	EXPORTED_FUNCTION(taskDefend, "Set up defenses around a given position")
	EXPORTED_FUNCTION(taskPatrol, "Generate a patrol route in a given area")
	EXPORTED_FUNCTION(markerPatrol, "Generate a patrol route inside a marker")
};

class Groups
{
	tag="FHQ";
	file="functions\fhq_ai";

	EXPORTED_FUNCTION(groupHasVehicle, "Check if the group has a vehicle")
	EXPORTED_FUNCTION(groupHasBoat, "Check if the group has a water vehicle")
	EXPORTED_FUNCTION(groupHasAirVehicle, "Check if the group has an air vehicle")
	EXPORTED_FUNCTION(groupHasCar, "Check if the group has a car (motorized)")
	EXPORTED_FUNCTION(groupHasArmor, "Check if the group has a tank/apc (mechanized)")
	EXPORTED_FUNCTION(groupHasWheeled, "Check if the group has a wheeled vehicle (including APCs)")
	EXPORTED_FUNCTION(warpGroup, "Move a group to a new position, retaining relative positions")
	EXPORTED_FUNCTION(cloneGroup, "Create a copy of a group at a new position, retaining relative position, loadouds and vehicles")
	EXPORTED_FUNCTION(clearBuilding, "clear a target building")
	EXPORTED_FUNCTION(clearBuildingNext, "used for clearBuilding, internal function")
};

class Dynamic
{
	tag="FHQ";
	file="functions\fhq_ai";

	EXPORTED_FUNCTION(dynamicSpawn, "Spawn a number of groups dynamically, for generated missions")
	EXPORTED_FUNCTION(setupDynamicLayers, "Pass in an array of layers and their costs")
	EXPORTED_FUNCTION(cleanupDynamicSpawn, "Remove the dynamic spawn templates, should be done before the mission starts")

	EXPORTED_FUNCTION(initTriggerSpawn, "Initialize Trigger Spawning system")

	INTERNAL_FUNCTION(spawnDynamicGroup)
	INTERNAL_FUNCTION(buildSpawnables)
};

class Convoy
{
	// Siil's convoy scripts, modified a bit for ease of use
	tag="FHQ";
	file="functions\fhq_ai";

	EXPORTED_FUNCTION(convoyInit, "Init Convoy Lead Vehicle")
	EXPORTED_FUNCTION(convoy, "Looks like we got us a convoy")
	EXPORTED_FUNCTION(convoyAmbushAction, "Perform Ambush Action")

};
