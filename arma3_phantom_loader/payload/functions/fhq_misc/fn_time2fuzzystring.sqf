/* Convert time into a fuzzy string, like "early morning", or "noon"
 * _this select 0   time
 * _this select 1   prefix
 * _this select 2   suffix
 */ 

private ["_curTime", "_timeString", "_prefix", "_suffix", "_res"];

_curTime = _this select 0;
_prefix = _this select 1;
_suffix = _this select 2;
 
if (_curTime < 4) then
{
    _timeString = "Night";
};
if (_curTime >= 4 && _curTime < 8) then
{
  	_timeString = "Early Morning";  
};
if (_curTime >= 8 && _curTime < 11) then
{
    _timeString = "Morning";
};
if (_curTime >= 11 && _curTime < 14) then
{
  	_timeString = "Noon";  
};
if (_curTime >= 14 && _curTime < 17) then
{
    _timeString = "Afternoon";
};
if (_curTime >= 17 && _curTime < 20) then
{
    _timeString = "Early Evening";
};
if (_curTime >= 20 && _curTime < 23) then
{
    _timeString = "Evening";
};
if (_curTime >= 23) then
{
    _timeString = "Night";
};

_res = format["%1%2%3", _prefix, _timeString, _suffix];

_res;