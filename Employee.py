import mysql.connector
from Connection import Connection
from datetime import datetime
import maskpass
import uuid


con=Connection.getConnection()
cursor=con.cursor()

#Custom Exception when Gender is invalid.
class InvalidGenderException(Exception):
    pass

class Employee:
    act_no=int()
    id=int()
    name=''
    gender=''
    dob=''
    password=''
    balance=int()
    isAdmin=bool()
        

    def autoIncr(self):
        sql='select max(id) from accounts;'
        cursor.execute(sql)
        max=cursor.fetchall()
        if(max[0][0]==None):
            self.id=1000
        else:
            self.id=max[0][0]+1


    def inputAdmin(self):
        self.act_no=str(uuid.uuid4().int)[:10]
        Employee.autoIncr(self)
        self.name=input('Enter employee name:')
        while True:
            try:
                self.gender=input('Enter your gender(M/F):')
                if self.gender not in ('M','F'):
                    raise InvalidGenderException('You can only enter M/F')
                else:
                    break
            except InvalidGenderException as e:
                print(e)
        while True:
            try:
                self.dob=datetime.strptime(input('Enter your dob(dd-mm-yyyy):'),'%d-%m-%Y').date()
            except Exception as e:
                print(e)
            else:
                break
        self.password=maskpass.askpass('Enter password:')
        self.balance=input('Enter intial balance:')
        self.isAdmin=True

    def insertAdmin(self):
        sql='insert into accounts(act_no,id,emp_name,gender,dob,pass,balance,isAdmin) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        val=(self.act_no,self.id,self.name,self.gender,self.dob,self.password,self.balance,self.isAdmin)
        cursor.execute(sql,val)
        con.commit()

        if(cursor.rowcount>0):
            print(f'{cursor.rowcount} rows affected.')
        else:
            print('Data not inserted')

    def viewAdminProfile(id):
        sql='select * from accounts where id=%s'
        val=(id,)
        cursor.execute(sql,val)
        info=cursor.fetchall()
        return list(info[0])
    
    def viewEmployees():
        sql='select act_no,id,emp_name,gender,dob,balance,isAdmin from accounts order by id'
        cursor.execute(sql)
        info=cursor.fetchall()

        return info
    
    def inputEmployee(self):
        self.act_no=str(uuid.uuid4().int)[:10]
        Employee.autoIncr(self)
        self.name=input('Enter employee name:')
        while True:
            try:
                self.gender=input('Enter your gender(M/F):')
                if self.gender not in ('M','F'):
                    raise InvalidGenderException('You can only enter M/F')
                else:
                    break
            except InvalidGenderException as e:
                print(e)
        while True:
            try:
                self.dob=datetime.strptime(input('Enter your dob(dd-mm-yyyy):'),'%d-%m-%Y').date()
            except Exception as e:
                print(e)
            else:
                break
        self.password=maskpass.askpass('Enter password:')
        self.balance=input('Enter intial balance:')
        self.isAdmin=False

    def insertEmployee(self):
        sql='insert into accounts(act_no,id,emp_name,gender,dob,pass,balance,isAdmin) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        val=(self.act_no,self.id,self.name,self.gender,self.dob,self.password,self.balance,self.isAdmin)
        cursor.execute(sql,val)
        con.commit()

        if(cursor.rowcount>0):
            print(f'{cursor.rowcount} rows affected.')
        else:
            print('Data not inserted')
        
    
    def viewProfile(self,id):
        sql='select act_no,id,emp_name,gender,dob,balance,isAdmin from accounts where id=%s'
        val=(id,)
        cursor.execute(sql,val)
        info=cursor.fetchall()
        return list(info[0])
    
    def viewBalance(self,id,password):
        sql='select balance from accounts where id=%s and pass=%s'
        val=(id,password)
        cursor.execute(sql,val)
        balance=cursor.fetchall()
        return [balance[0][0]]
    
    def updateBalance(self,act_no,balance):
        sql='update  accounts set balance=%s where act_no=%s'
        val=(balance,act_no)
        cursor.execute(sql,val)
        con.commit()
        if(cursor.rowcount>0):
            print(f'{cursor.rowcount} balance affected')
        else:
            print('No balance updated')
    
    def addTransaction(self,id,trans_date,trans_type,dc_amount,balance):
        trans_id=int(str(uuid.uuid4().int)[:10])
        sql='insert into transactions values (%s,%s,%s,%s,%s,%s)'
        val=(trans_id,id,trans_date,trans_type,dc_amount,balance)
        cursor.execute(sql,val)
        con.commit()
        if(cursor.rowcount>0):
            print(f'{cursor.rowcount} transaction added')
        else:
            print('No transaction added')

    def viewTransactionsbyId(id):
        sql='select * from transactions where emp_id=%s order by trans_date'
        cursor.execute(sql,(id,))
        info=cursor.fetchall()

        return info
    
    def checkLogin(self,id,password):
        try:
            cursor.execute('select id,pass from accounts where id=%s and pass=%s',(id,password))
            credentials=cursor.fetchall()
        except Exception as e:
            print(e)

        if(len(credentials)==0):
            return False
        
        return True
    
    


