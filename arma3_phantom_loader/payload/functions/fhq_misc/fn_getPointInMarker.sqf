/* File: fn_getPointInMarker.sqf
 * Author: Thomas "Varanon" Frieden
 * 
 * Description:
 * Generate a random point somewhere in a given marker. The marker can have
 * any area shape (ellipse or rectangle) and can be rotated
 * 
 * Parameters(s):
 * _this select 0: Marker
 * 
 * Returns:
 * position (array)
 * 
 */
private "_marker";

_marker = [_this, 0, "", ["string"]] call BIS_fnc_param;
_pos = [markerShape _marker, getMarkerPos _marker, getMarkerSize _marker, markerDir _marker] call FHQ_fnc_getPointInShape;

_pos;