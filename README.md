Command 1: Takes in the name of the station you want to find and outputs the Station ID and Name of all the relevant stations found using the keyword you provide

Command 2: Outputs the total ridership at each station alomng with the percentage of the ridership from the total ridership


Command 3: Outputs the top 10 busiest stations


Command 4: Outputs the least 10 busiest stations


Command 5: Outputs the stop names as well as other details on the Line you provide the program with


Command 6: Outputs total ridership by month in ascending order and then prompts you if you would like to plot it in a graph


Command 7: Outputs total ridership by year in ascending order and then prompts you if you would like to plot it in a graph


Command 8: Input the year of two stations and outputs the first 5 days and last 5 days of data, and then prompts you if you would like to plot it in a graph


Command 9: Input a line color and the program will output a station names that are a part of that line

DATABASE:

Stations:
- Denotes the stations on the CTA system. A station can have one or more stops, e.g. “Chicago/Franklin” has 2 stops
- Station_ID: primary key, integer
- Station_Name: string

Stops:
- Denotes the stops on the CTA system. For example, “Chicago (Loop-bound)” is one of the
stops at the “Chicago/Franklin” station; a Southbound stop, and handicap-accessible (ADA)
- Stop_ID: primary key, integer
 Station_ID of station this stop is associated with: foreign key, integer
- Stop_Name: string
- Direction: a string that is one of N, E, S, W
- ADA: integer, 1 if the stop is handicap-accessible, 0 if not
- Latitude and Longitude: position, real numbers

Lines:
- Denotes the CTA lines, e.g. “Red” line or “Blue” line
- Line_ID: primary key, integer
- Color: string

StopDetails:
- A stop may be on one or more CTA lines — e.g. “Chicago (Loop-bound)”, stop 30138, is on
the Brown and Purple-Express lines
- One row of StopDetail denotes one unique pair (stop_id, line_id) --- if a stop is on multiple
lines such as “Chicago (Loop-bound)”, it will have multiple StopDetail pairs
- Stop_ID: foreign key, integer
- Line_ID: foreign key, integer
- The pair (Stop_ID, Line_ID) forms a composite primary key

Ridership:
- Denotes how many riders went through the turnstile at this station on this date
- Station_ID: foreign key, integer
- Ride_Date: string in format “yyyy-mm-dd hh:mm:ss.sss”
- Type_of_Day: string, where ‘W’ denotes a weekday, ‘A’ denotes Saturday, and ‘U’ denotes Sunday or Holiday
- Num_Riders: integer, total # of riders who went through the turnstile on this date
- The pair (Station_ID, Ride_Date) forms a composite primary key
