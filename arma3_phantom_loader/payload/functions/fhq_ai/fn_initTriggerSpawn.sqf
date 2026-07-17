
/*
 * Initialize the spawning system
 *
 * The system picks random groups and vehicles from a number of Eden layers
 * named in a certain manner. The layer naming is as following:
 *
 * EG_0, EG_1, ... for "easy" groups
 * SG_0, SG_1, ... for "normal" difficulty groups
 * HG_0, HG_1, ... for "hard" difficulty groups
 *
 * Normal difficulty is, well, normal, and if EG_ or HG_ layers are not defined,
 * the SG_ layers are used instead. IF all layer types are defined, their numbers needs to match.
 * SG_* layers MUST be present.
 *
 * Parameters:
 * _this select 0: difficulty (optional, 0 (easy), 1 (normal) or 2 (hard). Default is 1) 
 *
 * How to use:
 *
 * Create the appropriate layers (they can be in their own sub-layer to keep things tidy)
 * and fill them with groups or empty vehicles. Groups and vehicles are handled differently 
 * (see below). Note that vehicles that are NOT empty 
 * are not added to the spawnables, since they are assumed to belong to a group. Only empty vehicles
 * can be spawnables.
 *
 * It is generally recommended that you keep groups and empty vehicles in their own layers. 
 *
 * Triggers are placed on the map were groups and vehicles should spawn. The "Text" field of the trigger
 * is a formatted string that has the following template:
 *
 * SP,<number>[,option:value]*
 *
 * <number> is the layer from which to select a group or vehicle, so for example a text of "1" will 
 * use a spawnable from layer EG_1, SG_1 or HG_1. You can add options to that in the form of a comma-separated
 * list of key:value pairs. The following key/values can be used right now:
 *
 * - spawn:<condition>
 *      When spawning, look for a specific place to spawn on. Default is nothing which just picks
 *		a random point. "road" will make sure the group spawns on a road. "water" will ensure a spawn
 *      point in the water. Finally, you can specify a marker name and the point will be randomly selected
 *      inside that marker
 *
 * - task:<task>
 *      Define a task for the group after spawning. <task> can be either "defend" or "patrol". "defend"
 *      will use the spawn position to call FHQ_fnc_taskDefend, meaning they will man buildings, send
 *      out patrols, and occupy static weapons. "patrol" will generate a patrol inside the trigger area.
 *
 * - rep:<number>
 *      <number> represents the number of repeated spawns this trigger will cause. That is, if rep is e.g. 3
 *      it will randomly select a spawnable from the indicated group three times.
 *
 * - range:<number>
 *      <number> is the range (in meters) any player must approach the trigger center in order to cause the 
 *      spawn operation to start. The default is one klick (1000 meters). As soon as a player gets closer
 *      than this number, the spawn is triggered. Note that the trigger area is not relevant, since the
 *      trigger is actually deleted on mission startup.
 *
 * - patrol:<type>
 *      Set the type of patrol if task:patrol is specified. The values correspond to the 
 *      third parameter of FHQ_fnc_taskPatrol.
 *
 * - dynamic:<yes|no>
 *      Enable dynamic simulation for the spawn. By default this is set to yet, use "no" for patrols that
 *      cover a large area (like planes or helicopters)
 *
 * Examples:
 *   Spawn a group to guard the point of the trigger from layer xG_1:
 *	 "SP,1,task:defend" (note no spaces)
 *
 *   Spawn three groups to patrol the trigger area from layer xG_0:
 *   "SP,0,task:patrol,rep:3"
 *
 * If the spawnable is a vehicle, the vehicle is played ON the trigger facing the direction of the trigger. 
 * This can be used to spawn boats, civilian vehicles, and other stuff. Note that the vehicles will be a carbon
 * copy of the one put down in the layer; damage, fuel, cargo and even vehicle customization will be copied.
 * Naturally, neither task nor rep makes sense for vehicles, in fact, rep will probably cause spontaneous
 * self-combustion.
 *
 * If the spawnable is a group, the starting position of the group is put at a random point inside the
 * trigger area. If rep is used, random points are generated for each group.
 *
 * Triggers can be placed anywhere, and should not have anything set as their activation. It is sufficient
 * to just put a trigger and edit its text; no other action is required, except for adjusting the size.
 *
 */

params [
	["_difficultyLevel", 1, [1]]
];

FHQ_SpawnableCategoriesNormal = ["SG_"] call FHQ_fnc_buildSpawnables;
FHQ_SpawnableCategoriesEasy = ["EG_", "SG_"] call FHQ_fnc_buildSpawnables;
FHQ_SpawnableCategoriesHard = ["HG_", "SG_"] call FHQ_fnc_buildSpawnables;

FHQ_SpanwableArrays = [];
if (count FHQ_SpawnableCategoriesEasy > 0) then
{
	FHQ_SpanwableArrays set [0, FHQ_SpawnableCategoriesEasy];
} else {
	FHQ_SpanwableArrays set [0, FHQ_SpawnableCategoriesNormal];
};

