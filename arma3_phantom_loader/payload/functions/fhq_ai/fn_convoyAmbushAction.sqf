// Script by Siil
//systemchat "ambush";
_vehicle = (_this select 0);
_grp = group (_this select 0);
_ambushtype = (_this select 0) getVariable ["FHQ_AmbushType", ""];



_vehicle forcespeed 0;
dostop _vehicle;
driver _vehicle enableai "FSM";
_grp setbehaviour "combat";

switch (_ambushtype) do {

    case "tank": {
		_wp = _grp addWaypoint [getpos leader _grp,5];
		_wp setwaypointtype "SAD";
		_grp setcurrentwaypoint _wp;
		
		sleep 10 + (random 20);
		_vehicle forcespeed -1;		
	};
    case "apc": { 
		sleep 2;
		
		_wp = _grp addWaypoint [getpos leader _grp,5];
		_wp setwaypointtype "SAD";
		_grp setcurrentwaypoint _wp;
		
		_troops = (fullCrew [vehicle _vehicle, "cargo"]);

		{
			[_x] orderGetIn false; 
			[_x] allowGetIn false;
			unassignVehicle _x;
			moveout _x;
			sleep 0.2;
		} forEach _troops;
		sleep 10 + random 10;
		
		_vehicle forcespeed -1;
		
	};
	
	case "truck": { 
		sleep 2;
	
		{
			[_x] orderGetIn false; 
			[_x] allowGetIn false;
			unassignVehicle _x;
			moveout _x;
			sleep 0.2;
		} forEach crew _vehicle;
		
	};
	
	 default {

		_wp = _grp addWaypoint [getpos leader _grp,5];
		_wp setwaypointtype "SAD";
		_grp setcurrentwaypoint _wp;
		
		sleep 10 + (random 20);
		_vehicle forcespeed -1;
		
	};
  
};
