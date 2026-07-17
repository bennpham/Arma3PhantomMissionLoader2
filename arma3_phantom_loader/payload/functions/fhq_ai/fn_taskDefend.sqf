/* Defend a position
 * 
 * This function orders the given group to defend the given position.
 * 
 * It will do the following:
 * - Man empty static weapons
 * - Place guards around the position
 * - Send out patrols around the perimeter
 * - Put guards on buildings (preferring those with optics)
 * (- If the group has static weapon backpacks, put them up)
 * 
 * Immediate setup will move units into position directly. Otherwise, units
 * will, for example, move to a static weapon before getting in.
 * 
 * Parameters:
 *  _this select 0: Group that does the defending
 *  _this select 1: Position to defend
 *  _this select 2: Radius of defence (optional, default 30)
 *  _this select 3: Percentage of units to put into houses (optional, default 50 %)
 *  _this select 4: Number of units to go on patrol (default 2)
 *  _this select 5: Teleport units instead of moving (default false)
 */

//#define DEBUG

#define STATIC_CHANCE 20
#define SITDOWN_CHANCE 30

#define POP_UNIT _units select ((count _units) - 1); _units deleteAt ((count _units) - 1);

private "_i";
    
if ((count _this) < 2) exitWith {false;};

private _grp = param [0, grpNull, [grpNull]];
private _pos = param [1, [0, 0, 0], [[2,3]]];

/* Bail out if the group isn't local to this machine */
if (!local _grp) exitWith {};

_grp setBehaviour "SAFE";

private _radius = param [2, 30, [0]];
private _percent = param [3, 50, [0]];
private _numPatrol = param [4, 2, [0]];
private _teleport = param [5, false, [false]];

#ifdef DEBUG
private _debugMarker = createMarker [format ["debugmarker%1%2", random 100, random 100], _pos];
_debugMarker setMarkerShape "ELLIPSE";
_debugMarker setMarkerColor "ColorGreen";
_debugMarker setMarkerSize [_radius, _radius];
#endif

private _nearBuildings = _pos nearObjects ["Building", _radius];
private _nearStatic = _pos nearObjects ["StaticWeapon", _radius];
private _units = units _grp;

private _allBuildingPos =  [];
/* Find building positions */
{
    private _pos = _x buildingPos -1;
    if (count _pos != 0) then {
        _allBuildingPos = _allBuildingPos +  _pos;
    };
} foreach _nearBuildings;
diag_log str _allBuildingPos;
_nearBuildings = nil;

private _allStatics = [];
/* Remove all statics with gunners */
{
    if ((_x emptyPositions "Gunner") != 0) then {
        _allStatics pushBack _x;
   	};
} foreach _nearStatic;
_nearStatic = nil;

/* Assign units to static weapons */
{
    if ((random 100) > STATIC_CHANCE) then {
        private _unit = POP_UNIT;
        
        _unit assignAsGunner _x;      
        [_unit] orderGetIn true;
    };
} foreach _allStatics;

/* Assign two units as perimeter guard */
if (count _units > _numPatrol) then {
	private _grp2 = createGroup (side _grp);
    for "_i" from 0 to _numPatrol-1 do {
		private _unit = POP_UNIT;
       [_unit] joinSilent _grp2;
   	};
     
    private "_wp";
    for "_i" from 0 to 360 step 60 do {
        private _wpPos = [_pos, ((_radius*2) + random 10) - 5, (_i + random 20) - 10] call BIS_fnc_relPos;
    	_wp = _grp2 addWaypoint [_wpPos, 5];
        _wp setWaypointSpeed "LIMITED";
		_wp setWaypointBehaviour "SAFE";
        _wp setWaypointCombatMode "RED";
    };
    _wp setWaypointType "CYCLE";
};

private _remaining = count _units;
private _inBuildings = _remaining * (_percent/100.0);

for "_i" from 0 to _inBuildings - 1 do {
    /* Select a building position */
    if (count _allBuildingPos > 0) then {
        private _unit = POP_UNIT;
       	private _building = floor random ((count _allBuildingPos));
    	private _pos = _allBuildingPos select _building;
    	_allBuildingPos deleteAt _building;

		[_unit, _pos, _teleport] spawn {
	        //diag_log str _this;
    		private _unit = _this select 0;
        	private _pos = _this select 1;
			private _teleport = _this select 2;

			if (_teleport) then {
				_unit setPos _pos;
			} else {
			_unit doMove _pos;
			};
        	waitUntil {unitReady _unit};
        	doStop _unit;
        	/* Since the team leader will at one point order them back into
         	* formation, disable moving, wait for it to be ordered to attack, and then 
         	* allow movement again
         	*/
        	_unit disableAI "move";
        	
        	waituntil {(behaviour _unit == "COMBAT") || (behaviour _unit == "STEALTH") || (!unitReady _unit)}; 
        	_unit enableAI "move";
    	};
	};
};

private _wp = _grp addWaypoint [_pos, _radius];
_wp setWaypointType "HOLD";

_units spawn {
    sleep 5;
	{
	    /* Remaining can do random idle stuff */
        /* FIXME: Make them sit around campfires */
	    if ((random 100) > SITDOWN_CHANCE) then {
        	doStop _x;
        	sleep 1;
        	_x action ["SitDown", _x];
    	};
	} foreach _this;
};
