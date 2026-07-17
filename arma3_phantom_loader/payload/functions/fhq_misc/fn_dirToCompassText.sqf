/*
 * Convert a compass bearing to a one or two letter string.
 *
 * Parameter:
 * _this select 0: heading (0...360)
 *
 * Returns:
 * String representation of major 8-point compass direction.
 *
 */

params [
	["_dir", 0, [0]]
];

if (_dir > 360) then {
	_dir = _dir mod 360;
};

if (_dir >= 0 && _dir <= 22.5 ) exitWith {"north"};
if (_dir >= 22.5 && _dir <= 67.5) exitWith {"north-east"};
if (_dir >= 67.5 && _dir <= 112.5) exitWith {"east"};
if (_dir >= 112.5 && _dir <= 157.5) exitWith {"south-east"};
if (_dir >= 157.5 && _dir <= 202.5) exitWith {"south"};
if (_dir >= 202.5 && _dir <= 247.5) exitWith {"south-west"};
if (_dir >= 247.5 && _dir <= 292.5) exitWith {"west"};
if (_dir >= 292.5 && _dir <= 337.5) exitWith {"north-west"};
if (_dir >= 337.5 && _dir <= 360) exitWith {"north"};

"N"