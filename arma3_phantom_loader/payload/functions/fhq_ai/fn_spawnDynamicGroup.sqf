/* Internal function
 * 
 * Used to spawn a dynamic group
 * Parameters:
 * _this select 0: Template group
 * _this select 1: Area
 * _this select 2: Init code
 * _this select 3: Blacklist
 * 
 * Return:
 * The spawned group
 * 
 * Possible variables on groups:
 * "FHQ_DynSpawnRoad": Spawn on roads (Default: true for ground vehicles, false for all others)
 * "FHQ_DynSpawnWater": Spawn on water (Default: true for boats, false for others)
 * "FHQ_DynSpawnGuard": Once spawned, start guarding:
 * 						"Building" - Find near building to garrison
 * 						"Guard" - Guard the spawn location 
 * "FHQ_DynSpawnPatrol": Once spawned, send this group on a patrol (patrol points on Road if FHQ_DynSpawnRoad is set):
 * 						 "Random" - Random points inside the area
 * 						 "Perimeter" - Along the edge of the area
 * 						 "Buildings" - Find buildings in the area and move to those
 * 						 "Loiter" - Loiter on spawn point
 * 						 "None" - Do nothing
 */

private _tmplGrp = param [0];
private _area = param [1, [], [[]]];
private _init = param [2, {}];
private _blackList = param [3, [], [[]]];
 
private _clone = createGroup [side _tmplGrp, true];

/* Read parameters of the given group */
private _road = _tmplGrp getVariable ["FHQ_DynSpawnRoad", [_tmplGrp] call FHQ_fnc_groupHasWheeled];
private _sea = _tmplGrp getVariable ["FHQ_DynSpawnWater",  [_tmplGrp] call FHQ_fnc_groupHasBoat];
private _garrison = _tmplGrp getVariable ["FHQ_DynSpawnGuard", "None"];
private _patrol = _tmplGrp getVariable ["FHQ_DynSpawnPatrol", "None"];

/* Find a position to put the group */
private _destPos = [0, 0, 0];
private _filter = {!(surfaceIsWater _this)};

if (_road) then {
    _filter = {
		if (!isNull (roadAt _this)) exitWith {true};
       	private _roads = _this nearRoads 50;
 		if (count _roads != 0) exitWith {getPos (_roads select 0)};
	   	false;
    };
};

if (_sea) then {
    _filter = {(surfaceIsWater _this) and ((getTerrainHeightASL _this) < -0.5)};
};

/* TODO: If a vehicle is present, find an empty space via findEmptyPosition */
_destPos = [_area, _blackList, _filter] call FHQ_fnc_getRandomPos;

private _grp = [_tmplGrp, _destPos] call FHQ_fnc_cloneGroup;
[_grp] call _init;

if ((tolower _garrison) != "none") then {
	switch (tolower _garrison) do {
        case "guard": {
            /* Let them guard this position */
			[_grp, getPos leader _grp] call FHQ_fnc_taskDefend;
            //[getPos leader _grp, "waypoint", 0.5, "guard"] call FHQ_fnc_debugMarker;
        };
        case "building": {
            /* Find a nearby building */
            private _pos = getpos leader _grp;
            private _list = nearestObjects [_pos, ["house"], 50];
            for "_i" from 0 to (count _list - 1) do {
                private _positions = (_list select _i) buildingPos -1;
                if (count _positions != 0) exitWith {
             		_pos = getPos (_list select _i);
                };
            };
            //[getPos leader _grp, "waypoint", 0.5, "building"] call FHQ_fnc_debugMarker;
            [_grp, _pos] call FHQ_fnc_taskDefend;
		};
	};
};

if ((tolower _patrol) != "none") then {
    [_grp, _area select 0, _patrol, _filter] call FHQ_fnc_taskPatrol;
};

_grp;