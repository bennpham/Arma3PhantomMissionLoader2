/* Warp a group to a new position, keeping the orientation and distances between group members */

private _group = param [0];
private _pos = param [1];

private _vehicles = [];

private _xPos = getPos (vehicle (leader _group));

{
    /* Only if not in a vehicle */
    if (vehicle _x == _x) then {
		private _targetPos = getPos _x vectorDiff _xPos;
		_x setPos (_targetPos vectorAdd _pos);
    } else {
		_vehicles pushBackUnique (vehicle _x);
    };
} foreach units _group;

/* Move vehicles as well */
{
	private _targetPos = getPos _x vectorDiff _xPos;
	_x setPos (_targetPos vectorAdd _pos);
} foreach _vehicles;