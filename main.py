#
# Hassan Ali Qadir
# This program uses python and sqllite 3 to use the implemented commands and get whatever information you made need from the database


import sqlite3
import matplotlib.pyplot as plt

##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic the stats.
#


## Command for finding a station using the partial station name input by the user
def command_1():
    dbCursor = dbConn.cursor()

    print()
    print("Enter partial station name (wildcards _ and %): ", end='')
    partial_station_name = input()

    #Used this to make the sql command we want to execute
    sql = "Select Station_ID,Station_Name From Stations Where Station_Name like '" + partial_station_name + "' order by Station_Name asc "
    dbCursor.execute(sql)

    row = dbCursor.fetchall()
    if len(row) == 0:
        print("**No stations found...")
        return 0
    else:
        #this prints the Station ID first then the station name from the tuple
        for i in row:
            print(i[0], ":", i[1])

    dbCursor.close()


###################################################################

####Command 2#################
def command_2():
    dbCursor = dbConn.cursor()
    print("** ridership all stations **")
    dbCursor.execute("Select sum(num_riders) From ridership")
    row = dbCursor.fetchone()
    totalrider = row[0]
    dbCursor.execute(
        "Select Station_Name,sum(num_riders) From ridership join Stations on ridership.Station_ID=Stations.Station_ID Group by Station_Name order by Station_Name asc"
    )
    row = dbCursor.fetchall()
    for i in row:
        #this is to make sure the percentage is to 2 decimal places
        percentage_of_ridership = (i[1] / totalrider) * 100
        print(i[0], ":", f"{i[1]:,}", f"({percentage_of_ridership:.2f}%)")

#######################################################################
#########Command 3#################
def command_3():
    dbCursor = dbConn.cursor()
    print("** top-10 stations **")
    dbCursor.execute("Select sum(num_riders) From ridership")
    row = dbCursor.fetchone()
    totalrider = row[0]
    dbCursor.execute(
        "Select Station_Name,sum(num_riders) From ridership join Stations on ridership.Station_ID=Stations.Station_ID Group by Station_Name order by sum(num_riders) desc limit 10"
    )
    row = dbCursor.fetchall()
    for i in row:
        #this is to make sure the percentage is to 2 decimal places
        percentage_of_ridership = (i[1] / totalrider) * 100
        print(i[0], ":", f"{i[1]:,}", f"({percentage_of_ridership:.2f}%)")

###########################################################################
###############Command 4############################
def command_4():
    dbCursor = dbConn.cursor()
    print("** least-10 stations **")
    dbCursor.execute("Select sum(num_riders) From ridership")
    row = dbCursor.fetchone()
    totalrider = row[0]
    dbCursor.execute(
        "Select Station_Name,sum(num_riders) From ridership join Stations on ridership.Station_ID=Stations.Station_ID Group by Station_Name order by sum(num_riders) asc limit 10"
    )
    row = dbCursor.fetchall()
    for i in row:
        #this is to make sure the percentage is to 2 decimal places
        #percentage_of_ridership=str(round((i[1]/totalrider)*100, 2))
        percentage_of_ridership = (i[1] / totalrider) * 100

        print(i[0], ":", f"{i[1]:,}", f"({percentage_of_ridership:.2f}%)")
#########################################################
######################Command 5##########################

def command_5():
    print()
    print("Enter a line color (e.g. Red or Yellow):", end=' ')
    user_color = input()
    dbCursor = dbConn.cursor()
    cmd = "Select Color,Line_ID From Lines where Color like '" + user_color + "'"
    dbCursor.execute(cmd)
    row = dbCursor.fetchall()

    ###if no line was found or not
    if len(row) == 0:
        print("**No such line...")
    else:
        stop_id = str(row[0][1])
        cmd = "Select Stop_Name,Direction,ADA From Stops join StopDetails on StopDetails.Stop_ID=Stops.Stop_ID where Line_ID like '" + stop_id + "' order by Stop_Name asc"
        dbCursor.execute(cmd)
        row = dbCursor.fetchall()
        for i in row:
            print(i[0], ": direction =", i[1], "(accessible?", end=' ')
            if (i[2] == 1):
                print("yes)")
            else:
                print("no)")

#########################################################
######################Command 6##########################

