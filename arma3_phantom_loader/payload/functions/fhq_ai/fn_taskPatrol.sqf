/* Generate a patrol for a given group
 * 
 * Parameters:
 * _this select 0: Group
 * _this select 1: Area (see below)
 * _this select 2: Patrol type (optional, default "Random")
 * _this select 3: Filter code (optional, see below)
 * _this select 4: Amount of waypoints (optional, default 4)
 * _this select 5: Code to be called when the last waypoint is reached. (Optional, see below)
 * _this select 6: Code to be called on each waypoint (Optional, same parameters as the last waypoint code)
 * 
 * The area description and filter functions are compatible to FHQ_fnc_findPositionInArea. Each potential waypoint
 * is generated inside the given area constrained by the filter function (see FHQ_fnc_findPositionInArea for more
 * information).
 * 
 * The end-patrol code is called in the last waypoint. By default, it does nothing, and the group continues to cycle
 * through it's patrol. You can opt to delete all waypoints and call this function again to generate a new route. The
 * code is called with the parameters originally passed into this function, so "_this call FHQ_fnc_taskPatrol;" would
 * re-create a new route with the same parameters.
 * 
 * The type of patrol parameter determines how the patrol is generated:
 * "Random": The points are random. This might create pretty erratic patterns
 * "Perimeter": Points are generated near the edge of the area
 * "Buildings": Points are generated near buildings, to give the impression that the patrol is inspecting buildings in the area.
 *              Ignores the filter code.
 * "Roads":	Only travel on roads, ignores filter code.
 * "Secure": Useful for vehicles that travel cross country. The patrol consists of random waypoints, but the 
 *           group will stop at waypoints and wait for a few minutes, then move on
 * "Loiter": Air vehicles only. Selects a random position in the area and creates a loiter waypoint.
 */

private _grp = param [0];
private _area = param [1];
private _type = param [2, "Random"];
private _filter = param [3, {true}];
private _numWP = param [4, 4];
private _endCode = param [5, {}];
private _eachCode = param [6, {}];

if (!local _grp) exitWith {};

/* Remove all previous waypoints. Also wards against multiple execution */
while {(count (waypoints _grp)) > 0} do {
    deleteWaypoint ((waypoints _grp) select 0);
};

/* Store parameters */
_grp setVariable ["FHQ_TaskPatrol_Area", _area, true];
_grp setVariable ["FHQ_TaskPatrol_Type", _type, true];
_grp setVariable ["FHQ_TaskPatrol_Filter", _filter, true];
_grp setVariable ["FHQ_TaskPatrol_NumWP", _numWP, true];
_grp setVariable ["FHQ_TaskPatrol_EndCode", _endCode, true];
_grp setVariable ["FHQ_TaskPatrol_EachCode", _eachCode, true];

/* Code callbacks */
private _wpEndStatement = "[group this, (group this) getVariable 'FHQ_TaskPatrol_Area', (group this) getVariable 'FHQ_TaskPatrol_Type', (group this) getVariable 'FHQ_TaskPatrol_Filter', (group this) getVariable 'FHQ_TaskPatrol_numWP', (group this) getVariable 'FHQ_TaskPatrol_EndCode', (group this) getVariable 'FHQ_TaskPatrol_EachCode'] call ((group this) getVariable 'FHQ_TaskPatrol_EndCode');"; 
private _wpEachStatement = "[group this, (group this) getVariable 'FHQ_TaskPatrol_Area', (group this) getVariable 'FHQ_TaskPatrol_Type', (group this) getVariable 'FHQ_TaskPatrol_Filter', (group this) getVariable 'FHQ_TaskPatrol_numWP', (group this) getVariable 'FHQ_TaskPatrol_EndCode', (group this) getVariable 'FHQ_TaskPatrol_EachCode'] call ((group this) getVariable 'FHQ_TaskPatrol_EachCode');"; 
  
/* Check the area. If it is a single number, then we assume a circle centered
   at the position of the group's leader with the given radius */

if (_area isEqualType 0) then {
    _newarea = ["ELLIPSE", getPos (leader _grp), [_area, _area], 0];
    _area = _newarea;
};

/* Generate waypoints */
switch (tolower _type) do {
	//case "random": {
    default {
		for [ {private _i = 0}, {_i < _numWP}, {_i = _i + 1} ] do {
            private _pos =  [_area, _filter] call FHQ_fnc_findPositionInArea;

            if (!(_pos call FHQ_fnc_isPositionValid)) then {
                _pos = [_area, {true}] call FHQ_fnc_findPositionInArea;
            };
            
			private _wp = _grp addWaypoint [_pos, 5];
            //_wp setWaypointTimeout [0, random 5, 5 + random 5];
            if (_i == _numWP - 1) then {
                _wp setWaypointStatements ["true", _wpEndStatement];
                _wp setWaypointType "CYCLE";
            } else {
            	_wp setWaypointStatements ["true", _wpEachStatement];
            };
            if (tolower _type == "secure") then {
                _wp setWaypointTimeout [60, 120, 180];
            };
		};
	};
    case "roads": {
        private _roads = {
       		private _roads = _this nearRoads 10;
 			if (count _roads != 0) exitWith {getPos (_roads select 0)};
	   		false;
        };
        
		for [ {private _i = 0}, {_i < _numWP}, {_i = _i + 1} ] do {
            private _pos = [_area, _roads] call FHQ_fnc_findPositionInArea; 
            if (!(_pos call FHQ_fnc_isPositionValid)) then {
                _pos = [_area, _filter] call FHQ_fnc_findPositionInArea;
            };
            if (!(_pos call FHQ_fnc_isPositionValid)) then {
                _pos = [_area, {true}] call FHQ_fnc_findPositionInArea;
            };
            
			private _wp = _grp addWaypoint [_pos, 5];
            if (_i == _numWP - 1) then {
                _wp setWaypointStatements ["true", _wpEndStatement];
                _wp setWaypointType "CYCLE";
            } else {
            	_wp setWaypointStatements ["true", _wpEachStatement];
            };
		};
    };
    case "buildings": {
        private _buildings = {
       		private _list = nearestObjects [_this, ["house"], 10];
 			if (count _list != 0) exitWith {getPos (_list select 0)};
	   		false;
        };
        
		for [ {private _i = 0}, {_i < _numWP}, {_i = _i + 1} ] do {
            private _pos = [_area, _buildings] call FHQ_fnc_findPositionInArea;
            if (!(_pos call FHQ_fnc_isPositionValid)) then {
                _pos = [_area, _filter] call FHQ_fnc_findPositionInArea;
            };
            if (!(_pos call FHQ_fnc_isPositionValid)) then {
                _pos = [_area, {true}] call FHQ_fnc_findPositionInArea;
            };
            
			private _wp = _grp addWaypoint [_pos, 5];
            if (_i == _numWP - 1) then {
                _wp setWaypointStatements ["true", _wpEndStatement];
                _wp setWaypointType "CYCLE";
            } else {
            	_wp setWaypointStatements ["true", _wpEachStatement];
            };
		};
    };
    case "loiter": {
        private _pos =  [_area, _filter] call FHQ_fnc_findPositionInArea;

        if (!(_pos call FHQ_fnc_isPositionValid)) then {
            _pos = [_area, {true}] call FHQ_fnc_findPositionInArea;
        };
        
		private _wp = _grp addWaypoint [_pos, 5];
        _wp setWaypointType "LOITER";
        _wp setWaypointLoiterType "CIRCLE";
        _wp setWaypointLoiterRadius 50 + random (100);
	};
};
