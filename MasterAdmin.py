from Connection import Connection
from datetime import datetime
import maskpass
import bcrypt

#Custom Exception when Gender is invalid
class InvalidGenderException(Exception):
    pass

#Custom Exception when Date is of future.
class FutureDateException(Exception):
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
            while True:
                self.name=input('\nEnter name:').replace(' ','')

                if(self.name.isalpha() and len(self.name)>=3):
                    break
                else:
                    print('Name should only be Alphabetic!/Name should be of atleast 3 letters! ')
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
                    self.dob = datetime.strptime(input('Enter dob(dd-mm-yyyy): '), '%d-%m-%Y').date()

                    if self.dob >= datetime.now().date() or (datetime.now().year - self.dob.year <= 18):
                        raise FutureDateException()

                except FutureDateException:
                    print('Future Date!/You are not an adult!')
                except Exception as e:
                    print('Invalid Format!')
                else:
                    break
            while True:
                print('\nEnter a strong password.\nStrong password is alphanumeric with \"[@_!#$%^&*()<>?/\|}{~:]\" characters!')
                self.password=maskpass.askpass('Enter password:')

                def isSpecial(password):
                    for i in password:
                        if i in '[@_!#$%^&*()<>?/\|}{~:]':
                            return True
                    return False

                if(any(s.isalpha() for s in self.password) and any(s.isdigit() for s in self.password)  and isSpecial(self.password)):
                    break
                else:
                    print('Weak Password!')
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
    @staticmethod
    def viewProfile(id):
        sql='select id,ma_name,gender,dob from master_admin where id=%s'
        val=(id,)

        try:
            cursor.execute(sql,val)
            info=cursor.fetchall()
        except Exception as e:
            print(e)

        return list(info[0])
    
    #Checks whether Master Admin is present or not.
    @staticmethod
    def isMasterAdminPresent():
        try:
            cursor.execute('select count(*) from master_admin')
            count=cursor.fetchall()
        except Exception as e:
            print(e)

        if (count[0][0]<=0):
            return False
        
        return True
    
    #Checks credentials of MasterAdmin
    @staticmethod
    def checkLogin(id,password):
        try:
            cursor.execute('select id,pass from master_admin where id=%s',(id,))
            credentials=cursor.fetchall()
        except Exception as e:
            print(e)

        if credentials and bcrypt.checkpw(password.encode('utf-8'), credentials[0][1].encode('utf-8')):
            return True

        return False
    
    #Use to fetch password.
    @staticmethod
    def getPass(id):
        try:
            cursor.execute('SELECT pass FROM master_admin WHERE id=%s', (id,))
            credentials = cursor.fetchall()
        except Exception as e:
            print(e)

        return [credentials[0][0]]
    
    #Use to reset password.
    @staticmethod
    def resetPasswordbyId(id):
        while True:
            print('\nEnter a strong password.\nStrong password is alphanumeric with \"[@_!#$%^&*()<>?/\|}{~:]\" characters!')
            password=maskpass.askpass('Enter password:')
            a=password

            def isSpecial(password):
                for i in password:
                    if i in '[@_!#$%^&*()<>?/\|}{~:]':
                        return True
                return False

            if(any(s.isalpha() for s in password) and any(s.isdigit() for s in password)  and isSpecial(password)):
                break
            else:
                print('Weak Password!')

        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                                                
        try:
            cursor.execute('update master_admin set pass=%s where id=%s', (password,id))
            cursor.fetchall()
            con.commit()
        except Exception as e:
            print(e)

        if(cursor.rowcount>0):
            return True
        return False
    
     #closes connection at last.
    @staticmethod
    def closeConnection():
        cursor.close()
        con.close()


    #Checks if id is present or not.
    @staticmethod
    def isIdExist(id):
        try:
            cursor.execute('SELECT 1 FROM master_admin WHERE id = %s', (id,))
            result = cursor.fetchone()
        except Exception as e:
            print(e)
            
        if result is not None:
            return True  
        else:
            return False  
    
    #closes connection at last.
    @staticmethod
    def closeConnection():
        cursor.close()
        con.close()
        

