from Connection import Connection


con=Connection.getConnection()
cursor=con.cursor()

cursor.execute('select max(id) from master_admin')
count=cursor.fetchall()
print(count)