/* Create a string for the given date.
 * Date is standard 'date' output, i.e. [year, month, day, hour, minute]
 */

private ["_year", "_day", "_month", "_endString"];
_year = _this select 0;

_day = _this select 2;

_month = ["Unknowinus", "January", "February", "March", "April", "May", "June", "July",
		  "August", "September", "October", "November", "December"] 
 		select (_this select 1);

_endString = "th";
if (_day == 1 || _day == 21 || _day == 31) then
{
    _endString = "st";
};

if (_day == 2 || _day == 22) then
{
    _endString = "nd";
};


_dateString = format["%1 %2%3, %4", _month, _day, _endString, _year];

_dateString;