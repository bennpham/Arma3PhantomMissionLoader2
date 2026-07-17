/* Delete all units and vehicles in a group */
private _grp = param [0, grpNull, [grpNull]];


/* Find the actual vehicle this group come in */
private _vehiclesInGroup = [];
{
	if (!(vehicle _x in _vehiclesInGroup)) then {
    	_vehiclesInGroup = _vehiclesInGroup + [vehicle _x];
	};
} foreach units _grp;

{
    deleteVehicle _x;
} foreach units _grp;

{
    deleteVehicle _x;
} foreach _vehiclesInGroup;
    