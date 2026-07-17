/*
	Description:
	Cause AI group to search a building for enemy
 
	Parameter(s):
	_this select 0:	group
	_this select 1: building to search
	_this select 2: (optional) maximum time to search
 
	Returns:
	Nothing
	
*/

if (!canSuspend) exitWith { _this spawn FHQ_fnc_clearBuilding; };

params [
	["_grp", grpNull, [grpNull]],
	["_pos", [0,0,0], [[], objNull]],
	["_timeout", 480, [0]]
];

if (!local (leader _grp)) exitWith {};

private _building = _pos;

if (_pos isEqualType []) then {
	_building = _pos nearestObject "House";
};

private _buildingPos = _building buildingPos -1;

if (count _buildingPos == 0) exitWith {diag_log "clearBuilding on non-enterable building";};

private _leader = leader _grp;
private _cnt = (count units _grp) -1;
private _numGrps = 1;

if (_cnt > 5) then {
	_numGrps = _cnt / 3;
};

if ((count _buildingPos ) < _numGrps) then {
	_numGrps = count _buildingPos;
};

_groups = [];

_leader = leader _grp;
_units = units _grp;
_units = _units - [_leader];
_side = side _leader;

_logic = _grp createUnit ["LOGIC", position _leader, [], 0, "NONE"];

_logic setVariable ["FHQ_clearBuilding_lock", true];

_grpSize = _cnt / _numGrps;

for "_i" from 0 to _numGrps do {
	_u = _units select [0,_grpSize];

	_units deleteRange [0,_grpSize];
	private _group = createGroup [_side, true];

	_u joinSilent _group;
	_groups pushBack _group;
	(leader _group) setVariable ["FHQ_clearBuilding_original", _grp];
	(leader _group) setVariable ["FHQ_clearBuilding_logic", _logic];

	_newPos = _buildingPos select 0;
	_buildingPos deleteAt 0;

	_wp = _group addWaypoint [_newPos, 1.8];
	_wp setWaypointType "MOVE";
	_wp setWaypointCombatMode "YELLOW";
	_wp setWaypointStatements ["true", "[group this] spawn FHQ_fnc_ClearBuildingNext;"];
};

_logic setVariable ["FHQ_clearBuilding_positions", _buildingPos];
_logic setVariable ["FHQ_clearBuilding_lock", false];

_logicLoop = true;
_now = time;
while {_logicLoop} do {
	sleep 30;
	
	if ((_now + _timeout) < time) then {
		// - Watchdog timer - 8 minutes, merge all groups back
		{
			(units _x) joinSilent _grp;
		} forEach _groups;
	};

	// Check if all our groups are empty
	_g = 0;
	{
		_g = _g + ({alive _x} count (units _x)); 
	} forEach _groups;

	if (_g == 0) then {
		// either everyone was killed or the groups finished their tasks
		deleteVehicle _logic;
		_logicLoop = false;
	};
};
