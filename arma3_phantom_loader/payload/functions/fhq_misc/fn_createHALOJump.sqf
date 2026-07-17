/* Do a halo jump, attach backpack to unit until they are on the ground
 * Based on a script cobra4v320
 * Note that the callbacks run on the machine where the jumping unit is local, so it's
 * clients for players and server or HC for AI.
 * 
 * Parameters:
 * _this select 0: The unit that should jump
 * _this select 1: Position to start the jump (should be high enough, like 2000 m)
 * _this select 2: (Optional, String) Backpack that should be created on the unit. This is usually
 *                 used to give team leaders backpack radios.
 * _this select 3: (Optional, String) An item class name that should be attached to the unit's foot.
 *                 For example, a smoke grenade or chemlight
 * _this select 4: (Optional, String) Piece of code that is executed when chutes open (Parameters: [_unit, _attachedObject])
 * _this select 5: (Optional, String) Piece of code that is executed when unit is on the ground (Parameters: [_unit])
 * _this select 6: (Optional, String) Piece of code that is executed repeatedly until the unit is on the ground (Parameters: [_unit])
 * 
 * Example:
 * 	tf_no_auto_long_range_radio = true;
 * 	{
 *      private _scatter =  [(random 20) - 10, (random 20) - 10, (random 20) - 10];    
 *	    if (_x == leader group _x) then {
 *       	[_x, _startHalo vectorAdd _scatter, "tf_anprc155"] remoteExec ["FHQ_fnc_createHALOJump", _x];
 *   	} else {
 *	    	[_x, _startHalo vectorAdd _scatter] remoteExec ["FHQ_fnc_createHALOJump", _x];
 *	    };
 *	} foreach units FHQ_playerGroup1; 
 */

