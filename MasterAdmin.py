from Connection import Connection
from datetime import datetime
import maskpass
import bcrypt

#Custom Exception when Gender is invalid
class InvalidGenderException(Exception):
    pass

#Setup Connection with DB
con=Connection.getConnection()
cursor=con.cursor()

#MasterAdmin
class MasterAdmin:
    
    #Attributes for DB
    id=int()
    ma_name=''
    gender=''
    dob=''
    password=''
    
    #Increments the id of MasterAdmin
    def autoIncr(self):
        sql='select max(id) from master_admin;'
        try:
            cursor.execute(sql)
            max=cursor.fetchall()
        except Exception as e:
            print(e)

        if(max[0][0]==None):
            self.id=1
        else:
            self.id=max[0][0]+1
    
    #Takes MasterAdmin data from user
    def fetchMasterAdmin(self):
        choice=input('Warning! You won\'t be able to exit till you add an admin.\nDo you want to continue?(y/n):')
        if(choice=='y' or choice=='Y'):
            self.ma_name=input('\nEnter name:')

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
        else:
            pass
    
    #Adds MasterAdmin data to DB
    def addMasterAdmin(self):
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        MasterAdmin.autoIncr(self)
        sql='insert into master_admin values(%s,%s,%s,%s,%s)'
        val=(self.id,self.ma_name,self.gender,self.dob,hashed_password)

        try:
            cursor.execute(sql,val)
            con.commit()
        except Exception as e:
            print(e)
    
    #Reads the data from DB
    def viewProfile(self,id):
        sql='select id,ma_name,gender,dob from master_admin where id=%s'
        val=(id,)

        try:
            cursor.execute(sql,val)
            info=cursor.fetchall()
        except Exception as e:
            print(e)

        return list(info[0])
    
    #Checks whether Master Admin is present or not.
    def isMasterAdmin(self):
        try:
            cursor.execute('select count(*) from master_admin')
            count=cursor.fetchall()
        except Exception as e:
            print(e)

        if (count[0][0]<=0):
            return False
        
        return True
    
    #Checks credentials of MasterAdmin
    def checkLogin(self,id,password):
        try:
            cursor.execute('select id,pass from master_admin where id=%s and pass=%s',(id,password))
            credentials=cursor.fetchall()
        except Exception as e:
            print(e)

        if(len(credentials)==0):
            return False
        
        return True
        

