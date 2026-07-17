/* File: fn_getRandomPos.sqf
 * Author: Thomas "Varanon" Frieden
 * 
 * Description:
 * Generate a random point somewhere in a list of areas. The area list is given as an array
 * of areas, triggers or markers (or a mixture of those). 
 * Additionally, a list of areas can be passed that will serve as a blacklist.
 * Finally, a piece of code can be passed that can be used to further filter the result.
 * 
 * Filter code is called with the x and y coordinates of the point in question as parameters,
 * and is supposed to return false if the point is to be rejected.
 * 
 * Parameters(s):
 * _this select 0: Whitelist (array)
 * _this select 1: Blacklist (array)
 * _this select 2: Filter code (code)
 * 
 * Returns:
 * position (array)
 * 
 */

private ["_whitelist", "_blacklist", "_filterCode", "_getShape", "_element", "_pos", "_blackElement"];

_whitelist = [_this, 0, [], [[]]] call BIS_fnc_param;
_blacklist = [_this, 1, [], [[]]] call BIS_fnc_param;
_filterCode = [_this, 2, {true}, [{}]] call BIS_fnc_param;
_result = [];

_getShape = {
  	/* Extract the parameter array */
    if (typename _this == "ARRAY") exitWith {
        _this;
    };
    
	if (typename _this == "STRING") exitWith {
        [markerShape _this, getMarkerPos _this, getMarkerSize _this, markerDir _this];
    };

    /* Assume it's a trigger */    
    private ["_triggerArea", "_shape"];
    _triggerArea = triggerArea _this;

    _shape = "ELLIPSE";
    if ((_triggerArea select 3)) then {
        _shape = "RECTANGLE";
    };
    
    [_shape, getPos _this, [_triggerArea select 0, _triggerArea select 1], _triggerArea select 2];
};

/* we give up after 100 attemtps */
for "_i" from 0 to 99 do { 
    _element = _whitelist call BIS_fnc_selectRandom;

    _pos = (_element call _getShape) call FHQ_fnc_getPointInShape;
    
    {
        /* Check if the point is in any exclude marker, and terminate early if it is */
        _blackElement = _x call _getShape;
        _res = [_pos, _blackElement select 0, _blackElement select 1,
        			_blackElement select 2, _blackElement select 3] call FHQ_fnc_isPointInShape;
        if (_res) exitWith {
            _pos = [];
        };
    } foreach _blacklist;
    
    if (count _pos != 0) then {
        _res = _pos call _filterCode;

        if (typename _res == "BOOL") then {
            if (!_res) exitWith {
                _pos = [];
            };
        } else {
            if (typename _res == "ARRAY") then {
                _pos = _res;
            } else {
                _pos = [];
            };
        };
    };
    
    if (count _pos != 0) exitWith {
       _result = _pos;
    };
};

_result;