/* Disable the given group, hiding it if wanted */

private _grp = param [0];
private _damage = param [1, true, [false]];
private _hide = param [2, false, [false]];

private _units = units _grp;
private _vehicles = [];
private _uavs = [];

{
    if (vehicle _x != _x) then {
        if (!(vehicle _x in _vehicles)) then {
            _vehicles = _vehicles + [vehicle _x];
        };
    };
} foreach _units;

{
    if (!isNull getConnectedUAV _x ) then {
        if (!(getConnectedUAV _x in _uavs)) then {
            _uavs = _uavs + [getConnectedUAV _x];
        };
    };
} foreach _units;

{
    [_x, _damage, _hide] call FHQ_fnc_disableUnit;
} foreach _units + _vehicles + _uavs;