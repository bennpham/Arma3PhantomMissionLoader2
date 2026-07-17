/* Find the first leader in a list of groups. In essence, it returns the leader of the 
 * first group that still has alive members.
 */
 
private "_res";

_res = objNull;
{
    private "_leader";
    _leader = leader _x;
    if (!isNull _leader) exitwith {_res = _leader;}
} foreach _this;

_res;