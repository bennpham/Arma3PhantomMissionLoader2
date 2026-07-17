params [
	["_stringList", [], [[]]],
	["_timeToShow", 8, [0]]
];

private _numMainStrings = (count _stringList)-1;

private _camera = "camera" camCreate [0,0,2];
_camera camPrepareTarget [-50419.49,-4203.23,86250.00];
_camera camCommitPrepared 0;
_camera cameraEffect ["internal", "BACK"];

100011 cutrsc ["RscQuoteTextDialog", "BLACK"];
sleep 1;
waitUntil {
	!isNil {uinamespace getvariable "fhq_RscQuoteTextDialog"};
};


disableSerialization;

private _display = uinamespace getvariable "fhq_RscQuoteTextDialog";
_display displayAddEventHandler ["unload", {uinamespace setVariable ["fhq_RscQuoteTextDialog", objNull];}];

// Set up in the middle of the screen
private _centerX = safeZoneX + 0.5*safeZoneW;
private _centerY = safeZoneY + 0.5*safeZoneH;
private _leftEdge = safeZoneX + 0.1 * (safeZoneX + safeZoneH);
private _topEdge = _centerY - 0.9*_centerY;
private _height = (safeZoneY + safeZoneH) / 20;

private _largest = 0;

private _missionDisplay = call BIS_fnc_displayMission;
private _skipEH = _missionDisplay displayAddEventHandler [
    "KeyDown",
    {
        private _res = false;
        if (_this select 1 == 57) then {
            (call BIS_fnc_displayMission) displayRemoveEventHandler [	
            	"KeyDown", 
                uiNameSpace getVariable "FHQ_Quote_SkipEH"
            ];
            uiNameSpace setVariable ["FHQ_Quote_SkipEH", nil];
            playSound ["click", true];
            uiNameSpace setVariable ["fhq_quote_break", true];
            _res = true; 
        };
        _res
    }
];
uiNameSpace setVariable ["FHQ_Quote_SkipEH", _skipEH];

for "_i" from 0 to _numMainStrings-1 do {
	_id = _display ctrlCreate ["RscStructuredText",1001+_i];
	_id ctrlSetFade 1; 
	_id ctrlCommit 0;

	_id ctrlSetPosition [_leftEdge,_topEdge, safeZoneX+safeZoneW,_height];
	_id ctrlSetBackgroundColor [0, 0, 0, 1];

	_id ctrlSetStructuredText parseText  ("<t size=""1.5"">" +  (_stringList select _i) + "</t>");
	
	_id ctrlCommit 0;

	_w = ctrlTextWidth _id;
	if (_largest < _w) then {
		_largest = _w;
	};
	_topEdge = _topEdge + _height;
};

for "_i" from 0 to _numMainStrings-1 do {
	_id = _display displayCtrl 1001+_i;
	_pos = ctrlPosition _id;
	_pos set [0, _centerX - _largest/2];

	_id ctrlSetPosition _pos;
	_id ctrlCommit 0;

	_id ctrlSetFade 0;
	_id ctrlCommit 2;

	sleep 0.7;
};

// Source line
topEdge = _topEdge + _height;
_source = _stringList select _numMainStrings;
_id = _display ctrlCreate ["RscStructuredText",10000];
_id ctrlSetFade 1; 
_id ctrlCommit 0;

_id ctrlSetPosition [_leftEdge,_topEdge, safeZoneX+safeZoneW,_height];
_id ctrlSetBackgroundColor [0, 0, 0, 1];

_id ctrlSetStructuredText parseText  ("<t size=""1.5"" color=""#ff7700"">" +  (_stringList select _numMainStrings) + "</t>");
_id ctrlCommit 0;
_w = ctrlTextWidth _id;
_newX = (_centerX + _largest/2) - _w;
_id ctrlSetPosition [_newX,_topEdge, safeZoneX+safeZoneW,_height];
_id ctrlCommit 0;

_id ctrlSetFade 0;
sleep 2;
_id ctrlCommit 2;

//sleep _timeToShow;
private _startTime = time;
while {_startTime + _timeToShow + 4 > time} do {
    
    if (!isNil {uiNameSpace getVariable "fhq_quote_break"}) exitWith {
		uiNameSpace setVariable ["fhq_quote_break", nil];
	};
    sleep 0.5; 
    
};

// Fade out all of them
for "_i" from 0 to _numMainStrings-1 do {
	_id = _display displayCtrl 1001+_i;

	_id ctrlSetFade 1;
	_id ctrlCommit 2;

	sleep 0.5;
};

_id = _display displayCtrl 10000;

_id ctrlSetFade 1;
_id ctrlCommit 2;


sleep 3;


_camera cameraEffect ["Terminate", "BACK"];
sleep 1;
100011 cutfadeout 0;