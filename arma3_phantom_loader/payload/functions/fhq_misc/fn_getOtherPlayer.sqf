/* This function tries to find another player character that can work as a 
 * dialog partner for the team leader for player to player interactions.
 *
 */

private _soldiers = (if (isMultiplayer) then {playableUnits} else {switchableUnits});

private _playableUnits = [];
private _playableGroups = [];
{
    if (side _x != sideLogic) then {
        _playableUnits pushBack _x;
        _playableGroups pushBackUnique (group _x);
    };
} forEach _soldiers;

private _notGuy = param [0, call FHQ_fnc_getOpsLeader];
private _otherGroup = param [1, true, [true]];

private _res = objNull;

if (_otherGroup) then {
    {
        if (_x != group _notGuy) then {
            if (count (units _x) != 0) exitWith {
                _res = (units _x) select 0;
            };
        };        
    } foreach _playableGroups;
};

if (isNull _res) then {
    {
        if (_x != _notGuy) exitWith {
            _res = _x;
        };
    } foreach _playableUnits;
};

_res;