def command_6():
    print("** ridership by month **")
    dbCursor = dbConn.cursor()
    dbCursor.execute(
        "Select strftime('%m',Ride_Date), sum(num_riders) From Ridership group by strftime('%m',Ride_Date) order by strftime('%m',Ride_Date) asc "
    )
    row = dbCursor.fetchall()
    for i in row:
        print(i[0], ":", f"{i[1]:,}")

    ####################################
    #Plotting or not
    print()
    print("plot? (y/n)", end=' ')
    answer = input()
    if (answer == "y"):
        x = []
        y = []
        for i in row:
            x.append(i[0])

            deci = i[1] / (100000000)

            y.append(deci)
        plt.xlabel("month")
        plt.ylabel("number of riders(x*10^8)")
        plt.title("monthly ridership")
        plt.plot(x, y)
        plt.show()


#########################################################
######################Command 7##########################
def command_7():
    print("** ridership by year **")
    dbCursor = dbConn.cursor()
    dbCursor.execute(
        "Select strftime('%Y',Ride_Date), sum(num_riders) From Ridership group by strftime('%Y',Ride_Date) order by strftime('%Y',Ride_Date) asc "
    )
    row = dbCursor.fetchall()
    for i in row:
        print(i[0], ":", f"{i[1]:,}")
    ####################################
    #Plotting
    print()
    print("plot? (y/n)", end=' ')
    answer = input()
    if (answer == "y"):
        x = []
        y = []
        for i in row:
            x.append(i[0][2] + i[0][3])
            deci = i[1] / (100000000)
            y.append(deci)

        plt.xlabel("year")
        plt.ylabel("number of riders(x*10^8)")
        plt.title("yearly ridership")
        plt.plot(x, y)
        plt.show()

#########################################################
######################Command 8##########################



####   Helper function for command 8 ####
def command_8_1(row):
    if len(row) > 1:
        print("**Multiple stations found...")
    else:
        print("**No station found...")


#### Helper function for command 8 #### TO print the dates and ridership ####
def command_8_2(id, year):
    dbCursor = dbConn.cursor()
    cmd = "Select Date(Ride_Date),Num_riders From Ridership where Station_ID like " + str(
        id) + " and strftime('%Y',Ride_Date) like " + str(
            year) + " order by Date(Ride_Date) asc"
    dbCursor.execute(cmd)
    row = dbCursor.fetchall()
    count = 0
    while (count != len(row)):
        print(row[count][0], row[count][1])
        count = count + 1
        if (count == 5):
            count = len(row) - 5
    return row

#### ACtual Command 8 ####
def command_8():
    print()
    print("Year to compare against?", end=' ')
    year_to_c = input()
    print()
    print("Enter station 1 (wildcards _ and %):", end=' ')

    ## First station input
    station_name1 = input()
    dbCursor = dbConn.cursor()
    cmd = "Select Station_ID,Station_Name From Stations where Station_Name like '" + station_name1 + "'"
    dbCursor.execute(cmd)
    row = dbCursor.fetchall()
    if len(row) > 1 or len(row) == 0:
        command_8_1(row)
        return 0
    station_id1 = row[0][0]
    station_name1 = row[0][1]

    ## Second station input
    print()
    print("Enter station 2 (wildcards _ and %):", end=' ')
    station_name2 = input()
    cmd = "Select Station_ID,Station_Name From Stations where Station_Name like '" + station_name2 + "'"
    dbCursor.execute(cmd)
    row = dbCursor.fetchall()
    if len(row) > 1 or len(row) == 0:
        command_8_1(row)
        return 0
    station_id2 = row[0][0]
    station_name2 = row[0][1]
    ###############################################

    ## OUTPUTTING COMMAND 8 DATA
    print("Station 1:", station_id1, station_name1)
    g1 = command_8_2(station_id1, year_to_c)
    print("Station 2:", station_id2, station_name2)
    g2 = command_8_2(station_id2, year_to_c)

    ###############################################
    #Plotting or not
    print()
    print("plot? (y/n)", end=' ')
    answer = input()
    if (answer == "y"):
        x = []
        y = []
        count = 0
        for i in g1:
            x.append(count)
            y.append(i[1])
            count = count + 1

        x2 = []
        y2 = []
        count = 0
        for i in g2:
            x2.append(count)
            y2.append(i[1])
            count = count + 1

        plt.xlabel("day")
        plt.ylabel("number of riders")
        plt.title("riders each day of " + year_to_c)
        plt.plot(x, y, label=station_name1)
        plt.plot(x2, y2, label=station_names2)
        plt.legend()
        plt.show()


