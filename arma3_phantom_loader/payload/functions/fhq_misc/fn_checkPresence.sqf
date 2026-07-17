/* Check presence of an object depending on current difficulty settings.
 * Assumes that difficulty is the first parameter
 * Example:
 * _null = [this, 2] call FHQ_fnc_checkPresence;
 * Only present when the difficutly is 2+
 * 
 * _null = [this, [0,2]] call FHQ_fnc_checkPresence;
 * only present if difficulty is low or high
 */
 
_object = [_this, 0] call BIS_fnc_param;
_difficulty = [_this, 1] call BIS_fnc_param;
_difficultyLevel = 0;



if (isMultiplayer) then
{
    _difficultyLevel = [_this, 2, (paramsArray select 0)] call BIS_fnc_param;
}
else
{
    _difficultyLevel = [_this, 2, 0] call BIS_fnc_param;
    if (!cadetMode) then
    {
        _difficultyLevel = 1;
    };
};

if (toUpper(typename _difficulty) != "ARRAY") then
{
    /* Normal version, _difficulty is minimum level of spawning */
	if (_difficultyLevel < _difficulty) then
	{
        { if (_x != _object) then {deleteVehicle _x;};} forEach crew _object; 
		deleteVehicle _object;
	};
}
else
{
    /* _difficulty is an array, spawned when current difficulty in list */
	if (!(_difficultyLevel in _difficulty)) then
	{
        { if (_x != _object) then {deleteVehicle _x;};} forEach crew _object;
		deleteVehicle _object;
	};    
};

    	