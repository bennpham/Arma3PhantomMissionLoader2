/* Find a circle [center, radius] enclosing all given units 
 * Note: This isn't the smalles circle around the units. Calculating the smallest
 * circle is O(n²) and not really a necessity for us.
 * 
 * The simple approach here is to find the lowest and highest x and y coordinates, 
 * and then form a circle enclosing that rectangle
 */

private _minX = (getPos (_this select 0)) select 0;
private _maxX = (getPos (_this select 0)) select 0;
private _minY =	(getPos (_this select 0)) select 1;
private _maxY = (getPos (_this select 0)) select 1;

{
    private _nx = (getPos _x) select 0;
    private _ny = (getPos _x) select 1;
    
    if (_nx < _minX) then {
        _minX = _nx;
    };
    
    if (_nx > _maxX) then {
        _maxX = _nx;
    };
    
    if (_ny < _minY) then {
        _minY = _ny;
    };
    
    if (_ny > _maxY) then {
        _maxY = _ny;
    };
} foreach _this;

private _center = [(_maxX + _minX)/2, (_maxY + _minY)/2, 0];
private _radius = [_maxX, _maxY, 0] distance _center;

[_center, _radius];