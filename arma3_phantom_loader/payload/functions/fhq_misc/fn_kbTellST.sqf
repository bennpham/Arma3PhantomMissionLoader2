if (!canSuspend) exitWith {
	_this spawn FHQ_fnc_kbTellST;
};

_from = _this select 0;
_args = _this select 1;

if (local _from) then {
	_from kbTell _args;
};

if (!hasInterface) exitWith {}; // This will only be run on player clients

// get the receiver
_to = _args select 0;
_shouldSee = true;
if (group _from isEqualTo group _to) then 
{
	// Group radio, must belong to this group
	if (!(group player isEqualTo group _to)) then {_shouldSee = false; };
} else {
	if (side _from isEqualTo side _to) then {
		// Side Radio, must belong to this side
		if (!(side player isEqualTo side _to)) then {_shouldSee = false; };
	};
};

if (!_shouldSee) exitWith {};

// either this is global radio or the above conditions apply, show subtitle
// continue by extracting the text
_sentence = _args select 2;
_text = getText (missionConfigFile >> "Speech" >> "Sentences" >> _sentence >> "text");
_name = name _from;

if ((typeOf _from) isEqualTo "ModuleHQ_F") then {
	_name = _from getVariable "CallsignCustom";
};

showChat false;
[_name, _text] call BIS_fnc_showSubtitle;

_time = time;
waitUntil {clearRadio; time - _time > 0.1; };
showChat true;