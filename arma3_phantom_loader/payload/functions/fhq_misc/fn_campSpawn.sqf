
params [
	[ "_camp", [] ],
	[ "_pos", [] ],
	[ "_dir", 0 ]
];

private _objects = [];
private _sin = sin (-1 * _dir);
private _cos = cos (-1 * _dir);
diag_log format["_pos = %1, _dir = %2", _pos, _dir];


/* Handle all empty objects, minus people and vehicles with people inside */
{
	/* Each entry is [_class, _disp, _up, _dir, _simulation, _damage, 
	 *	_itemCargo, _weaponCargo, _backpackCargo, _magazineCargo, 
	 *	_ammoCargo, _fuelCargo, _repairCargo];
	 */
	_x params ["_class", "_disp", "_up", "_dirV", "_simulation", "_damage", "_lock",
			"_itemCargo", "_weaponCargo", "_backpackCargo", "_magazineCargo",
			"_ammoCargo", "_fuelCargo", "_repairCargo", "_skins", "_anims"];

	private _posE = [(_pos select 0) + _cos * (_disp select 0) - _sin * (_disp select 1),
					 (_pos select 1) + _sin * (_disp select 0) + _cos * (_disp select 1),
					 (_pos select 2) +        (_disp select 2)];

	private _entity = createVehicle [_class, [0, 0, 100]];
	if (_entity isKindOf "allVehicles") then {
		_posE set [2, (_posE select 2) + 0.5];
	};

	_entity enableSimulation false;
	_entity allowDamage false;
	_entity setVectorUp _up;
	_entity setDir (_dirV + _dir);
	_entity setPos _posE;

	{
		_entity setObjectTexture[_foreachIndex, _x];
	} foreach _skins;
	{
		_entity animateSource [_x select 0, _x select 1];
	} foreach _anims;
	

	if (_lock != -1) then {
		_entity lock _lock;
	};

	if (count _itemCargo != 0) then {
		clearItemCargoGlobal _entity;

		{
			private _item = _x;
			private _count = (_itemCargo select 1) select _forEachIndex;
			_entity addItemCargoGlobal [_item, _count];
		} foreach (_itemCargo select 0)
	};

	if (count _weaponCargo != 0) then {
		clearWeaponCargoGlobal _entity;

		{
			private _item = _x;
			private _count = (_weaponCargo select 1) select _forEachIndex;
			_entity addWeaponCargoGlobal [_item, _count];
		} foreach (_weaponCargo select 0)
	};

	if (count _backpackCargo != 0) then {
		clearBackpackCargoGlobal _entity;

		{
			private _item = _x;
			private _count = (_backpackCargo select 1) select _forEachIndex;
			_entity addBackpackCargoGlobal [_item, _count];
		} foreach (_backpackCargo select 0)
	};

	if (count _magazineCargo != 0) then {
		clearMagazineCargoGlobal _entity;

		{
			private _item = _x;
			private _count = (_magazineCargo select 1) select _forEachIndex;
			_entity addMagazineCargoGlobal [_item, _count];
		} foreach (_magazineCargo select 0)
	};

	if (_ammoCargo != -1) then {
		_entity setAmmoCargo _ammoCargo;
	};

	if (_fuelCargo != -1) then {
		_entity setFuelCargo _fuelCargo;
	};

	if (_repairCargo != -1) then {
		_entity setRepairCargo _repairCargo;
	};

	_objects pushBack [_entity, _simulation, _damage];
} foreach (_camp select 2);


/* Now, the rest, groups, units, and vehicles with units in them.
 * The array has different layouts depending on the first entry:
 * Groups: ["GROUP", _side, _combatMode, _formation, _speed, _waypoints]
 * Vehicles: ["VEHICLE", _class, _disp, _up, _dir, _simulation, _damage, 
 *				 _itemCargo, _weaponCargo, _backpackCargo, _magazineCargo, 
 *				_ammoCargo, _fuelCargo, _repairCargo, _crewMembers]
 * Units: ["UNIT", _class, _disp, _up, _dir, _simulation, _damage, _loadout, _behaviour]
 *
 * For groups, the _waypoints parameter is another array of the following form:
 * [_type, _behaviour, _combatMode, _position, _speed, _timeout, _type, (optional)_statement]
 * and likewise, for vehicles, the _crewMembers is an array of the following form:
 * [_class, _loadout, _role, _cargoindex, _turretpath, _manturret, _behaviour]
 */