_this spawn {
	private _unit = param [0];
	private _pos = param [1];
    private _radio = param [2, ""];
	private _item = param [3, ""];
	private _chute = "B_Parachute";
	private _hookChuteOpen = compile param [4, "", [""]];
	private _hookOnGround = compile param [5, "", [""]];
	private _hookEvery10 = compile param [6, "", [""]];
	private _hookValid = param [6, "", [""]];

    private _useTFAR = isclass (configfile >> "CfgPatches" >> "task_force_radio_items");
	private _itemVeh = objNull;

	private _y = -22; 
	private _p = 0; 
	private _r = 0;
    
    private _needSpecialHandling = false;
    if (_useTfar and _unit == leader group _unit) then {
        _needSpecialHandling = true;
    };

	/* If desired, attach an item to the unit's foot */
	if (_item != "") then {
		_itemVeh = _item createVehicle position _unit;
		_itemVeh attachto [_unit, [0, 0.1, 0], "RightShoulder"];
		_itemVeh setVectorDirAndUp [[ sin _y * cos _p,cos _y * cos _p,sin _p], [ [ sin _r,-sin _p,cos _r * cos _p],-_y] call BIS_fnc_rotateVector2D];
	};

	/* If a hook is given for every 10 m callback, create an on frame handler that 
	 * will handle this 
	 */
	private _id = format ["FHQ_Halo_unit_%1", _unit];
	_unit setVariable ["FHQ_EveryCode", _hookEvery10];
	if (_hookValid != "") then {
		[_id, "onEachFrame", {
			private _callMe = (_this select 0) getVariable ["FHQ_EveryCode", {}];
			_this call _callMe;
		}, [_unit]] call BIS_fnc_addStackedEventHandler;
	};

    /* Get the backpack data */	
    if (backpack _unit != "" and backpack _unit != "B_Parachute" or _needSpecialHandling) then { 
    	/* Has a backpack that is not a chute */
        private _unitBackpack = unitBackpack _unit;
    	private _backpackClass = typeOf _unitBackpack;
    	private _items = getItemCargo _unitBackpack;
    	private _weapons = getWeaponCargo _unitBackpack;
    	private _magazines = getMagazineCargo _unitBackpack;

		/* TFAR Override */
        if (_radio != "" && _unit == leader group _unit) then {
        	_backpackClass = _radio;
        };

		/* Add chute */
    	removeBackpackGlobal _unit;
		_unit addBackpackGlobal _chute;
		_unit setPos _pos;

		/* Add empty backpack and attach */
        private _backpackProxy = createVehicle ["groundWeaponHolder", [0,0,10000], [], 0, "NONE"];
        _backpackProxy addBackpackCargoGlobal [_backpackClass, 1];

        if (_backpackClass != "B_Parachute") then {        
        	_backpackProxy attachTo [_unit, [-0.1, 0, -0.65], "pelvis"];
        	_backpackProxy setVectorDirAndUp [[0, -1, 0], [0, 0, -1]];
		};
    
    	if (!isPlayer _unit) then {
            _unit allowDamage false;
        };
        
		/* Let them drop */
        waitUntil {vehicle _unit != _unit};	/* Wait until chute open */
        
		[_unit, _itemVeh] call _hookChuteOpen;

		if (!isPlayer _unit) then {
            vehicle _unit allowDamage false;
        };
        if (_backpackClass != "B_Parachute") then {
        	_backpackProxy attachTo [vehicle _unit, [-0.1, 0.7, 0], "pelvis"]; 
        	_backpackProxy setVectorDirAndUp [[0, 0, -1], [0, 1, 0]];
		};
        
		if (!isNull _itemVeh) then {
			_y = -22; _p = -80; _r = -0;
			_itemVeh attachto [vehicle _unit, [0.2,0,0.67]];
			_itemVeh setVectorDirAndUp [[ sin _y * cos _p,cos _y * cos _p,sin _p], [ [ sin _r,-sin _p,cos _r * cos _p],-_y] call BIS_fnc_rotateVector2D];
		};

        waitUntil {vehicle _unit == _unit}; /* Wait until out of chute */
    
    	if (!isPlayer _unit) then {
            _unit spawn {
                sleep 0.2;
            	_this allowDamage true;
            };
        };
        
    	/* Get rid of the proxy */
        detach _backpackProxy;
        deleteVehicle _backpackProxy;
        
		/* Recreate and refill backpack. Why the heck does get***Cargo have such
         * a bad format ?
         */
        if (_backpackClass != "B_Parachute") then {
			_unit addBackpack _backpackClass;
        	clearAllItemsFromBackpack _unit;
        	
            for "_i" from 0 to count (_items select 0) - 1 do {
	            (unitBackpack _unit) addItemCargoGlobal [(_items select 0) select _i, (_items select 1) select _i];
        	}; 
	        
        	for "_i" from 0 to count (_weapons select 0) - 1 do {
	            (unitBackpack _unit) addWeaponCargoGlobal [(_weapons select 0) select _i, (_weapons select 1) select _i];
        	};
        
	        for "_i" from 0 to count (_magazines select 0) - 1 do {
            	(unitBackpack _unit) addMagazineCargoGlobal [(_magazines select 0) select _i, (_magazines select 1) select _i];
	        };
		};
	} else {
        /* has no backpack, or a chute, simply replace the chute (simpler) */
    	removeBackpackGlobal _unit;
		_unit addBackpackGlobal _chute;
		_unit setPos _pos;
        
        if (!isPlayer _unit) then {
            _unit allowDamage false;
        };
        
		waitUntil {vehicle _unit != _unit};	/* Wait until chute open */

		[_unit, _itemVeh] call _hookChuteOpen;
		
		if (!isNull _itemVeh) then {
			_y = -22; _p = -80; _r = -0;
			_itemVeh attachto [vehicle _unit, [0.2,0,0.67]];
			_itemVeh setVectorDirAndUp [[ sin _y * cos _p,cos _y * cos _p,sin _p], [ [ sin _r,-sin _p,cos _r * cos _p],-_y] call BIS_fnc_rotateVector2D];

		};
		
        waitUntil {vehicle _unit == _unit}; /* Wait until out of chute */

        if (!isPlayer _unit) then {
            _unit spawn {
                sleep 0.2;
            	_this allowDamage true;
            };
        };
   	};

	[_unit] call _hookOnGround;
	
	/* Cleanup */
	if (!isNull _itemVeh) then {
		detach _itemVeh;
	};

	if (_hookValid != "") then {
		[_id, "onEachFrame"] call BIS_fnc_removeStackedEventHandler;
	};

};