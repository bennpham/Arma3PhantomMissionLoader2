/* File: fn_getPointInTrigger.sqf
 * Author: Thomas "Varanon" Frieden
 * 
 * Description:
 * Generate a random point somewhere in a given trigger. The trigger can have
 * any shape (ellipse or rectangle) and can be rotated
 * 
 * Parameters(s):
 * _this select 0: Trigger
 * 
 * Returns:
 * position (array)
 * 
 */
private ["_trigger", "_triggerArea"];

_trigger = [_this, 0, objNull, [objNull]] call BIS_fnc_param;
_triggerArea = triggerArea _trigger;
_pos = [];

if (_triggerArea select 3) then {
	_pos = ["RECTANGLE", getPos _trigger, [_triggerArea select 0, _triggerArea select 1], _triggerArea select 2] call FHQ_fnc_getPointInShape;
} else {
    _pos = ["ELLIPSE", getPos _trigger, [_triggerArea select 0, _triggerArea select 1], _triggerArea select 2] call FHQ_fnc_getPointInShape;
};

_pos;