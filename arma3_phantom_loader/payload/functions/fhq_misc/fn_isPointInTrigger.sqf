/* File: fn_isPointInTrigger.sqf
 * Author: Thomas "Varanon" Frieden
 * 
 * Description:
 * Check if a point is within a given trigger
 * 
 * Parameters(s):
 * _this select 0: Point to check (array)
 * _this select 1: Trigger to check against (object)
 * 
 * Returns:
 * Boolean
 * 
 */
 
 private ["_trigger", "_triggerArea", "_pos"];

_pos = [_this, 0, [0,0,0], [[]], [2,3]] call BIS_fnc_param;
_trigger = [_this, 1, objNull, [objNull]] call BIS_fnc_param;
_triggerArea = triggerArea _trigger;
_res = false;

if (_triggerArea select 3) then {
	_res = [_pos, "RECTANGLE", getPos _trigger, [_triggerArea select 0, _triggerArea select 1], _triggerArea select 2] call FHQ_fnc_isPointInShape;
} else {
    _res = [_pos, "ELLIPSE", getPos _trigger, [_triggerArea select 0, _triggerArea select 1], _triggerArea select 2] call FHQ_fnc_isPointInShape;
};

_res;