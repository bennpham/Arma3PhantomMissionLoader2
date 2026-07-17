// Put on the convoy lead vehicle
_veh = _this select 0;
_group = group _veh;

_tmp = _veh getVariable "FHQ_WaypointArray";
if (!isnil "_tmp") exitWith {};

_wpArray = [];

_wps = waypoints group _veh;

{
    _pos = waypointPosition _x;
    _wpArray pushBack _pos;

} forEach _wps;

for "_i" from count waypoints _group - 1 to 0 step -1 do
{
	deleteWaypoint [_group, _i];
};

_veh setVariable ["FHQ_WaypointArray", _wpArray, true];