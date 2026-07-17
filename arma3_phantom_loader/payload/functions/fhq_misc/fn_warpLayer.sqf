/* Warp a layer to a given position
 * Moves all objects and markers, keeping their relative position intact
 * 
 * Parameters:
 * _this select 0: Layer Name
 * _this select 1: position
 * _this select 2: Boolean, allow damage, defaults to true;
 */

private _layer = param [0];
private _pos = param [1];
private _damage = param [2, true];
private _layerObjs = (getMissionLayerEntities _layer) select 0;
private _layerMarkers = (getMissionLayerEntities _layer) select 1;

private _refPos = getPos (_layerObjs select 0);
{
	private _targetPos = getPos _x vectorDiff _refPos;
	_targetPos = _targetPos vectorAdd _pos;
	_targetPos set [2, 0]; 
	
    if (vehicle _x == _x) then {
		_x setPos _targetPos;
	};
    
    _x allowDamage _damage;
} foreach _layerObjs;

{
	private _targetPos = getMarkerPos _x vectorDiff _refPos;
	_targetPos = _targetPos vectorAdd _pos;
	_targetPos set [2, 0]; 

	_x setMarkerPos _targetPos;        
} foreach _layerMarkers;