/*
 * Send a speech sample from sender to recipicient with proper locality set up.
 * 
 * Params:
 * _this select 0: Speaker : Object
 * _this select 1: Receipicient : Object
 * _this select 2: sentenceID : String
 * _this select 3: (optional) .bikb topic (default: speech.bikb) : String
 * _this select 4: (optional) Force radio (default: true) : Boolean, Number, or String
 *     true/false to force radio or not, Number 1-10 for custom radio channel, string for
 *	   specific radio channel "GLOBAL", "SIDE", "GROUP", "VEHCILE", "DIRECT", "COMMAND"
 *
 */

params [
	["_speaker", objNull, [objNull]],
	["_listener", objNull, [objNull]],
	["_sentence", "", [""]],
	["_topic", "speech", [""]],
	["_forceRadio", true, [true,0,""]]
];

if (isNull _speaker || isNull _listener) exitWith {};
if (_sentence == "") exitWith {};

//[_speaker, [_listener, _topic, _sentence, "", {}, "", [], _forceRadio]] remoteExec ["kbTell", _speaker];
//[_speaker, [_listener, _topic, _sentence, ["",{},"",[]],_forceRadio]] remoteExec ["kbTell", _speaker];
[_speaker, [_listener, _topic, _sentence, ["",{},"",[]],_forceRadio]] remoteExec ["FHQ_fnc_kbTellST"];