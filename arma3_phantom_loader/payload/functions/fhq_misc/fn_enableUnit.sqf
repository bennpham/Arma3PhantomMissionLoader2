/* Enable a unit.
 * Re-Enable a unit that has been previously disabled with FHQ_fnc_disableUnit;
 */
private "_unit";

_unit = [_this, 0] call BIS_fnc_param;

_unit enableSimulationGlobal true; 
[_unit, "ALL"] remoteExec ["enableAI", _unit];
_unit hideObjectGlobal false;
_unit allowDamage true;