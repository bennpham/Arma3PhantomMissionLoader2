/* This function checks the playable/Switchable units and returns 
 * the highest ranking, living playable unit
 */

private _soldiers = (if (isMultiplayer) then {playableUnits} else {switchableUnits});
private _highest = objNull;


{
    if (side _x != sideLogic && alive _x && !(_x getVariable ["ACE_isUnconscious", false])) then {
        /* It's an actual player (no zeus or spectator) */
        if (isNull _highest) then {
            /* No previous */
            _highest = _x;
        } else {
            private _rankTable = ["PRIVATE", "CORPORAL", "SERGEANT", "LIEUTENANT", "CAPTAIN", "MAJOR", "COLONEL"];
			private _highestRank = _rankTable find (rank _highest);
            private _thisRank = _rankTable find (rank _x);
            if (_thisRank > _highestRank) then {
                _highest = _x;
            };
        };
	};
} foreach _soldiers;

_highest;
            