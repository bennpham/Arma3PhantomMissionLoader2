/* Find a position in a given area filtered by constraints.
 * 
 * This function takes an area description (either a marker, a trigger, or a shape given by an array 
 * ["RECTANGLE"|"ELLIPSE", _center, [_xsize, _ysize], _direction] (_direction east = 0).
 * 
 * It tries to find a position inside that marker that fulfils the constraints defined by a piece of code
 * that is the second parameter to this function. The third parameter gives the maximum tries.
 * 
 * The constraints function receives the generated position as it's argument, and must return true or false.
 * Returning true accepts the position, while false rejects it. If the maximum number of tries was exceeded,
 * the function returns [0, 0, 0], indicating failure.
 * 
 * The function can also return a "corrected" position, which is in turn checked if it's in the area or not, 
 * and rejected if not. This can be used to search for nearby roads positions that will be guaranteed to be 
 * in the area.
 * 
 * Parameters:
 * _this select 0: Area (can be an array like above, marker or trigger)
 * _this select 1: Code to run for correcting/filtering
 * _this select 2: Maximum tries (Default 30)
 * _this select 3: Additional parameter passed to the code (Default 0)
 * 
 * 
 * Example:
 * 
 * Search for a point in water in a given area:
 * [_area, {surfaceIsWater _this}] call FHQ_fnc_findPositionInArea;
 * 
 * Search for road position, only try 10 times:
 * [_area, {
 *     private _roads = _this nearRoads 50;
 *     if (count _roads != 0) exitWith {getPos (_roads select 0)};
 *     false;
 * }, 10] call FHQ_fnc_findPositionInArea;
 * 
 * Search for a position inside an area but not in another marker
 * [_area1, {!([_this, "NotInThisMarker"] call FHQ_fnc_isPointInMarker})] call FHQ_fnc_findPositionInArea;
 */

private _area = param [0, objNull, [objNull, "", []], [4]];
private _code = param [1, {true}, [{}]];
private _tries = param [2, 30];
private _add = param [3, objNull];

private _result = [0, 0, 0];

private _shape = "";
private _center = [0, 0, 0];
private _dimension = [];
private _orientation = 0;

switch (typeName _area) do {
	case "ARRAY": {
		_shape = _area select 0;
        _center = _area select 1;
        _dimension = _area select 2;
        _orientation = _area select 3;
	};
	case "STRING": {
		_shape = markerShape _area;
        _center = getMarkerPos _area;
        _dimension = getMarkerSize _area;
        _orientation = markerDir _area;
	};
	case "OBJECT": {
		private _triggerArea = triggerArea _area;
        if (_triggerArea select 3) then {
			_shape = "RECTANGLE";
        } else {
            _shape = "ELLIPSE";
       	};
        _center = getPos _area;
        _dimension = [_triggerArea select 0, _triggerArea select 1];
        _orientation = _triggerArea select 2;
	};
};

while {_tries > 0} do {
    _tries = _tries - 1;
    
    _result = [_shape, _center, _dimension, _orientation] call FHQ_fnc_getPointInShape;
  
    private _filter = (
         if (isNull _add) then {_result call _code;}
         else {[_result, _add] call _code;});
         
    private _found = false;
    
    if (typeName _filter == "BOOL") then {
        _found = _filter;
    };
    
    if (typeName _filter == "ARRAY") then {
        _result = _filter;
        
	    if ([_result, _shape, _center, _dimension, _orientation] call FHQ_fnc_isPointInShape) then {
            _found = true;
		};
	};
    
    if (_found) exitWith {};
    
    _result = [0, 0, 0];
};

diag_log str _result; 
_result;
    
    