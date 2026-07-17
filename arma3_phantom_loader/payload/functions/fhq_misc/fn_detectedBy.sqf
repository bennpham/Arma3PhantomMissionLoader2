/* 
** _this select 0: List of units that can be detected
** _this select 1: List of objects that can detect, typically a trigger thisList
**
** returns true if there is at least one detecting
*/
private _detectList = _this select 0;
private _triggerList = _this select 1;

private _knowledge = 0;

{
	private _unit = _x;
	if (alive _unit) then {
		_knowledge = _knowledge + ({(_unit knowsAbout _x) > 0} count _detectList);
	};
} forEach _triggerList;

_knowledge > 0