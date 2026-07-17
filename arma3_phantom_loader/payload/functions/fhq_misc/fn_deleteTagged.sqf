params 
[
	["_tagName", "A", [""]]
];

_varName = format ["FHQ_Tag%1", _tagName];

{
	if (_x getVariable [_varName, false]) then {
		[_x] call FHQ_fnc_deleteGroup;
	};
} forEach allGroups;

{
	if (_x getVariable [_varName, false]) then {
		deleteVehicle _x;
	};
} forEach allUnits;