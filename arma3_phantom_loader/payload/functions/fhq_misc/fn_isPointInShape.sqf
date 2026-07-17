/* File: fn_isPointInShape.sqf
 * Author: Thomas "Varanon" Frieden
 * 
 * Description:
 * Check if a point is within a given shape
 * 
 * Parameters(s):
 * _this select 0: Point to check (array)
 * _this select 1: Shape, either "Rectangle" or "Ellipse" (STRING)
 * _this select 2: Position (array)
 * _this select 3: Size [xsize, ysize] (array)
 * _this select 4: Direction, 0 is east (scalar) 
 * 
 * Returns:
 * Boolean
 * 
 */
 
 
private ["_xc", "_yc", "_xsize", "_ysize", "_cos", "_sin", "_testPoint", "_shape", "_pos", "_size", "_dir"];

_testPoint = [_this, 0, [0, 0, 0], [[]], [2,3]] call BIS_fnc_param;
_shape = [_this, 1, "Ellipse", ["string"]] call BIS_fnc_param;
_pos = [_this, 2, [0, 0, 0], [[]], [2,3]] call BIS_fnc_param;
_size = [_this, 3, [0, 0], [[]], [2]] call BIS_fnc_param;
_dir = [_this, 4, 0.0, [0.0]] call BIS_fnc_param;

_res = false;

diag_log str _size;
diag_log _shape;

/* We use a simple method of transforming the point to the coordinate system of the shape
 * we want to check. This basically means tranposing the point by the center of the 
 * shape and rotating it by the negative angle.
 */
_xc = _pos select 0;
_yc = _pos select 1;
_xsize = _size select 0;
_ysize = _size select 1;
_cos = cos (_dir);
_sin = sin (_dir);
        
_xp = ((_testPoint select 0) - _xc) * _cos - ((_testPoint select 1) - _yc) * _sin;
_yp = ((_testPoint select 1) - _yc) * _cos + ((_testPoint select 0) - _xc) * _sin;


if ((toupper _shape) == "RECTANGLE") then {
	/* For the rectangle, the test is now simply checking whether the transferred point
     * is within the rectangle bounds
     */
    if ((_xp > -_xsize && _xp < _xsize && _yp > -_ysize && _yp < _ysize)) exitWith {
		_res = true;
    };
} else {
    /* We now have to check against a centered, axis parallel ellipse, so if 
     * x^2/a^2 + y^2/b^2 <= 1, it's in
     */
    if ( ((_xp*_xp)/(_xsize*_xsize)) + ((_yp*_yp)/(_ysize*_ysize)) <= 1) exitWith {
        _res = true;
    };
};

_res;