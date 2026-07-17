/* Update an aspect of the weather effect
 *
 * Parameters:
 *  param [0] - fsm (from FHQ_fnc_weatherEffect)
 *  param [1] - Name (Snow, Fog, Sand, snowInterval, fogInterval, sandInterval)
 *  param [2] - depends on param [1]
 * 
 * Example: Cancel snow
 * [_fsm, "Snow", {false}] call FHQ_fnc_setWeatherEffect;
 * 
 */

/* Note: Variables are global, so _fsm is actually ignored. Reserved for future use */
private _name = param [1];
private _param = param [2, 0, [{true}, 0, []]];

if ((tolower _name) in ["snow", "fog", "sand"]) then {
	_param call compile format ["FHQ_handle%1 = _this;", _name];
};

if ((tolower _name) == "snowInterval") then {
    waitUntil {!isNil "FHQ_Snow"};
	FHQ_Snow setDropInterval _param;
};

if ((tolower _name) == "fogInterval") then {
    waitUntil {!isNil "FHQ_GrndFog"};
	FHQ_GrndFog setDropInterval _param;
};

if ((tolower _name) == "fogSize") then {
    waitUntil {!isNil "FHQ_GrndFog"};
    FHQ_FogParamArray set [11, _param];
    FHQ_GrndFog setParticleParams FHQ_FogParamArray;
};

if ((tolower _name) == "sandInterval") then {
    waitUntil {!isNil "FHQ_Sand"};
	FHQ_Sand setDropInterval _param;
};

if ((tolower _name) == "sandSize") then {
    waitUntil {!isNil "FHQ_Sand"};
    FHQ_SandParamArray set [11, _param];
    FHQ_Sand setParticleParams FHQ_SandParamArray;
};

/*
  [
    ["\A3\data_f\cl_basic.p3d", 1, 0, 1], 
    "", 
	"Billboard", 
	1, 
	10, 
	[0, 0, 0], 
	wind, 
	1,
	1.275,
	1, 
	0,
	[4], 
	[	[1.0 * _fogBrightness, 1.0 * _fogBrightness, 1.0 * _fogBrightness, 0],	[1.0 * _fogBrightness, 1.0 * _fogBrightness, 1.0 * _fogBrightness, 0.04],	[1.0 * _fogBrightness, 1.0 * _fogBrightness, 1.0 * _fogBrightness, 0.02]	],
	[1000], 
                                [["\A3\data_f\cl_basic.p3d", 1, 0, 1], "", 
	"Billboard", 
	1, 
	10, 
	[0, 0, 0], 
	wind, 
	1, 1.275, 1, 0,
	[4], 
	[
		[1.0 * _fogBrightness, 1.0 * _fogBrightness, 1.0 * _fogBrightness, 0],
		[1.0 * _fogBrightness, 1.0 * _fogBrightness, 1.0 * _fogBrightness, 0.04],
		[1.0 * _fogBrightness, 1.0 * _fogBrightness, 1.0 * _fogBrightness, 0.02]
	],
	[1000], 1, 0, "", "", ""];
	1, 
	0, 
	"", 
	"", 
	""];

 */