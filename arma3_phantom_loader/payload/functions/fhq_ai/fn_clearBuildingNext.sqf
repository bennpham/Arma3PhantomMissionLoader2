private _group = _this select 0;
private _origGroup = (leader _group) getVariable "FHQ_clearBuilding_original";
private _logic = (leader _group) getVariable "FHQ_clearBuilding_logic";
private _origLeader = leader _origGroup;

waitUntil { !(_logic getVariable "FHQ_clearBuilding_lock") };

_logic setVariable ["FHQ_clearBuilding_lock", true];
_buildingPos = _logic getVariable "FHQ_clearBuilding_positions";

if ((count _buildingPos) == 0) then {
	// Building is done, merge back to leader
	_logic setVariable ["FHQ_clearBuilding_lock", false];
	units _group joinSilent _origGroup;
} else {
	_newPos = _buildingPos select 0;
	_buildingPos deleteAt 0;
	_logic setVariable ["FHQ_clearBuilding_positions", _buildingPos];
	_logic setVariable ["FHQ_clearBuilding_lock", false];

	_wp = _group addWaypoint [_newPos, 1.8];
	_wp setWaypointType "MOVE";
	_wp setWaypointCombatMode "YELLOW";
	_wp setWaypointStatements ["true", "[group this] spawn FHQ_fnc_ClearBuildingNext;"];
};