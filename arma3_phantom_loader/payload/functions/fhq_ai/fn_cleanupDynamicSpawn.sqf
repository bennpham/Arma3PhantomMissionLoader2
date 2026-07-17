/* Delete all template groups involved with dynamic spawning. This will prevent future dynamic spawns */

if (!isServer) exitWith {/*Not on clients */};

if (isNil "FHQ_dynSpawnLayers") then {
    [] call FHQ_fnc_setupDynamicLayers;
};

private _groupList = [];

{
    private _layer = _x select 0;
    private _units = (getMissionLayerEntities _layer) select 0; 
    
    {
        private _group = group _x;
        
        if (!isNull _group) then { 
        	_groupList pushBackUnique _group;
        };
    } foreach _units;
} foreach FHQ_dynSpawnLayers;



{
  	[_x] call FHQ_fnc_deleteGroup;
} foreach _groupList;

FHQ_dynSpawnLayers = nil;
FHQ_dynSpawnGroups = nil;
FHQ_dynSpawnScores = nil;
FHQ_dynSpawnWeights = nil;
FHQ_dynSpawnMin = nil;
FHQ_dynSpawnMax = nil;