if (count FHQ_SpawnableCategoriesHard > 0) then
{
	FHQ_SpanwableArrays set [2, FHQ_SpawnableCategoriesHard];
} else {
	FHQ_SpanwableArrays set [2, FHQ_SpawnableCategoriesNormal];
};

FHQ_SpanwableArrays set [1, FHQ_SpawnableCategoriesNormal];
_spawnableCategoryCount = count FHQ_SpawnableCategoriesNormal;

/* Set up the spawns */
{
	_txt = triggerText _x;
	if (count _txt > 0) then 
	{
		if (tolower (_txt select [0,3]) == "sp,") then 
		{

			_tokens = _txt splitString ",";
			_cat = parseNumber (_tokens # 0);
			if (_cat < _spawnableCategoryCount) then {
				[_x, _tokens, _difficultyLevel] spawn {
					_trigger = _this # 0;
					_tokens = _this # 1;
					_difficultyLevel = _this # 2;
					_tokens deleteAt 0; // Delete the "SP" prefix
					_cat = parseNumber (_tokens # 0);
					_rad = (triggerArea _trigger) select 0;
					_basePos = position _trigger;
					_dir = (triggerArea _trigger) select 2;
					if (_dir < 0) then {_dir = 360 + _dir};

					_marker = [_trigger, true] call FHQ_fnc_markerFromTrigger;

					_tokens deleteAt 0;

					_paramArray = [
						"default", 	// Spawn
						"defend",	// task
						1,			// rep
						1000,		// range
						"Random",	// Patrol
						"yes"		// dynamic
					];

					{
						_token = (tolower _x) splitString ":";
						_tag = _token # 0;
						_arg = _token # 1;

						switch (_tag) do
						{
							case "spawn"	: {_paramArray set [0,_arg]};
							case "task" 	: {_paramArray set [1,_arg]};
							case "rep"  	: {_paramArray set [2, parseNumber _arg]};
							case "range"	: {_paramArray set [3, parseNumber _arg]};
							case "patrol"	: {_paramArray set [4, _arg]};
							case "dynamic"  : {_paramArray set [5, _arg]};
						};

					} forEach _tokens;

					waitUntil {sleep 5; ({(_x distance2d _basePos) < (_paramArray # 3)} count allPlayers > 0)};

					_repeat = _paramArray # 2;

					while {_repeat > 0} do 
					{
						_array = FHQ_SpanwableArrays # _difficultyLevel;
						_spawnable = selectRandom (_array # _cat);
						if (_spawnable isEqualType grpNull) then
						{
							_patrol = _paramArray # 4;
							_filterCode = switch (_paramArray # 0) do
							{
								case "water": {
									{
										surfaceIsWater _this
									}
								};
								case "road": {
									{
										private _roads = _this nearRoads 50;
										if (count _roads != 0) exitWith {getPos (_roads select 0)};
 										false;
									}
								};
								default
								{
									{true}
								};
							};
							
							// Spawn group
							_spawnMarker = _marker;
							if (_filterCode isEqualTo {true}) then
							{
								if (count (_paramArray # 0) > 0) then 
								{
									_spawnMarker = _paramArray # 0;
								};
							};


							private _tries = 10;
							_pos = [0,0,0];
							while {_tries > 0} do {
								_tries = _tries - 1;
								_pos = [_spawnMarker, _filterCode] call FHQ_fnc_findPositionInArea;
								
								if (_pos isEqualTo [0,0,0]) then 
								{
									_pos = _basePos;
								};
								
								private _numClose = {(_x distance2d _pos) < 200} count allPlayers;

								//diag_log format ["SPAWN: _numClose = %1", _numClose];

								if (_numClose == 0) then {
									_tries = -1;
								};

							};	
							//systemChat format ["spawn position _pos = %1", _pos];
							_pos set [2,0];
							_newGrp = [_spawnable, _pos] call FHQ_fnc_cloneGroup;
							_newGrp setBehaviour "SAFE";
							_newGrp setSpeedMode "LIMITED";

							{
								_x addCuratorEditableObjects [(units _newGrp)];
							} forEach allCurators;

							// Enable dynamic simulation
							if ((_paramArray # 5) isEqualTo "yes") then 
							{
								_newGrp enableDynamicSimulation true;
							};

							switch (_paramArray # 1) do
							{
								case "patrol":
								{
									_newGrp setSpeedMode "LIMITED";
									_newGrp setBehaviour "SAFE";
									_newGrp setFormation "COLUMN";

									[_newGrp, _marker, _patrol] call FHQ_fnc_taskPatrol;
								};
								case "defend":
								{
									[_newGrp, _pos] call FHQ_fnc_taskDefend;
								};
							};
						}
						else
						{
							// Spawn object
							_veh = [_spawnable, _basePos, _dir] call FHQ_fnc_cloneVehicle;
							{
								_x addCuratorEditableObjects [[_veh], true];
							} forEach allCurators;
						};
						_repeat = _repeat - 1;
					};
				};
			};
		};
	};
} forEach (allMissionObjects "EmptyDetector");