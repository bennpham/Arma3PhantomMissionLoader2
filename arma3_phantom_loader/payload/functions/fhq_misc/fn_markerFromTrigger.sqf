/*
 * Create a marker from a trigger. The marker will be initially created fully transparent
 * to avoid "pop-up" effects.
 *
 * Parameters:
 * _this select 0: Trigger object
 * _this select 1: boolean. If true, delete the trigger afterwards. Default is false
 *
 * Returns: 
 * The marker created
 *
 */

params [
	["_trigger", objNull],
	["_deleteTrigger", false, [true]]
];

if (_trigger == objNull) exitWith {"NULL Trigger object" call BIS_fnc_log;};

_name = str time + str _trigger;
_area = triggerArea _trigger;

_marker = createMarkerLocal [_name, position _trigger];
_marker setMarkerAlphaLocal 0;
if ((_area # 3) == true) then 
{
	_marker setMarkerShapeLocal "RECTANGLE";
} 
else
{
	_marker setMarkerShapeLocal "ELLIPSE";
};
_marker setMarkerSizeLocal [_area # 0, _area # 1];
_marker setMarkerDirLocal _area # 2;

if (_deleteTrigger) then {
	deleteVehicle _trigger;
};

_marker