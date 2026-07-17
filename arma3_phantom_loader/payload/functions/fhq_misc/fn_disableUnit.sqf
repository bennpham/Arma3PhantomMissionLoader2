/* Disable a unit.
 * The unit's simulation as well as several AI parameters will be disabled. Testing showed
 * that this reduces the server lag substentially if used on far away units.
 * 
 * The second, optional parameter determines whether the unit may continue to receive damage (true, default) or not (false).
 * The third, optional parameter determines whether the unit is hidden (true) or not (false, default)
 */
private _unit = param [0];
private _damage = param [1, false, [true]];
private _hide = param [2, false, [true]];


_unit enableSimulation false; 
[_unit, "ALL"] remoteExec ["disableAI", _unit];
if (!_damage) then {
    _unit allowDamage false;
};
if (_hide) then {
    _unit hideObjectGlobal true;
};