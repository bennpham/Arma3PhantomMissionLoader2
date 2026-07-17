/*
 * Returns an array of units that are in a trigger, counting vehicle cargo
 * 
 * _this select 0: (Object) Trigger name
 * _this select 1: (Boolean Optional) if true, filter for playable units
 */
 
private ["_res", "_trigger", "_filter", "_playable"];
    
_trigger = [_this, 0, objNull, [objNull]] call BIS_fnc_param;
_filter = [_this, 1, false, [false]] call BIS_fnc_param;
_playable = (if (isMultiplayer) then {playableUnits} else {switchableUnits});

_res = [];
{
    if ((vehicle _x) inArea _trigger) then {
        if (_filter) then {
            if (_x in _playable and side _x != sideLogic) then {
                _res pushBack _x;
            };
        } else {
            _res pushBack _x;
        };
    };
} forEach allUnits;
    
_res
