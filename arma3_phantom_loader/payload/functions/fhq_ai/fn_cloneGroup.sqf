/* Clone an existing group, and move it to a specified position.
 * 
 * The group's members, their damage, fuel state and loadouts are all copied over to the
 * new group.
 * 
 * Parameters: 
 * _this select 0: The group to clone
 * _this select 1: The position to clone to
 * 
 * Returns:
 * The newly created group
 */

private _tmplGrp = param [0];
private _pos = param [1];

/* Create the actual group */
private _grp = createGroup [side _tmplGrp, true];

/* Find the vehicles owned by them */
private _vehicles = [];


{
    if (vehicle _x != _x) then {
		_vehicles pushBackUnique (vehicle _x);
    };
} foreach units _tmplGrp;

/* Create vehicles first. */
for "_i" from 0 to (count _vehicles) - 1 do
{
  	private _templ = _vehicles select _i;
    private _state = "CAN_COLLIDE";
    
    /* Create empty */
    if (_templ isKindOf "Air") then {
        _state = "FLY";
    };
    
    private _veh = createVehicle [typeof _templ, [-1000 + random 100, -1000 + random 100, 1000 + random 1000], [], 0, _state];
    
    /* Textures */
    {
    	_veh setObjectTextureGlobal [_foreachIndex, _x];
    } foreach getObjectTextures _templ;
    
	/* Todo: Copy cargo */
    /* Todo: Copy animations ? */
    
    /* Fuel and health */
    _veh setFuel (fuel _templ);
    _veh setDamage (damage _templ);

    _templ setVariable ["FHQ_copy", _veh];
};

/* Create units, outfit them, set skill, damage etc */
{
	private _templ = _x;
    private _unit = _grp createUnit	[typeof _templ,  [-1000 + random 100, -1000 + random 100, 1000 + random 1000], [], 0, "CAN_COLLIDE"];
    
    /* Loadout and damage */
    _unit setUnitLoadout (getUnitLoadout _templ);
    _unit setDamage (damage _templ);
    
    /* Skills */
    _unit setSkill ["aimingAccuracy", _templ skill "aimingAccuracy"];
    _unit setSkill ["aimingShake", _templ skill "aimingShake"];
    _unit setSkill ["aimingSpeed", _templ skill "aimingSpeed"];
    _unit setSkill ["endurance", _templ skill "endurance"];
    _unit setSkill ["spotDistance", _templ skill "spotDistance"];
    _unit setSkill ["spotTime", _templ skill "spotTime"];
    _unit setSkill ["courage", _templ skill "courage"];
    _unit setSkill ["reloadSpeed", _templ skill "reloadSpeed"];
    _unit setSkill ["commanding", _templ skill "commanding"];
    _unit setSkill ["general", _templ skill "general"];
    
	/* Record the appropriate unit in a variable so we can access it when determining vehicle positions */
    _templ setVariable ["FHQ_copy", _unit]; 
} foreach units _tmplGrp;

/* All created, move them in their respective vehicle */
{
    private _crew = fullCrew _x;
    private _veh = _x getVariable "FHQ_copy";
    
    {
        private _unit = (_x select 0) getVariable "FHQ_copy";
        diag_log str (_x select 0);
        switch (tolower (_x select 1)) do {
            case "driver": { _unit assignAsDriver _veh; _unit moveInDriver _veh; };
            case "commander": { _unit assignAsCommander _veh; _unit moveInCommander _veh; };
            case "gunner": { _unit assignAsGunner _veh; _unit moveInGunner _veh; };
            case "turret": { _unit moveInTurret[_veh, _x select 3]; };
            case "cargo": { _unit assignAsCargo _veh; _unit moveInCargo [_veh, _x select 2];};
        };                
    } foreach _crew;
} foreach _vehicles;

/* Finally, move the group to their new home */
private _xPos = getPos (vehicle (leader _tmplGrp));

{
    /* Only if not in a vehicle */
    //if (vehicle _x == _x) then {
    if (isNull (objectParent _x)) then {
		private _targetPos = getPos _x vectorDiff _xPos;
	    (_x getVariable "FHQ_copy") setPos (_targetPos vectorAdd _pos); 
    };
} foreach units _tmplGrp;

/* Move vehicles as well */
{
	private _targetPos = getPos _x vectorDiff _xPos;

	if (_x isKindOf "Air") then {
		/* Make sure anything that flies ends up at the height set in the editor */
		(_x getVariable "FHQ_copy") setPos [(_targetPos vectorAdd _pos) select 0, (_targetPos vectorAdd _pos) select 1, (getPos _x) select 2];
	} else {
        if (_x isKindOf "LandVehicle")  then {
            /* Land vehicles are a tricky bunch. They tend to end up in houses if spawned in a densly populated area. We therefore search for an
             * empty position. 
             * Note that this might disrupt the relative positions, but there's little we can do here 
             */
            private _newPos = (_targetPos vectorAdd _pos) findEmptyPosition[0, 100, typeof _x];
            if (count _newPos == 0) then {
                _newPos = (_targetPos vectorAdd _pos);
            };
            (_x getVariable "FHQ_copy") setPos _newPos;
        } else {
			(_x getVariable "FHQ_copy") setPos (_targetPos vectorAdd _pos);
        };
    };
} foreach _vehicles;

/* Add them to the curator interface */
{
	_x addCuratorEditableObjects [units _grp, true];
    _x addCuratorEditableObjects [_vehicles, true];
} forEach allCurators;
_grp;