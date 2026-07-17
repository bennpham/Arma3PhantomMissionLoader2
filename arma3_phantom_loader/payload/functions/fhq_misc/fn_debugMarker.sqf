private _pos = param [0, [0,0,0], [[]], [2,3]];
private _type = param [1, "waypoint", [""]];
private _scale = param [2, 0.5, [0.0]];
private _text = param [3, "", [""]];


_dbg = createMarker [format["debug%1%2", _pos select 0, _pos select 1], _pos];
_dbg setMarkerShape "ICON";
_dbg setMarkerType _type;
_dbg setMarkerSize [_scale, _scale];
_dbg setMarkerText _text;

_dbg;