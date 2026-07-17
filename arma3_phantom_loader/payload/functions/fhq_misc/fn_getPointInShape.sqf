/* File: fn_getPointInShape.sqf
 * Author: Thomas "Varanon" Frieden
 * 
 * Description:
 * Generate a random point somewhere in a given shape.
 * 
 * Parameters(s):
 * _this select 0: Shape, either "Rectangle" or "Ellipse" (STRING)
 * _this select 1: Position (array)
 * _this select 2: Size [xsize, ysize] (array)
 * _this select 3: Direction, 0 is east (scalar) 
 * 
 * Returns:
 * position (array)
 * 
 */
 
private ["_tX", "_tY", "_size", "_marker", "_pos", "_dir", "_shape", "_x", "_y", "_dist", "_phi"];

_shape = [_this, 0, "Ellipse", ["string"]] call BIS_fnc_param;
_pos = [_this, 1, [0, 0, 0], [[]], [2,3]] call BIS_fnc_param;
_size = [_this, 2, [0, 0], [[]], [2]] call BIS_fnc_param;
_dir = [_this, 3, 0.0, [0.0]] call BIS_fnc_param;

_x = 0;
_y = 0;

if ((toupper _shape) == "RECTANGLE") then {
    _tX = 1.0 - ((random 20000) / 10000.0);
	_tY = 1.0 - ((random 20000) / 10000.0); 
	/* Calculate the actual coordinates. */
    _x = (_pos select 0) + (((_tX * (_size select 0)) * cos(-_dir)) - ((_tY * (_size select 1)) * sin(-_dir)));
    _y = (_pos select 1) + (((_tX * (_size select 0)) * sin(-_dir)) + ((_tY * (_size select 1)) * cos(-_dir)));
} else {
    _dist = (random 10000) / 10000.0 + (random 10000) / 10000.0;
    _phi = (random 36000) / 100.0;
    if (_dist > 1.0) then {_dist = 2.0 - _dist};
    _tX = (_dist * (_size select 0)) * sin(_phi);
    _ty = (_dist * (_size select 1)) * cos(_phi);
    _x = (_pos select 0) + (_tX * cos(-_dir)) - (_tY * sin(-_dir));
    _y = (_pos select 1) + (_tX * sin(-_dir)) + (_tY * cos(-_dir));
};

[_x, _y, 0]