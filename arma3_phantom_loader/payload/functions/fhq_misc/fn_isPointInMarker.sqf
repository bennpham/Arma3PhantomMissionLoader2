/* File: fn_isPointInMarker.sqf
 * Author: Thomas "Varanon" Frieden
 * 
 * Description:
 * Check if a point is within a given marker
 * 
 * Parameters(s):
 * _this select 0: Point to check (array)
 * _this select 1: Marker to check against (string)
 * 
 * Returns:
 * Boolean
 * 
 */
 
 
 private ["_marker", "_pos"];

_pos = [_this, 0, [0,0,0], [[]], [2,3]] call BIS_fnc_param;
_marker = [_this, 1, "", ["string"]] call BIS_fnc_param;

_res = [_pos, markerShape _marker, getMarkerPos _marker, markerSize _marker, markerDir _marker] call FHQ_fnc_isPointInShape;

_res;