######################################################
### Command 9 ###
def command_9():
    print()
    print("Enter a line color (e.g. Red or Yellow):", end=' ')
    user_color = input()
    dbCursor = dbConn.cursor()
    cmd = "Select Color,Line_ID From Lines where Color like '" + user_color + "'"
    dbCursor.execute(cmd)
    row = dbCursor.fetchall()

    ###if no line was found or not
    if len(row) == 0:
        print("**No such line...")
    else:
        user_color = row[0][0]
        stop_id = str(row[0][1])
        cmd = "Select distinct Station_Name,Latitude,Longitude From Stops join StopDetails on StopDetails.Stop_ID=Stops.Stop_ID join Stations on Stations.Station_ID=Stops.Station_ID where Line_ID like '" + stop_id + "' order by Station_Name asc"
        dbCursor.execute(cmd)
        row = dbCursor.fetchall()
        #Print data
        for i in row:
            print(i[0], ": (" + str(i[1]) + ", " + str(i[2]) + ")")

        #Plot or not
        print()
        print("Plot? (y/n) ", end='')
        plotting = input()
        if (plotting == "y"):
            x = []
            y = []
            for i in row:
                x.append(i[2])
                y.append(i[1])
            image = plt.imread("chicago.png")
            xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
            plt.imshow(image, extent=xydims)
            plt.title(user_color + " line")
            if (user_color.lower() == "purple-express"):
                user_color = "Purple"
            plt.plot(x, y, "o", c=user_color)
            for i in row:
                plt.annotate(i[0], (i[2], i[1]))
            plt.xlim([-87.9277, -87.5569])
            plt.ylim([41.7012, 42.0868])
            plt.show()


##Checks commands## Checks which command the user input 
def command_check():

    print("Please enter a command (1-9, x to exit):", end=' ')
    command_chosen = input()

    while (command_chosen != 'x'):
        if (command_chosen == '1'):
            command_1()
        elif (command_chosen == '2'):
            command_2()
        elif (command_chosen == '3'):
            command_3()
        elif (command_chosen == '4'):
            command_4()
        elif (command_chosen == '5'):
            command_5()
        elif (command_chosen == '6'):
            command_6()
        elif (command_chosen == '7'):
            command_7()
        elif (command_chosen == '8'):
            command_8()
        elif (command_chosen == '9'):
            command_9()
        else:
            print("**Error, unknown command, try again...")
        print()
        print("Please enter a command (1-9, x to exit):", end=' ')
        command_chosen = input()


################################################################


## prints the stats at the start of the program ##
def print_stats(dbConn):
    dbCursor = dbConn.cursor()

    print("General stats:")

    dbCursor.execute("Select count(*) From Stations")
    row = dbCursor.fetchone()

    print("  # of stations:", f"{row[0]:,}")
    dbCursor.execute("Select count(*) From Stops")
    row = dbCursor.fetchone()
    print("  # of stops:", f"{row[0]:,}")

    ##Getting the number of ride entries
    dbCursor.execute("Select count(*) From ridership")
    row = dbCursor.fetchone()
    print("  # of ride entries:", f"{row[0]:,}")

    dbCursor.execute(
        "Select min(Date(Ride_Date)),max(Date(Ride_Date)) From ridership")
    row = dbCursor.fetchall()
    print("  date range:", row[0][0], " - ", row[0][1])

    dbCursor.execute("Select sum(num_riders) From ridership")
    row = dbCursor.fetchone()
    print("  Total ridership:", f"{row[0]:,}")
    totalrider = row[0]

    dbCursor.execute(
        "Select sum(num_riders) From ridership where Type_of_Day like 'W' ")
    row = dbCursor.fetchone()
    x = (row[0] / totalrider) * 100
    print("  Weekday ridership:", f"{row[0]:,}", f"({x:.2f}%)")

    dbCursor.execute(
        "Select sum(num_riders) From ridership where Type_of_Day like 'A' ")
    row = dbCursor.fetchone()
    x = (row[0] / totalrider) * 100
    print("  Saturday ridership:", f"{row[0]:,}", f"({x:.2f}%)")

    dbCursor.execute(
        "Select sum(num_riders) From ridership where Type_of_Day like 'U' ")
    row = dbCursor.fetchone()
    x = (row[0] / totalrider) * 100
    print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({x:.2f}%)")

    print()

    ##starts the command check funtion
    command_check()
    dbCursor.close()

    ### FOR ME ###
    ###BASICALLY SCHEMA###

    # dbCursor.execute("SELECT name FROM sqlite_master WHERE type='table' ;")
    # row = dbCursor.fetchall();
    # print(row)

    # for row in dbCursor.execute("pragma table_info('ridership')").fetchall():
    #     print (row)


##################################################################

#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

#
# done
#
