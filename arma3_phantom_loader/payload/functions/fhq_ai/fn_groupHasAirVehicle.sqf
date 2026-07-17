/* Check if given group owns a vehicle */
private _group = param [0];
private _res = false;

{
    private _veh = vehicle _x; 
    if (_veh isKindOf "Air") exitWith {_res = true;};
} foreach units _group;

_res