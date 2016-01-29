# proj3-ajax  (or proj4)

Name: Alexander Owen  
URL: http://ix.cs.uoregon.edu/~aowen/htbin/cis399/proj3-ajax/  
http://ix.cs.uoregon.edu:6938    

RUSA ACP Brevet Time Calculator  
Gives the open and closing times based on brevet length and time. Follows the ACP brevet algorithm described at: http://www.rusa.org/octime_alg.html    

## Algorithm  
Determining the open and closing time of a control on a brevet follows either one of two special cases or 1 general case.    

Special case:  
1) If the control is zero, then the open time is the start time, and the closing time is the start time plus 1 hour. 
2) If the control distance is greater than or equal to the brevet length, the open time is treated as though it were the brevet length and the general
ACP algorithm is performed. The close time follows the maximum time for a brevet, following Article 9 found here: http://www.rusa.org/brvreg.html  
Notice that if the control1 and control2 are both greater than the brevet length, then the open and closing times for both will be the same.    

General case:
For most cases, the control location follows the ACP brevet algorithm described at: http://www.rusa.org/octime_alg.html  
When determining the duration of a control location, the table is helpful, but misleading.  
For a 150km location on a 200km brevet, opening is 150/34, closing is 150/15.  
However, for a 350km location on a 600km, opening is 200/34 + 150/32, closing is 200/15 + 150/15.  
Put simply, the time allotted for a given control location is accumulated with several calculations, not simply one calculation.    

## Small note on the features implemented  
- A calendar widget is used for easy date selection  
- Dates and times are checked for validity upon submission    

## Possible future features  
- Clear button to clear all fields  
- Update all fields when date, time, or distance units changed

