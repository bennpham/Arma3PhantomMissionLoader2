/* Delete all objects and markers in a layer
 * 
 * Parameters:
 * _this select 0: Layer Name
 */

private _layer = param [0, ""];

{
    deleteVehicle _x;
} foreach ((getMissionLayerEntities _layer) select 0);

{
    deleteMarker _x;
} foreach ((getMissionLayerEntities _layer) select 1);