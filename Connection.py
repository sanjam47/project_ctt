import mysql.connector

class Connection:
    
    def getConnection():
        con=None
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="47Billion@123",
                database="project_ctt"
            )
        except Exception as e:
            print(f'Some exception: {e}')

        return con


