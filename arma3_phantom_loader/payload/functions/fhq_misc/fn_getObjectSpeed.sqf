/* Get the speed of an object in m/s
 * 
 * Parameters:
 *   _obj The object
 * Returns:
 *    Speed in m/s
 */

if (isNull _this) exitWith {0};

private _velocity = velocity _this;
private _speed = vectorMagnitude _velocity; //sqrt((_velocity select 0)*(_velocity select 0) + (_velocity select 1)*(_velocity select 1) + (_velocity select 2)*(_velocity select 2));

_speed;