private _currentGrp = grpNull;
private _allGroups = [];
{
	private _type = _x select 0;


	if (_type == "GROUP") then {
		_x params ["_dummy", "_side", "_combatMode", "_formation", "_speed", "_waypoints"];
		private ["_realSide"];
		private ["_i"];
	
		

		switch (tolower _side) do {
			case "west": {_realSide = west;};
			case "east": {_realSide = east;};
			case "civ": {_realSide = civilian;};
			case "guer": {_realSide = resistance;};
		};

		_currentGrp = createGroup _realSide;
		_currentGrp setCombatMode _combatMode;
		_currentGrp setFormation _formation;
		_currentGrp setSpeedMode _speed;

		if (count _waypoints <= 1) then {
			_allGroups pushBack _currentGrp;
		};

		for [{_i = 0}, {_i < count _waypoints}, {_i = _i + 1}] do {
			private _entry = _waypoints select _i;
			private ["_statement"];

			_entry params ["_type", "_behaviour", "_combatMode", "_disp", "_speed", "_timeout"];

			if (count _entry == 7) then {
				_statement = _entry select 6;
			} else {
				_statement = ["true", ""];
			};

			private _wpPos = [(_pos select 0) + _cos * (_disp select 0) - _sin * (_disp select 1),
				 			  (_pos select 1) + _sin * (_disp select 0) + _cos * (_disp select 1),
							  (_pos select 2) +        (_disp select 2)];

			private _wp = _currentGrp addWaypoint [_wpPos, 0];
			_wp setWaypointType _type;
			_wp setWaypointBehaviour _behaviour;
			_wp setWaypointCombatMode _combatMode;
			_wp setWaypointSpeed _speed;
			_wp setWaypointTimeout _timeout;
			_wp setWaypointStatements _statement;
		};
	};

	if (_type == "VEHICLE") then {
		_x params ["_dummy", "_class", "_disp", "_up", "_dirV", "_simulation", "_damage", "_lock",
 				"_itemCargo", "_weaponCargo", "_backpackCargo", "_magazineCargo", 
 				"_ammoCargo", "_fuelCargo", "_repairCargo", "_crewMembers", "_skins", "_anims"];

		private _entity = createVehicle [_class, [0, 0, 0]];
		private _posE = [(_pos select 0) + _cos * (_disp select 0) - _sin * (_disp select 1),
						 (_pos select 1) + _sin * (_disp select 0) + _cos * (_disp select 1),
						 (_pos select 2) +        (_disp select 2)];
		_entity enableSimulation false;
		_entity allowDamage false;
		_entity setVectorUp _up;
		_entity setDir (_dirV + _dir);
		//_entity setVehiclePosition [_posE, [], -1, "CAN_COLLIDE"];
		_entity setPos [_posE select 0, _posE select 1, (_posE select 2) +  1 ];

		{
			_entity setObjectTexture[_foreachIndex, _x];
		} foreach _skins;
		{
			_entity animateSource [_x select 0, _x select 1];
		} foreach _anims;

		if (_lock != -1) then {
			_entity lock _lock;
		};

		if (count _itemCargo != 0) then {
			clearItemCargoGlobal _entity;
			{
				private _item = _x;
				private _count = (_itemCargo select 1) select _forEachIndex;
				_entity addItemCargoGlobal [_item, _count];
			} foreach (_itemCargo select 0)
		};

		if (count _weaponCargo != 0) then {
			clearWeaponCargoGlobal _entity;
			{
				private _item = _x;
				private _count = (_weaponCargo select 1) select _forEachIndex;
				_entity addWeaponCargoGlobal [_item, _count];
			} foreach (_weaponCargo select 0)
		};

		if (count _backpackCargo != 0) then {
			clearBackpackCargoGlobal _entity;
			{
				private _item = _x;
				private _count = (_backpackCargo select 1) select _forEachIndex;
				_entity addBackpackCargoGlobal [_item, _count];
			} foreach (_backpackCargo select 0)
		};

		if (count _magazineCargo != 0) then {
			clearMagazineCargoGlobal _entity;
			{
				private _item = _x;
				private _count = (_magazineCargo select 1) select _forEachIndex;
				_entity addMagazineCargoGlobal [_item, _count];
			} foreach (_magazineCargo select 0)
		};

		if (_ammoCargo != -1) then {
			_entity setAmmoCargo _ammoCargo;
		};

		if (_fuelCargo != -1) then {
			_entity setFuelCargo _fuelCargo;
		};

		if (_repairCargo != -1) then {
			_entity setRepairCargo _repairCargo;
		};

		_objects pushBack [_entity, _simulation, _damage];

		{
			_x params ["_class", "_loadout", "_role", "_cargoindex", "_turretpath", "_manturret", "_behaviour", "_stopped"];

			private _unit = _currentGrp createUnit [_class, [0, 0, 0], [], 0, "NONE"];
			_unit setUnitLoadout _loadout;

			switch (tolower _role) do {
				case "driver": {_unit moveInDriver _entity; _unit assignAsDriver _entity;};
				case "commander": {_unit moveInCommander _entity; _unit moveInCommander _entity;};
				case "gunner": {_unit moveInGunner _entity; _unit assignAsGunner _entity;};
				case "turret": {_unit moveInTurret [_entity, _turretpath]; _unit assignAsTurret [_entity, _turretpath];};
				case "cargo": {_unit moveInCargo [_entity, _cargoindex]; _unit assignAsCargoIndex [_entity, _cargoindex];};
			};

			_unit setBehaviour _behaviour;
		} foreach _crewMembers;
	};

	if (_type == "UNIT") then {
		_x params ["_dummy", "_class", "_disp", "_up", "_dirV", "_simulation", "_damage", "_loadout", "_behaviour", "_stopped"];

		private _entity = _currentGrp createUnit [_class, [0, 0, 0], [], 0, "CAN_COLLIDE"];
		private _posE = [(_pos select 0) + _cos * (_disp select 0) - _sin * (_disp select 1),
						 (_pos select 1) + _sin * (_disp select 0) + _cos * (_disp select 1),
						 (_pos select 2) +        (_disp select 2)];
		_entity enableSimulation false;
		_entity allowDamage false;
		_entity setVectorUp _up;
		_entity setDir (_dirV + _dir);
//		_entity setVehiclePosition [_posE, [], -1, "CAN_COLLIDE"];
		_entity setPos _posE;

		_entity setUnitLoadout _loadout;
		_entity setBehaviour _behaviour;

		_objects pushBack [_entity, _simulation, _damage];
	};

} foreach (_camp select 3);

