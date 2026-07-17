params [
	["_prefix", "SG_", [""]],
	["_alternatePrefix", "", [""]]
];

_array = [];
_count = 0;
_running = true;
while {_running} do 
{
	_entities = (getMissionLayerEntities format ["%2%1", _count, _prefix]) select 0;
	if (isNil "_entities" && _alternatePrefix != "") then
	{
		// Try the alternative layer name
		_entities = (getMissionLayerEntities format ["%2%1", _count, _alternatePrefix]) select 0;
	};

	_spawnables = [];
	if (!isNil "_entities") then 
	{
		{
			if (_x isKindOf "CAManBase") then 
			{
				// Get the group and uniquely add it to the spawnables
				_grp = group _x;
				_spawnables pushBackUnique _grp;
				_x enableSimulation false;
				hideObject _x;
			}
			else
			{
				// Empty vehicle?
				if (isNull (driver _x)) then 
				{
					// Ignore vehicles with drivers, they belong to a group.
					_spawnables pushBack _x;
				};
			};
		} forEach _entities;
	}
	else
	{
		_running = false;
	};

	_array pushBack _spawnables;

	_count = _count + 1;
};

_array