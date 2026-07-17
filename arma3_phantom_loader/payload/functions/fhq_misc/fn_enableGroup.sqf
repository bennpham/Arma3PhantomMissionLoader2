private ["_units", "_grp", "_vehicles", "_uavs"];

_grp = [_this, 0] call BIS_fnc_param;

_units = units _grp;
_vehicles = [];
_uavs = [];

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
    [_x] call FHQ_fnc_enableUnit;
} foreach _units + _vehicles + _uavs;