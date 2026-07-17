if (!canSuspend) exitWith {_this spawn FHQ_fnc_convoy;};
// Script by Siil
// Modifications by Alwarren

//_time = daytime + ("SpareTime" call BIS_fnc_getParamValue)/60;
//waituntil{daytime >= _time};

// call as
// [vehicle_1, vehicle_2, ..] execVM "scripts\convoy.sqf";

//_convoyarr = []; 
_convoyvararr = _this;
_conwparr =  (_this select 0) getVariable ["FHQ_WaypointArray", []];


_speed = 10; 
_boost = 3;
_targetdist = 30;
_P=2;
_I=0.1;

_countwp = count _conwparr;
_countveh= count _convoyvararr;

{
	driver _x disableAI "FSM";
	_x setVariable ["forcedspeed", 0, false];
	_x forcespeed 0;
	
} forEach _convoyvararr;

sleep 1;

_convoyarr = _convoyvararr;

{_x setdriveonpath _conwparr} foreach _convoyarr;

while {({!alive _x or !canmove _x or damage _x >0.2 or !alive driver _x} count _convoyarr == 0)} do 
{
	{
		_veh_prime=_x;
		_newspeed =0;
		_adjdist = 0;
		
		_veharr = _convoyarr select {(_veh_prime getreldir _x)<90 or (_veh_prime getreldir _x)>270};
		_veharr=[_veharr - [_veh_prime], [], {_veh_prime distance _x }, "ASCEND"] call BIS_fnc_sortBy;
		
		
		if (count _veharr == 0) then {
			_newspeed = _speed;
			//systemchat format ["lead %1 veharr %2",typeof _veh_prime, _veharr];
		} else {
			_veh_front = _veharr select 0;
			_curspeed = _veh_prime getVariable "forcespeed";
			_adjdist = (_veh_prime distance _veh_front)+5;
			_newspeed = _speed - (_targetdist - _adjdist)/2; 
		
			if (_newspeed > _speed+_boost) then 
			{
				_newspeed = _speed+_boost;
			};
			if (_newspeed < 0) then 
			{
				_newspeed = 0;
			};
		};
		
		driver _veh_prime forcespeed _newspeed;
		_veh_prime setVariable ["forcedspeed", _newspeed, false];
		
		sleep 0.1;	
	} foreach _convoyarr;
};

{null = [_x] call FHQ_fnc_convoyAmbushAction;} foreach _convoyarr;
ambushed = 1;

