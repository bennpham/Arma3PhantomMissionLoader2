/* Dynamic spawn layer setup
 * This function can be called prior to FHQ_fnc_dynamicSpawn to set up mission layers and associated costs.
 * 
 * Input to this function is an array of arrays. Each entry in the array is an array of two further entries,
 * a layer name (string) and a layer cost. Entries are not validated.
 * 
 * If called without parameters, assumes [["DynamicSpawn_x", x, 1/x]...] for x = 1 to 10
 * 
 * Call only on the server
 * 
 * Use in Eden:
 * Create a set of layers (names and parent don't matter), and fill them with groups. Each group has an associated
 * cost given by the parameters to this function.
 * Each group within the layer can have some variables defined on them to control further behavior:
 * - FHQ_DynSpawnUnique: This group can only be spawned once and will be removed if chosen
 * - FHQ_DynSpawnRoad: If true, will be spawned on road, elsewhere otherwise. Note that any ground vehicle
 *                     is implicitly spawned on roads, use this to override
 */

if (!isServer) exitWith {/* Server execution only */};

FHQ_dynSpawnLayers = [];
FHQ_dynSpawnGroups = [];
FHQ_dynSpawnScores = [];
FHQ_dynSpawnWeights = [];
FHQ_dynSpawnMin = 1000;
FHQ_dynSpawnMax = 0;

/* Check if objNull or empty array and generate default in this case */
if (count _this == 0) then {
    for "_i" from 1 to 20 do {
        private _name = format ["DynamicSpawn_%1", _i];

        if ((count getMissionLayerEntities _name) != 0) then {
            FHQ_dynSpawnLayers pushBack [_name, _i, 1/_i];
        };
    };
} else {
    FHQ_dynSpawnLayers = _this;
};

            

/* Go through the layers and find all groups for the appropriate layer. Unfortunately, the
 * function doesn't return groups, only entities within the layer.
 * 
 * We create a list of arrays. The first element is an array of groups within the layer, the second
 * is an associated cost. Third is layer name for later reference. 
 * Basically, this transforms the layer entities into groups.
 */

{
    private _layer = _x select 0;
    private _cost = _x select 1;
    private _weight = _x select 2;
    
    private _groupList = [];
    private _units = (getMissionLayerEntities _layer) select 0; 
    
    if (_cost < FHQ_dynSpawnMin) then {
        FHQ_dynSpawnMin = _cost;
    };
    
    if (_cost > FHQ_dynSpawnMax) then {
        FHQ_dynSpawnMax = _cost;
    };
    
    {
        private _group = group _x;
        
        if (!isNull _group) then { 
        	_groupList pushBackUnique _group;
        };

    } foreach _units;
    
    FHQ_dynSpawnGroups pushBack [_groupList, _cost, _layer];
    FHQ_dynSpawnScores pushBack _cost;
    FHQ_dynSpawnWeights pushBack _weight;
} foreach FHQ_dynSpawnLayers;

/* Disable and hide */
{
    {
    	[_x, false, true] call FHQ_fnc_disableGroup;
    } foreach (_x select 0);
} foreach FHQ_dynSpawnGroups;