/* Markers
 * Markers are stored in a seprate array in the following format:
 * [_markerName, _alpha, _brush, _color, _dir, _pos, _shape, _size, _text, _type]
 */
{
	_x params ["_markerName", "_alpha", "_brush", "_color", "_dirV", "_disp", 
			   "_shape", "_size", "_text", "_type"];

	private _num = 1;
	while {!(markerPos format ["%1_%2", _markerName, _num] isEqualTo [0, 0, 0])} do {
		_num = _num + 1;
	};

	private _posE = [(_pos select 0) + _cos * (_disp select 0) - _sin * (_disp select 1),
					 (_pos select 1) + _sin * (_disp select 0) + _cos * (_disp select 1),
					 (_pos select 2) +        (_disp select 2)];

	private _mrk = createMarker [format["%1_%2", _markerName, _num], _posE];
	_mrk setMarkerShape _shape;
	_mrk setMarkerType _type;
	_mrk setMarkerBrush _brush;
	_mrk setMarkerColor _color;
	_mrk setMarkerSize _size;
	_mrk setMarkerText _text;
	_mrk setMarkerAlpha _alpha;

	if (tolower(_shape) == "icon") then {
		_mrk setMarkerDir _dirV;
	} else {
		_mrk setMarkerDir _dir + _dirV;
	};
} foreach (_camp select 4);

/* Make all groups without waypoints stop */
{
	dostop units _x;
} foreach _allGroups;

/* Allow damage and simulation */
[_objects] spawn {
	params ["_objects"];

	{
		(_x select 0) enableSimulation (_x select 1);
	} foreach _objects;

	sleep 3;

	{
		(_x select 0) allowDamage (_x select 2);
	} foreach _objects;
};