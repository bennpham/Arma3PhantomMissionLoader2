/* Spawn a group of vehicles.
 * 
 * Parameters:
 *   _this select 0: Start position
 *   _this select 1: Group's side
 *   _this select 2: List of vehicles
 *   _this select 3: List of positions
 *   _this select 4: direction of spawning
 * 
 * Returns:
 *  The groups
 */

private _pos = _this param [0, [0, 0, 0], [[]], [2,3]];
private _side = _this param [1, sideUnknown, [sideUnknown]];
private _list = _this param [2, [], [[]]];
private _posList = _this param [3, []];
private _az = _this param[4, 0];

private _grps = []; 

private _i = 0;

for "_i" from 0 to ((count _list) - 1) do
{
    private _spawnPos = _pos vectorAdd (_posList select _i);
    private _vehicle = _list select _i;
    if ((typename _vehicle) == "STRING") then {
        private _grp = createGroup _side;
        [_spawnPos, _az, _list select _i, _grp, true] call BIS_fnc_spawnVehicle;

        _grps = _grps + [_grp];
    } else {
        private _grp = group driver _vehicle;
        private _mode = "none";
        if (_vehicle isKindOf "Air") then {
            _spawnPos set [2, 50];
            (driver _vehicle) action ["engineon", _vehicle];
            _mode = "fly";
        };

        _vehicle setVehiclePosition [_spawnPos, [], 0, _mode];
        _vehicle setDir _az;

        _grps = _grps + [_grp];
    };
};

_grps;