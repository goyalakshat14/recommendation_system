def collaborative_filter();

#testing collaborative filter

password = input("enter the password - ")
db = pymysql.connect("localhost","root",password,"newMovieLens" )
cursor = db.cursor()