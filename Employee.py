from Connection import Connection
from datetime import datetime
import maskpass
import uuid
import bcrypt

con=Connection.getConnection()
cursor=con.cursor()

#Custom Exception when Gender is invalid.
class InvalidGenderException(Exception):
    pass

#Custom Exception when Amount is invalid.
class InvalidAmountException(Exception):
    pass

#Custom Exception when Date is of future.
class FutureDateException(Exception):
    pass

#Employee
class Employee:
    act_no=int()
    id=int()
    name=''
    gender=''
    dob=''
    password=''
    balance=float()
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

    @staticmethod
    def checkAmountFormat(amount):
        amount=str(amount)
        b=amount.split('.')

        if len(b[1])<=2:
            return True
        
        return False

    
    #Fetches all Employees
    @staticmethod
    def viewEmployees():
        sql='select act_no,id,emp_name,gender,dob,balance,isAdmin from accounts order by id'

        try:
            cursor.execute(sql)
            info=cursor.fetchall()
        except Exception as e:
            print(e)

        return info
    
    #Inputs the data of Employee
    def  inputEmployee(self,isAdmin):
        self.act_no=str(uuid.uuid4().int)[:10]
        Employee.autoIncr(self)

        choice=input('Warning! You won\'t be able to exit till you add an employee.\nDo you want to continue?(y/n):')
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
                    
            while True:
                try:
                    self.balance=float(input('Enter intial balance(₹):'))
                    if Employee.checkAmountFormat(self.balance)==False:
                        raise InvalidAmountException()
                except InvalidAmountException as e:
                    print('Amount is always in Integer or Decimal(upto 2 decimal points)')
                except Exception as ec:
                    print(ec)
                else:
                    break
            
            self.isAdmin=isAdmin
            if(Employee.addEmployee(self)):
                return True
            else:
                return False
        else:
            pass

    #Adds the Employee to DB.
    def addEmployee(self):
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        sql='insert into accounts(act_no,id,emp_name,gender,dob,pass,balance,isAdmin) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        val=(self.act_no,self.id,self.name,self.gender,self.dob,hashed_password,self.balance,self.isAdmin)

        try:
            cursor.execute(sql,val)
            con.commit()
        except Exception as e:
            print(e)

        if(cursor.rowcount>0):
            return True
        return False
        
    #Gives profile of Employee.
    @staticmethod
    def viewProfile(id):
        sql='select act_no,id,emp_name,gender,dob,balance,isAdmin from accounts where id=%s'
        val=(id,)

        try:
            cursor.execute(sql,val)
            info=cursor.fetchall()
        except Exception as e:
            print(e)

        return list(info[0])
    
    #Fetches balance of Employee.
    @staticmethod
    def viewBalance(id):
        sql='select balance from accounts where id=%s'
        val=(id,)

        try:
            cursor.execute(sql,val)
            balance=cursor.fetchall()
        except Exception as e:
            print(e)

        return [balance[0][0]]
    
    #Update balance of Employee.
    @staticmethod
    def updateBalance(act_no,balance):
        sql='update  accounts set balance=%s where act_no=%s'
        val=(balance,act_no)

        try:
            cursor.execute(sql,val)
            con.commit()
        except Exception as e:
            print(e)


    #Checks the login credentials
    @staticmethod
    def checkLogin(id, password):
        try:
            cursor.execute('SELECT id, pass FROM accounts WHERE id = %s', (id,))
            credentials = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching credentials: {e}")  

        if credentials and bcrypt.checkpw(password.encode('utf-8'), credentials[0][1].encode('utf-8')):
            return True

        return False
    
    #Use to identify that Employee is Admin or not.
    @staticmethod
    def isEmployeeAdmin( id, password):
        try:
            cursor.execute('SELECT id, pass FROM accounts WHERE id=%s and isAdmin=1', (id,))
            credentials = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")

        if credentials and bcrypt.checkpw(password.encode('utf-8'), credentials[0][1].encode('utf-8')):
            return True

        return False
    
    #Use to fetch password.
    @staticmethod
    def getPass(id):
        try:
            cursor.execute('SELECT pass FROM accounts WHERE id=%s', (id,))
            credentials = cursor.fetchall()
        except Exception as e:
            print(e)

        return [credentials[0][0]]
    
    #Use to reset password
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
            cursor.execute('update accounts set pass=%s where id=%s', (password,id))
            cursor.fetchall()
            con.commit()
        except Exception as e:
            print(e)

        if(cursor.rowcount>0):
            return True
        return False
    
    #Checks if id is present or not.
    @staticmethod
    def isIdExist(id):
        try:
            cursor.execute('SELECT 1 FROM accounts WHERE id = %s', (id,))
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


        



    

    
    
    


