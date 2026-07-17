/* Dynamic Spawn selection.
 * 
 * This function forms the core of the dynamic spawning system. This system utilizes Eden layers to define a group
 * pool to be used for dynamic spawning. Each group has an associated cost, and to spawn an area, the user passes
 * in a total cost. Groups spawned deduct their cost from the starting cost, as long as the cost is greater than zero.
 * 
 * To set up dynamic spawning, you can either use automatic mode, or manual mode. Automatic mode will automatically
 * scan the mission for layers called "DynamicSpawn_n", with n between 1 and 20. The layer need not be in the root.
 * Usually, a good idea is to put all of them in a "DynamicSpawn" subfolder, that way, you can hide them all at
 * once. Each group in these layers is considered for dynamic spawning, with a cost of 'n' and a weight of 1/n.
 * 
 * Manual mode allows you full control over the layer names, costs and weights. To set this up, pass an array to
 * FHQ_fnc_setupDynamicLayers. The array contains arrays of the form ["layer name", _cost, _weight].
 * 
 * Calling this function without prior FHQ_fnc_setupDynamicLayers will use automatic mode.
 * 
 * After spawning, use FHQ_fnc_cleanupDynamicSpawn to destroy the template groups. This ill prevent you from further 
 * spawning though. Note that calling FHQ_fnc_setupDynamicLayers will hide and disable the units so they no longer 
 * interact with the mission.
 *  
 * 
 * The function is called as such:
 * [_startScore, _targetArea, _init, _callback, _blackList] call FHQ_fnc_dynamicSpawn;
 * 
 * Parameters:
 * _startScore - Total Score of units to spawn.
 * _targetArea - Area to spawn in. Array of triggers, area markers, or area descriptors.
 * _init - Code called after the group is spawned. The spawned group is passed in as the only parameter.
 * _callback - Code to be called for each group. Return false if you don't want this group to be spawned.
 *             It's score is counted, though. This function can be used to place groups yourself in case you don't 
 *             want the automatic placement. The template group is passed as a paremeter to this function.
 * _blackList - optional blacklisted areas. Same rules as _targetArea
 * 
 * Result: List of all groups spawned this way
 * 
 * This function is server callable only
 */

if (!isServer) exitWith {/* server only */};

private _startScore = param [0, 0, [1]];
private _targetArea = param [1, [], [[]]];
private _init = param [2, {}, [{}]];
private _callback = param [3, {true}, [{}]];
private _blackList = param [4, [], [[]]];
private _spawnedGroups = [];
  
if (isNil "FHQ_dynSpawnGroups") then {
    [] call FHQ_fnc_setupDynamicLayers;
};


private _sumWeights = 0;
{
    _sumWeights = _sumWeights + _x;
} forEach FHQ_dynSpawnWeights;


while {_startScore > 0} do {
    /* Calculate a random number between 0 and the maximum weight, and 
     * keep subtracting until we are below zero */
    private _weight = random _sumWeights;
    private _select = 0;
    
    for "_i" from 0 to count FHQ_dynSpawnWeights do {
        _weight = _weight - (FHQ_dynSpawnWeights select _i);
        _select = _i;
        
        if (_weight <= 0) exitWith {};
    };

	private _score = 0;
    private _selected = FHQ_dynSpawnGroups select _select;	// _selected = [_groupList, _cost, _layer];
    private _groups = _selected select 0;

	if (count _groups != 0) then {
        _score = _selected select 1;
        
        /* Select a random group */
    	private _groupNum = floor random ((count _groups));
        private _theGroup = _groups select _groupNum;

		/* Check the callback */
		if (_theGroup call _callback) then {
            /* Spawn it */
            private _spawnedGroup = [_theGroup, _targetArea, _init, _blackList] call FHQ_fnc_spawnDynamicGroup;
            _spawnedGroups pushBack _spawnedGroup;
            if (_theGroup getVariable ["FHQ_DynSpawnUnique", false]) then {
               	_groups deleteAt _groupNum;
            };
        };
    };  

    _startScore = _startScore - _score;
};

_spawnedGroups;