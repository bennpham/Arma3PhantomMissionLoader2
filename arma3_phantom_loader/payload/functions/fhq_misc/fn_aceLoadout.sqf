/*
** Add ACE Specific items to a unit, based on an abstract class
**
** Parameters:
**   _this select 0: (OBJECT) The unit to add the items to 
**   _this select 1: (STRING) A class name or
**                   (ARRAY) an array of class names
**
** Class name can be one of the following:
** "default" - A basic loadout with a fulton flashlight and ear plugs
** "maptools" - Adds map tools
** "sapper" - Adds a clacker
** "sniper" - Adds range card
** "spotter" - adds the spotting scope
** "vector", "vectorday" - give a Vector 21 and remove potential other binocs
** "flashbang" - give two M84 Stun Grenades
**
** Example of use:
**   Sniper-type unit: [this, ["default", "sniper"]] call FHQ_fnc_aceLoadout;
**   Compassman: [this, ["default", "maptools"]] call FHQ_fnc_aceLoadout;
**   Normal soldier: [this, "default"] call FHQ_fnc_aceLoadout;
*/

params [
	["_unit", objNull],
	"_class"
];
if (!isClass (configFile >> "CfgMods" >> "ace")) exitWith {}; // No ACE loaded

if (_class isEqualType "") then {
	_class = [_class];
};

// Class is an array here no matter what
{
	_varName = format ["FHQ_ACE_Handled_%1", _x];
	// Check if this class was added already
	if (!(_unit getVariable [_varName, false])) then {
		_unit setVariable [_varName, true, true];

		switch (_x) do {

			case "default":	{
				// Fulton Flashlight and ear plugs
				_unit addItem "ACE_Flashlight_MX991";
				_unit addItem "ACE_EarPlugs";
			};
			case "maptools": {
				_unit addItem "ACE_MapTools";
			};
			case "sapper": {
				_unit addItem "ACE_Clacker";
				_unit addItem "ACE_DefusalKit";
			};
			case "sniper": {
				_unit addItem "ACE_RangeCard";
			};
			case "spotter": {
				_unit addItem "ACE_SpottingScope";
			};
			case "autorifleman";
			case "machinegunner";
			case "spare barrel";
			case "barrel":
			{
				_unit addItem "ACE_SpareBarrel";
			};
			case "halo":
			{
				_unit linkItem "ACE_Altimeter";
			};
			case "vector": {
				_binoc = binocular _unit;
				if (!(_binoc isEqualTo "")) then {
					_unit removeWeapon _binoc;
				};
				_unit addWeapon "ACE_Vector";
			};
			case "vectorday": {
				_binoc = binocular _unit;
				if (!(_binoc isEqualTo "")) then {
					_unit removeWeapon _binoc;
				};
				_unit addWeapon "ACE_VectorDay";
			};
			case "flashbang": {
				_unit addMagazine "ACE_M84";
				_unit addMagazine "ACE_M84";
			};
		};
	};
} forEach _class;