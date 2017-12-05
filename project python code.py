#Read Data with mySQL (connect, execute SQL)
import mysql.connector
#import pandas as pd

# Read data
#Question 1
## here we are displaying number of cities, number of states and numbers of cities for each state.
cnx = mysql.connector.connect(user='scott', password='pwd123', host='127.0.0.1', database='project_db2')
v_cursor = cnx.cursor()

v_query = ("SELECT"
    " COUNT(city_id) AS no_of_cities,"
    " COUNT(DISTINCT state) AS no_of_states"
    " FROM city")


v_cursor.execute(v_query)


for (no_of_cities, no_of_states) in v_cursor:
  print("Solution to question 1:\n\nThe number of cities and states in the USA are {} and {}\n\n".format(
    no_of_cities, no_of_states))


cnx = mysql.connector.connect(user='scott', password='pwd123', host='127.0.0.1', database='project_db2')
v_cursor = cnx.cursor()

v_query = ("SELECT"
    " state.state as state, COUNT(city_id) as city_count"
    " FROM"
    " city join state on city.state=state.state_id"
    " GROUP BY state")


v_cursor.execute(v_query)


for (state, city_count) in v_cursor:
  print("{} has {} number of cities.".format(state, city_count))

#Question 2

v_query = ("SELECT"
    " Round(AVG(price),3) AS average_rent,"
    " MIN(price) AS minimum_rent,"
    " MAX(price) AS maximum_rent"
    " FROM"
    " price")


v_cursor.execute(v_query)


for (average_rent, minimum_rent, maximum_rent) in v_cursor:
  print("\n\nSolution for Question2:\n\nThe overall average rent is {}. \n\nThe overall minimum rent is {}. \n\nThe overall maximum rent is {}."
        .format(average_rent, minimum_rent, maximum_rent))


#Question 3

v_query = ("SELECT"
    " round(AVG(ppsq),3) AS average_rent_persqft,"
    " round(MIN(ppsq),3) AS minimum_rent_persqft,"
    " round(MAX(ppsq),3) AS maximum_rent_persqft"
    " FROM"
    " ppsq")


v_cursor.execute(v_query)


for (average_rent_persqft, minimum_rent_persqft, maximum_rent_persqft) in v_cursor:
  print("\n\nSolution for Question3:\n\nThe overall average rent per sq ft is {}. \n\nThe overall minimum rent per sq ft is {}."
        "\n\nThe overall maximum rent per sq ft is {}. ".format(average_rent_persqft, minimum_rent_persqft, maximum_rent_persqft))


#Question 4
  
v_query = ("SELECT"
    " round(AVG(ppsq),3) AS average_rent_persqft_tx"
    " FROM"
    " city join ppsq on city.city_id=ppsq.city_city_id"
    " GROUP BY state"
    " HAVING state = 'TX'")


v_cursor.execute(v_query)


for (average_rent_persqft_tx) in v_cursor:
  print("\n\nSolution for Question4:\n\nThe average rent per sq ft is {} in Texas state.".format(average_rent_persqft_tx))


#Question5
##Assumption(s): We have compared average rent in Texas metro(s) with average rent of Texas state 

v_query = ("SELECT"
    " COUNT(*) as no_of_metros"
    " FROM"
    " (SELECT "
     "   metro_metro_id"
    " FROM"
      "  city"
    " JOIN ppsq ON city.city_id = ppsq.city_city_id and state='TX'"
    " GROUP BY metro_metro_id , state"
    " HAVING AVG(ppsq) > (SELECT "
      "      AVG(ppsq)"##for (minrent) in v_cursor:
##    x = minrent
##
##print (x)

       " FROM"
        "    city"
        " JOIN ppsq ON city.city_id = ppsq.city_city_id"
        " GROUP BY state"
        " HAVING state = 'TX')) as noofmetros")


v_cursor.execute(v_query)


for (no_of_metros) in v_cursor:
  print("\n\nSolution for Question5:\n\nThe number of metros having average rent per sq ft greater than Texas state is {}.".format(no_of_metros))


#Question 6
##Assumption: As a continuation of question 5, we have considered metros of state of Texas

v_query = ("select metro, city from city join metro on city.metro_metro_id=metro.metro_id where metro_metro_id in ("
 " SELECT "
    " city.metro_metro_id"
" FROM"
  "   city"
    "    JOIN"
    " ppsq ON city.city_id = ppsq.city_city_id and state='TX'"
      "  JOIN"
    " metro ON metro.metro_id = city.metro_metro_id"
" GROUP BY metro_metro_id , state"
" HAVING AVG(ppsq) > (SELECT "
  "      AVG(ppsq)"
   " FROM"
    "    city"
     "       JOIN"
      "  ppsq ON city.city_id = ppsq.city_city_id"
    " GROUP BY state"
    " HAVING state = 'TX'))")


v_cursor.execute(v_query)

print("\n\nSolution for Question6:\n\nThe metros having average rent per sq ft greater than Texas state and their cities are:\n\n ")
for (metro, city) in v_cursor:
  print("Metro: {} || city: {}".format(metro, city))


#Read Data with mySQL (connect, execute SQL)
import mysql.connector

#Question7
##Assumption 1: Metros withing the state of Texas are only considered.
##Assumption 2: Minimum increment is considered, hence rent decrement is eliminated.
cnx = mysql.connector.connect(user='scott', password='pwd123', host='127.0.0.1', database='project_db2')
v_cursor = cnx.cursor()


v_query=(" select metro.metro as mtr, diff from (select avg15.metro_metro_id as mtrid, (avg16-avg15) as diff " 
" from " 
" (select metro_metro_id, avg(price) as avg15" 
" from city c join price p on" 
" c.city_id=p.city_city_id" 
" where p.date='2015-09-01'" 
" and state='TX'" 
" group by metro_metro_id, state) as avg15 join" 
" (select metro_metro_id, avg(price) as avg16" 
" from city c join price p on" 
" c.city_id=p.city_city_id" 
" where p.date='2016-09-01'" 
" and state='TX'" 
" group by metro_metro_id, state) as avg16" 
" on avg15.metro_metro_id=avg16.metro_metro_id) as differ" 
" join metro on metro.metro_id=differ.mtrid" 
" where diff>=0" 
" group by mtrid" 
" having diff IN (select min(diff) from (" 
" select avg15.metro_metro_id, (avg16-avg15) as diff from (select metro_metro_id, avg(price) as avg15" 
" from city c join price p on" 
" c.city_id=p.city_city_id" 
" join metro m on" 
" c.metro_metro_id=m.metro_id" 
" where p.date='2015-09-01'" 
" and state='TX'" 
" group by metro_metro_id) as avg15 join" 
" (select metro_metro_id, avg(price) as avg16" 
" from city c join price p on" 
" c.city_id=p.city_city_id" 
" join metro m on" 
" c.metro_metro_id=m.metro_id" 
" where p.date='2016-09-01'" 
" and state='TX'" 
" group by metro_metro_id, state) as avg16" 
" on avg15.metro_metro_id=avg16.metro_metro_id) as differ" 
" where diff>0)" )

v_cursor.execute(v_query)

for (mtr, diff) in v_cursor:
  print("\n\n{} and its increment is {}".format(mtr, diff))





v_cursor.close()
cnx.close()

