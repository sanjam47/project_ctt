from Connection import Connection
from datetime import datetime
import maskpass
import uuid


con=Connection.getConnection()
cursor=con.cursor()

#Custom Exception when Gender is invalid.
class InvalidGenderException(Exception):
    pass

#Employee
class Employee:
    act_no=int()
    id=int()
    name=''
    gender=''
    dob=''
    password=''
    balance=int()
    isAdmin=bool()
        
    #Increments id of Employee
    def autoIncr(self):
        sql='select max(id) from accounts;'

        try:
            cursor.execute(sql)
            max=cursor.fetchall()
        except Exception as e:
            print(e)
        
        if(max[0][0]==None):
            self.id=1000
        else:
            self.id=max[0][0]+1
    
    #Fetches all Employees
    def viewEmployees(self):
        sql='select act_no,id,emp_name,gender,dob,balance,isAdmin from accounts order by id'

        try:
            cursor.execute(sql)
            info=cursor.fetchall()
        except Exception as e:
            print(e)

        return info
    
    #Inputs the data of Employee
    def inputEmployee(self,isAdmin):
        self.act_no=str(uuid.uuid4().int)[:10]
        Employee.autoIncr(self)
        choice=input('Warning! You won\'t be able to exit till you add an employee.\nDo you want to continue?(y/n):')
        self.name=input('\nEnter  name:')
        while True:
            try:
                self.gender=input('Enter gender(M/F):')
                if self.gender not in ('M','F'):
                    raise InvalidGenderException('You can only enter M/F')
                else:
                    break
            except InvalidGenderException as e:
                print(e)
        while True:
            try:
                self.dob=datetime.strptime(input('Enter dob(dd-mm-yyyy):'),'%d-%m-%Y').date()
            except Exception as e:
                print(e)
            else:
                break
        self.password=maskpass.askpass('Enter password:')
        self.balance=input('Enter intial balance:')
        self.isAdmin=isAdmin

    #Adds the Employee to DB.
    def addEmployee(self):
        sql='insert into accounts(act_no,id,emp_name,gender,dob,pass,balance,isAdmin) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        val=(self.act_no,self.id,self.name,self.gender,self.dob,self.password,self.balance,self.isAdmin)

        try:
            cursor.execute(sql,val)
            con.commit()
        except Exception as e:
            print(e)
        
    #Gives profile of Employee.
    def viewProfile(self,id):
        sql='select act_no,id,emp_name,gender,dob,balance,isAdmin from accounts where id=%s'
        val=(id,)

        try:
            cursor.execute(sql,val)
            info=cursor.fetchall()
        except Exception as e:
            print(e)

        return list(info[0])
    
    #Fetches balance of Employee.
    def viewBalance(self,id,password):
        sql='select balance from accounts where id=%s and pass=%s'
        val=(id,password)

        try:
            cursor.execute(sql,val)
            balance=cursor.fetchall()
        except Exception as e:
            print(e)

        return [balance[0][0]]
    
    #Update balance of Employee.
    def updateBalance(self,act_no,balance):
        sql='update  accounts set balance=%s where act_no=%s'
        val=(balance,act_no)

        try:
            cursor.execute(sql,val)
            con.commit()
        except Exception as e:
            print(e)


    #Checks the login credentials
    def checkLogin(self,id,password):
        try:
            cursor.execute('select id,pass from accounts where id=%s and pass=%s',(id,password))
            credentials=cursor.fetchall()
        except Exception as e:
            print(e)

        if(len(credentials)==0):
            return False
        
        return True
    
    #Checks if the Employee is Admin or not.
    def isEmployeeAdmin(self,id,password):
        try:
            cursor.execute('select id,pass from accounts where id=%s and pass=%s and isAdmin=1',(id,password))
            credentials=cursor.fetchall()
        except Exception as e:
            print(e)
        
        if(len(credentials)==0):
            return False
        
        return True
    

    
    
    


