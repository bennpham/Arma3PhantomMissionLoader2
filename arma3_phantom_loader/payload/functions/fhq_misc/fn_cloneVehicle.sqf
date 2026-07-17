/*
 * CLone a given template vehicle at the given position with the given direction. The
 * new vehicle will have exactly the same parameters, cargo, fuel, damage etc as the
 * template. ONLY clones the vehicle, not the driver or occupants.
 *
 * Parameters:
 * _this select 0: template vehicle (OBJECT)
 * _this select 1: position to spawn at (optional, default [0,0,0])
 * _this select 2: direction of spawned vehicle (option, default 0 (NORTH))
 *
 * Returns:
 * The newly created vehicle
 */

params [
	["_template", objNull, [objNull]],
	["_position", [0,0,0], [[]]],
	["_dir", 0, [0]]
];

if (isNull _template) exitWith {"NULL template for cloneVehicle" call BIS_fnc_log};

_className = typeOf _template;
_veh = _className createVehicle _position;
_veh setDir _dir;

// Copy vehicle customization
_custom = [_template] call BIS_fnc_getVehicleCustomization;
_texture = _custom # 0;
_animations = _custom # 1; 
//systemChat format ["_tex = %1, _anim = %2", _texture, _animations];
[_veh, _texture, _animations] call BIS_fnc_initVehicle;

// Copy the inventory
clearWeaponCargoGlobal _veh;
clearMagazineCargoGlobal _veh;
clearBackpackCargoGlobal _veh;
clearItemCargoGlobal _veh;

_cargo = getWeaponCargo _template;
_classes = _cargo select 0;
_counts = _cargo select 1;
{
	_veh addWeaponCargoGlobal [_x, _counts # _forEachIndex];
} forEach _classes;

_cargo = getItemCargo _template;
_classes = _cargo select 0;
_counts = _cargo select 1;
{
	_veh addItemCargoGlobal [_x, _counts # _forEachIndex];
} forEach _classes;

_cargo = getMagazineCargo _template;
_classes = _cargo select 0;
_counts = _cargo select 1;
{
	_veh addMagazineCargoGlobal [_x, _counts # _forEachIndex];
} forEach _classes;

_cargo = getBackpackCargo _template;
_classes = _cargo select 0;
_counts = _cargo select 1;
{
	_veh addBackpackCargoGlobal [_x, _counts # _forEachIndex];
} forEach _classes;

_veh setDamage (getDammage _template);
_veh setFuel (fuel _template);

_veh