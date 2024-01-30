from Connection import Connection
from MasterAdmin import MasterAdmin
from Employee import Employee
import maskpass
from tabulate import tabulate
from datetime import datetime

con=Connection.getConnection()
cursor=con.cursor()

print('\nWelcome to Employee Transaction Tracker!')

while True:
    choice=input('\nDo you want to continue?(y/n):')

    if choice=='Y'or choice=='y':
        ma=MasterAdmin()
        if(not ma.isMasterAdmin()):
            print('Create Master Admin')
            ma=MasterAdmin()
            ma.fetchMasterAdmin()
            ma.addMasterAdmin()
            con.commit()
        
        if(ma.isMasterAdmin()):
            while True:
                try:
                    choice=int(input('1.Master Admin\n2.Employee\n3.Admin\n4.Exit\nLogin as:'))
                except Exception as e:
                    print(e)
                
                if(choice==1):
                    while True:
                        
                        try:
                            id=int(input('Enter id:'))
                        except Exception as e:
                            print(e)
                        else:
                            password=maskpass.askpass('Enter password:','*')
                                
                            ma=MasterAdmin()
                            if(not ma.checkLogin(id,password)):
                                print('Invalid credentials!')
                            else:
                                while True:
                                    try:
                                        choice=int(input('1.View Profile\n2.Add Admin\n3.Exit\nEnter choice:'))
                                    except Exception as e:
                                        print(e)
                                    else:
                                        ma=MasterAdmin()
                                        if(choice==1):
                                            info=list([ma.viewProfile(id)])
                                            fields=['Id','Name','Gender','Dob']
                                            print(tabulate(info,headers=fields,tablefmt='grid'))
                                        elif(choice==2):
                                            E=Employee()
                                            E.inputAdmin()
                                            E.insertAdmin()
                                        elif(choice==3):
                                            break
                                        else:
                                            print('Invalid Choice!') 
                                break                              
                elif(choice==2):
                    while True:
                        try:
                            id=int(input('Enter id:'))
                        except Exception as e:
                            print(e)
                        else:
                            password=maskpass.askpass('Enter password:','*')

                            cursor.execute('select id,pass from accounts where id=%s and pass=%s',(id,password))
                            credentials=cursor.fetchall()
                            
                            e=Employee()
                            if(not e.checkLogin(id,password)):
                                print('Invalid credentials!')
                            else:
                                while True:
                                    try:
                                        choice=int(input('1.View Profile\n2.View Balance\n3.Transaction\n4.Transaction History\n5.Exit\nEnter choice:'))
                                    except Exception as e:
                                        print(e)
                                    else:
                                        if(choice==1):
                                            e=Employee()
                                            info=list([e.viewProfile(id)])
                                            fields=['A/c No','Id','Name','Gender','Dob','Balance','isAdmin']
                                            print(tabulate(info,headers=fields,tablefmt='grid'))
                                        elif(choice==2):
                                            e=Employee()
                                            balance=list([e.viewBalance(id,password)])
                                            fields=['Current Balance']
                                            print(tabulate(balance,headers=fields,tablefmt='grid'))
                                        elif(choice==3):
                                            while True:
                                                choice=int(input('1.Send\n2.Recieve\n3.Exit\nEnter Choice:'))
                                                if(choice==1):
                                                    trans_type='Debit'
                                                    trans_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                    e=Employee()
                                                    balance=e.viewBalance(id,password)
                                                    info=list(Employee.viewEmployeeProfile(id))
                                                    act_no=info[0]
                                                    send=int(input('Enter amount:'))

                                                    if(send>balance):
                                                        print(f'Insufficient Balance!\nYour current_balance is:{balance}')
                                                    else:
                                                        balance-=send
                                                        E.updateBalance(act_no,balance)
                                                        con.commit()
                                                        E.addTransaction(id,trans_date,trans_type,send,balance)
                                                        con.commit()
                                                elif(choice==2):
                                                    trans_type='Credit'
                                                    trans_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                    E=Employee()
                                                    balance=E.viewBalance(id,password)
                                                    info=list(Employee.viewEmployeeProfile(id))
                                                    act_no=info[0]
                                                    recieve=int(input('Enter amount:'))
                                                    balance+=recieve
                                                    E.updateBalance(act_no,balance)
                                                    con.commit()
                                                    E.addTransaction(id,trans_date,trans_type,recieve,balance)
                                                    con.commit()
                                                elif(choice==3):
                                                    break
                                                    
                                                    
                                                
                                        elif(choice==4):
                                            transactions=Employee.viewTransactionsbyId(id)
                                            fields=['Transaction Id','Employee Id','Transaction Date','Type','Debit/Credit Amount','Current Balance']
                                            print(tabulate(transactions,headers=fields,tablefmt='grid'))
                                        elif(choice==5):
                                            break
                                    
                                
                                    break
                elif(choice==3):
                    while True:
                        try:
                            id=int(input('Enter id:'))
                            password=maskpass.askpass('Enter password:','*')
                            cursor.execute('select id,pass from accounts where id=%s and pass=%s and isAdmin=1',(id,password))
                            credentials=cursor.fetchall()
                            if(len(credentials)==0):
                                print('Invalid credentials/Not an Admin')
                            else:
                                while True:
                                    try:
                                        choice=int(input('1.View Profile\n2.Employees\n3.Add Employee\n4.Exit\nEnter choice:'))
                                    except Exception as e:
                                        print(e)
                                    else:
                                        if(choice==1):
                                            info=list(Employee.viewAdminProfile(id))
                                            print(f'A/c No:{info[0]}    id:{info[1]}   Name:{info[2]}    Gender:{info[3]}    Dob:{info[4]}   Balance:{info[6]}')
                                        elif(choice==2):
                                            employees=Employee.viewEmployees(id)
                                            fields=['A/c No','Id','Name','Gender','Dob','Balance','isAdmin']
                                            print(tabulate(employees,headers=fields,tablefmt='grid'))
                                        elif(choice==3):
                                            E=Employee()
                                            E.inputEmployee()
                                            E.insertEmployee()
                                        elif(choice==4):
                                            break
                            
                        except Exception as e:
                            print(e)
                        break
                elif(choice==4):
                    break
                else:
                    print('Enter valid choice!')

    elif choice=='N' or choice=='n':
        while True:
            choice=input('\nAre you sure you want to exit?(y/n):')
            if choice=='Y'or choice=='y':
                exit()
            else:
                print('Invalid Choice')
    else:
        print('Invalid choice!')