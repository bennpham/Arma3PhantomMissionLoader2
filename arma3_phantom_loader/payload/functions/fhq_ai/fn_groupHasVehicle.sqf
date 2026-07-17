/* Check if given group owns a vehicle */
private _group = param [0];

if (({vehicle _x != _x} count units _group) == 0) exitWith {false;};
true;