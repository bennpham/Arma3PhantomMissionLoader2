/*
** Generate a patrol route for a given unit or group
**
** Parameters -
** 0: the group or leader of the group
** 1: [Optional] Name of the marker. Blank of "" to use the name of the group leader as the marker name
** 2: [Optional] Number of waypoints for the group. Default is 6
** 3: [Optional] If TRUE, generate a new route at the end of the patrol. If false (the default), cycle
** 4: [Optional] If TRUE, prefer waypoints on or near roads. Defaults to False
** 5: [Optional] if TRUE, delete all previous waypoints of the group. Default is TRUE
*/
private [
	"_leader", "_group", "_marker", "_pos", 
	"_road", "_numWaypoints", "_resetRoute", 
	"_roadWay", "_wp", "_deleteWP"
];

_group = param [0, objNull, [objNull, grpNull]];
_leader = objNull;
if (typeName _group != typename grpNull) then {
	_group = group _group;
	_leader = leader _group;
} else {
	_leader = leader _group;
};

_marker = param [1, str _leader, [""]];
_numWaypoints = param [2, 6, [0]];
_resetRoute = param [3, FALSE, [TRUE]];
_roadWay = param [4, FALSE, [TRUE]];
_deleteWP = param [5, TRUE, [TRUE]];
/*
** Check if the leader is defined. If not, exit
*/
if (isnull _leader) exitWith {
	["expected group or group leader for markerPatrol"] call BIS_fnc_Error;
};

/*
** Check the marker name, and see if it exists
*/

if (_marker == "") then {
	_marker = str _leader;
};

_pos = getMarkerPos _marker;
if ((_pos select 0) == 0 && (_pos select 1) == 0) exitWith {
	["Marker name %1 not found", _marker] call BIS_fnc_Error;
};

/*
** Everything we need is there. 
*/

// Delete previous waypoints
 while {(count (waypoints _group)) > 0} do
 {
	deleteWaypoint ((waypoints _group) select 0);
 };

// Make marker invisible just in case
_marker setMarkerAlpha 0;

for "_i" from 1 to _numWaypoints do {
	_pos = [_marker] call FHQ_fnc_getPointInMarker;
	if (_roadWay) then {
		_road = [_pos, 200, []] call BIS_fnc_nearestRoad;
		if (!isnull _road) then {
			_pos = position _road;
		};
	};
    
	_wp = _group addWaypoint [_pos, 5];
	_wp setWaypointBehaviour "SAFE";
	_wp setWaypointType "MOVE";
	_wp setWaypointSpeed "LIMITED";
	_wp setWaypointFormation "COLUMN";
	if (_i == _numWaypoints) then {
		if (!_resetRoute) then {
			_wp setWaypointType "CYCLE";
		} else {
			_wp setWaypointType "MOVE";
			_wp setWaypointStatements ["true", format ["_nil = [group %1,%2,%3,%4,%5,%6] call FHQ_fnc_markerPatrol;",
			_leader, _marker, _numWaypoints, _resetRoute, _roadWay, _deleteWP]];
		};
	};
};