from Connection import Connection
from MasterAdmin import MasterAdmin
from Employee import Employee
from Transaction import Transaction
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
                    print('Invalid choice!')
                else:
                    if(choice==1):
                        while True:
                            
                            try:
                                id=int(input('Enter id:'))
                            except Exception as e:
                                print('Id is always Integer!')
                            else:
                                password=maskpass.askpass('Enter password:','*')
                                    
                                ma=MasterAdmin()
                                if(not ma.checkLogin(id,password)):
                                    print('Invalid credentials!')

                                    choice=input('\nDo you want to continue?(y/n):')
                                    if(choice=='Y' or choice=='y'):
                                        pass
                                    else:
                                        break
                                else:
                                    while True:
                                        try:
                                            choice=int(input('1.View Profile\n2.Add Admin\n3.Exit\nEnter choice:'))
                                        except Exception as e:
                                            print('Invalid choice!')
                                        else:
                                            ma=MasterAdmin()
                                            if(choice==1):
                                                info=list([ma.viewProfile(id)])
                                                fields=['Id','Name','Gender','Dob']
                                                print(tabulate(info,headers=fields,tablefmt='grid'))
                                            elif(choice==2):
                                                E=Employee()
                                                E.inputEmployee(True)
                                                E.addEmployee()
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
                                print('Id is always Integer!')
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
                                            print('Invalid choice!')
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
                                                    try:
                                                        choice=int(input('1.Send\n2.Recieve\n3.Exit\nEnter Choice:'))
                                                    except Exception as e:
                                                        print('Invalid choice!')
                                                    else:
                                                        if(choice==1):
                                                            e=Employee()
                                                            balance=int(e.viewBalance(id,password)[0])
                                                            info=list(e.viewProfile(id))
                                                            act_no=info[0]
                                                            send=int(input('Enter amount:'))

                                                            if(send>balance):
                                                                print(f'Insufficient Balance!\nYour current_balance is:{balance}')
                                                            else:
                                                                balance-=send
                                                                e.updateBalance(act_no,balance)
                                                                con.commit()
                                                                T=Transaction()
                                                                T.addTransaction(id,'Debit',send,balance)
                                                                con.commit()
                                                        elif(choice==2):
                                                            e=Employee()
                                                            balance=int(e.viewBalance(id,password)[0])
                                                            info=list(e.viewProfile(id))
                                                            act_no=info[0]
                                                            recieve=int(input('Enter amount:'))
                                                            balance+=recieve
                                                            e.updateBalance(act_no,balance)
                                                            con.commit()
                                                            T=Transaction()
                                                            T.addTransaction(id,'Credit',recieve,balance)
                                                            con.commit()
                                                        elif(choice==3):
                                                            break
                                                        else:
                                                            print('Enter Valid Choice!')       
                                            elif(choice==4):
                                                T=Transaction()
                                                transactions=T.viewTransactionsbyId(id)
                                                fields=['Transaction Id','Employee Id','Transaction Date','Type','Debit/Credit Amount','Balance']
                                                print(tabulate(transactions,headers=fields,tablefmt='grid'))
                                            elif(choice==5):
                                                break
                                            else:
                                                print('Enter Valid Choice!')
                                    break
                    elif(choice==3):
                        while True:
                            try:
                                id=int(input('Enter id:'))
                            except Exception as e:
                                print('Id is always Integer!')
                            else:
                                password=maskpass.askpass('Enter password:','*')
                                
                                e=Employee()
                                if(not e.isEmployeeAdmin(id,password)):
                                    print('Invalid credentials/Not an Admin')
                                else:
                                    while True:
                                        try:
                                            choice=int(input('1.View Profile\n2.Employees\n3.Add Employee\n4.Exit\nEnter choice:'))
                                        except Exception as e:
                                            print('Invalid choice!')
                                        else:
                                            if(choice==1):
                                                e=Employee()
                                                info=list([e.viewProfile(id)])
                                                fields=['A/c No','Id','Name','Gender','Dob','Balance','isAdmin']
                                                print(tabulate(info,headers=fields,tablefmt='grid'))
                                            elif(choice==2):
                                                e=Employee()
                                                employees=e.viewEmployees()
                                                fields=['A/c No','Id','Name','Gender','Dob','Balance','isAdmin']
                                                print(tabulate(employees,headers=fields,tablefmt='grid'))
                                            elif(choice==3):
                                                E=Employee()
                                                E.inputEmployee(False)
                                                E.addEmployee()
                                            elif(choice==4):
                                                break
                                    break
                    elif(choice==4):
                        break
                    else:
                        print('Enter valid choice!')

    elif choice=='N' or choice=='n':
        while True:
            choice=input('\nAre you sure you want to exit?(y/n):')
            if choice=='Y'or choice=='y':
                con.close()
                exit()
            else:
                print('Invalid Choice')
    else:
        print('Invalid choice!')
