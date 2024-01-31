from Connection import Connection
from datetime import datetime
import uuid

con=Connection.getConnection()
cursor=con.cursor()

class Transaction:
   
   #Adds Transaction to DB.
    def addTransaction(self,id,trans_type,dc_amount,balance):
        trans_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trans_id=int(str(uuid.uuid4().int)[:10])
        sql='insert into transactions values (%s,%s,%s,%s,%s,%s)'
        val=(trans_id,id,trans_date,trans_type,dc_amount,balance)
        
        try:
            cursor.execute(sql,val)
            con.commit()
        except Exception as e:
            print(e)

    #Fetches Transaction on id.
    def viewTransactionsbyId(id):
        sql='select * from transactions where emp_id=%s order by trans_date'
        
        try:
            cursor.execute(sql,(id,))
            info=cursor.fetchall()
        except Exception as e:
            print(e)

        return info