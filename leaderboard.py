import sqlite3 #Allows sql commands to be used in python file

conn = sqlite3.connect("UserName_Score.db") #Creates connection to file

c = conn.cursor() #Bound to the connection for the entire lifetime and all the commands are executed 

def create_table(): #Defines function for creating leaderboard
	c.execute("""CREATE TABLE leaderboard (
	            username text,
	            score integer    
	            )""") #Creates table


def add_user(user_name, score): #Defines function for adding user and score to database
	c.execute(f"INSERT INTO leaderboard VALUES ('{user_name}','{score}')") #Runs SQL command for adding user and score to database
	conn.commit() #Commits the current transaction


def select_users(): #Defines function for selecting users with the top 5 scores
    c.execute("SELECT * FROM leaderboard ORDER BY score DESC LIMIT 5") #Runs SQL command for selecting top 5 scores
    conn.commit() #Commits the current transaction
    return c.fetchall() #Returns values from table