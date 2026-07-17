/* Check if a point is in an area.
 * 
 * This function takes a position as first parameter, and an area description as the second parameter 
 * (either a marker, a trigger, or a shape given by an array 
 * ["RECTANGLE"|"ELLIPSE", _center, [_xsize, _ysize], _direction].
 * 
 */

private _pos = param [0, [0, 0, 0], [[]], [2,3]];
private _area = param [1, objNull, [objNull, "", []], [4]];
 
 
_result = (switch (typeName _area) do {
	case "ARRAY": {
		[_pos, _area select 0, _area select 1, _area select 2, _area select 3]  call FHQ_fnc_isPointInArea;
	};
	case "STRING": {
		[_pos, _area] call FHQ_fnc_isPointInMarker;
	};
	case "OBJECT": {
        [_pos, _area] call FHQ_fnc_isPointInTrigger;
	};
});

_result;