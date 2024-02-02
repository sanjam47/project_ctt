from MasterAdmin import MasterAdmin
from Employee import Employee
from Employee import InvalidAmountException
from Transaction import Transaction
import maskpass
from tabulate import tabulate

print('\nWelcome to Employee Transaction Tracker!')

while True:
    choice=input('\nDo you want to continue?(y/n):')

    if choice=='Y'or choice=='y':
        if(not MasterAdmin.isMasterAdminPresent()):
            print('\nCreate Master Admin')
            ma=MasterAdmin()
            ma.fetchMasterAdmin()
            ma.addMasterAdmin()
        
        if(MasterAdmin.isMasterAdminPresent()):
            while True:
                try:
                    choice=int(input('\n1.Master Admin\n2.Employee\n3.Admin\n4.Exit\nLogin as:'))
                except Exception as e:
                    print('Invalid choice!')
                else:
                    if(choice==1):
                        while True:
                            
                            try:
                                id=int(input('\nEnter id:'))
                            except Exception as e:
                                print('Id is always Integer!')
                            else:
                                password=maskpass.askpass('Enter password:','*')
                                    
                                if(not MasterAdmin.checkLogin(id,password)):
                                    print('\nInvalid credentials!')

                                    reset_pass=input('\nWant to reset password?(y/n):')

                                    if reset_pass=='y' or reset_pass=='Y':
                                        while True:
                                            try:
                                                reset_id=int(input('\nEnter id:'))
                                            except Exception as e:
                                                print('Id is always Integer!')
                                            else:
                                                if(MasterAdmin.isIdExist(reset_id)):
                                                    if(MasterAdmin.resetPasswordbyId(reset_id)):
                                                        print('Password updated!')
                                                        break
                                                    else:
                                                        print('Password not updated!')
                                                        break
                                                else:
                                                    print('Id doesnot exist!')
                                                    break
                                    
                                    choice=input('\nDo you want to continue?(y/n):')

                                    if(choice=='Y' or choice=='y'):
                                        pass
                                    else:
                                        break
                                else:
                                    while True:
                                        try:
                                            choice=int(input('\n1.View Profile\n2.Add Admin\n3.Exit\nEnter choice:'))
                                        except Exception as e:
                                            print('Invalid choice!')
                                        else:
                                            if(choice==1):
                                                info=list([MasterAdmin.viewProfile(id)])
                                                fields=['Id','Name','Gender','Dob']
                                                print(tabulate(info,headers=fields,tablefmt='grid',floatfmt=f".{2}f"))

                                                isViewPass=input('Do you want to see your password(y/n):')
                                                if(isViewPass=='Y'or isViewPass=='y'):
                                                    your_pass=list([MasterAdmin.getPass(id)])
                                                    fields=['Your Password']
                                                    print(tabulate(your_pass,headers=fields,tablefmt='grid',floatfmt=f".{2}f"))
                                                else:
                                                    pass
                                            elif(choice==2):
                                                E=Employee()
                                                isAdminAdded=E.inputEmployee(True)
                                                if(isAdminAdded):
                                                    print('Admin added!')
                                                else:
                                                    print('Admin not added!')
                                            elif(choice==3):
                                                break
                                            else:
                                                print('\nInvalid Choice!') 
                                    break                              
                    elif(choice==2):
                        while True:
                            try:
                                id=int(input('\nEnter id:'))
                            except Exception as e:
                                print('Id is always Integer!')
                            else:
                                password=maskpass.askpass('Enter password:','*')
                                
                                if(Employee.checkLogin(id,password)==False):
                                    print('Invalid credentials!')

                                    reset_pass=input('\nWant to reset password?(y/n):')

                                    if reset_pass=='y' or reset_pass=='Y':
                                        while True:
                                            try:
                                                reset_id=int(input('\nEnter id:'))
                                            except Exception as e:
                                                print('Id is always Integer!')
                                            else:
                                                if(Employee.isIdExist(reset_id)):
                                                    if(Employee.resetPasswordbyId(reset_id)):
                                                        print('Password updated!')
                                                        break
                                                    else:
                                                        print('Password not updated!')
                                                        break
                                                else:
                                                    print('Id doesnot exist')
                                                    break

                                    choice=input('\nDo you want to continue?(y/n):')
                                    if(choice=='Y' or choice=='y'):
                                        pass
                                    else:
                                        break
                                else:
                                    while True:
                                        try:
                                            choice=int(input('\n1.View Profile\n2.View Balance\n3.Transaction\n4.Transaction History\n5.Exit\nEnter choice:'))
                                        except Exception as e:
                                            print('\nInvalid choice!')
                                        else:
                                            if(choice==1):
                                                info=list([Employee.viewProfile(id)])
                                                fields=['A/c No','Id','Name','Gender','Dob','Balance(₹)','isAdmin']
                                                print(tabulate(info,headers=fields,tablefmt='grid',floatfmt=f".{2}f"))

                                                isViewPass=input('Do you want to see your password(y/n):')
                                                if(isViewPass=='Y'or isViewPass=='y'):
                                                    your_pass=list([Employee.getPass(id)])
                                                    fields=['Your Password']
                                                    print(tabulate(your_pass,headers=fields,tablefmt='grid',floatfmt=f".{2}f"))
                                                else:
                                                    pass
                                            elif(choice==2):
                                                balance=list([Employee.viewBalance(id)])
                                                print(balance)
                                                fields=['Current Balance(₹)']
                                                print(tabulate(balance,headers=fields,tablefmt='grid',floatfmt=f".{2}f"))
                                            elif(choice==3):
                                                while True:
                                                    try:
                                                        choice=int(input('\n1.Send\n2.Recieve\n3.Exit\nEnter Choice:'))
                                                    except Exception as e:
                                                        print('\nInvalid choice!')
                                                    else:
                                                        if(choice==1):
                                                            balance=float(Employee.viewBalance(id)[0])
                                                            info=list(Employee.viewProfile(id))
                                                            act_no=info[0]

                                                            while True:
                                                                try:
                                                                    send=float(input('\nEnter amount(₹):'))
                                                                    if Employee.checkAmountFormat(send)==False:
                                                                        raise InvalidAmountException()
                                                                except InvalidAmountException:
                                                                    print('Amount is always in Integer or Decimal(upto 2 decimal points)!')
                                                                except Exception as ec:
                                                                     print(ec)
                                                                else:
                                                                    break

                                                            if(send>balance):
                                                                print(f'\nInsufficient Balance!\nYour current_balance is:{balance}')
                                                            else:
                                                                balance-=send
                                                                Employee.updateBalance(act_no,balance)
                                                                isSent=Transaction.addTransaction(id,'Debit',send,balance)
                                                                if(isSent):
                                                                    print('Amount sent!')
                                                                else:
                                                                    print('Amount not sent!')
                                                        elif(choice==2):
                                                            balance=float(Employee.viewBalance(id)[0])
                                                            info=list(Employee.viewProfile(id))
                                                            act_no=info[0]
                                                            while True:
                                                                try:
                                                                    recieve=float(input('\nEnter amount(₹):'))
                                                                    if Employee.checkAmountFormat(recieve)==False:
                                                                        raise InvalidAmountException()
                                                                except InvalidAmountException:
                                                                    print('Amount is always in Integer or Decimal(upto 2 decimal points)!')
                                                                except Exception:
                                                                    print('Invalid Format!')
                                                                else:
                                                                    break
                                                            balance+=recieve
                                                            Employee.updateBalance(act_no,balance)
                                                            isRecieved=Transaction.addTransaction(id,'Credit',recieve,balance)
                                                            if(isRecieved):
                                                                print('Amount recieved!')
                                                            else:
                                                                print('No amount recived!')
                                                        elif(choice==3):
                                                            break
                                                        else:
                                                            print('Enter Valid Choice!')       
                                            elif(choice==4):
                                                transactions=Transaction.viewTransactionsbyId(id)
                                                fields=['Transaction Id','Employee Id','Transaction Time','Type','Debit/Credit Amount(₹)','Balance(₹)']
                                                print(tabulate(transactions,headers=fields,tablefmt='grid',floatfmt=f".{2}f"))
                                            elif(choice==5):
                                                break
                                            else:
                                                print('\nEnter Valid Choice!')
                                    break
                    elif(choice==3):
                        while True:
                            try:
                                id=int(input('\nEnter id:'))
                            except Exception as e:
                                print('Id is always Integer!')
                            else:
                                password=maskpass.askpass('Enter password:','*')
                                
                                if(Employee.isEmployeeAdmin(id,password)==False):
                                    print('\nInvalid credentials/Not an Admin')

                                    reset_pass=input('\nWant to reset password?(y/n):')

                                    if reset_pass=='y' or reset_pass=='Y':
                                        while True:
                                            try:
                                                reset_id=int(input('\nEnter id:'))
                                            except Exception as e:
                                                print('Id is always Integer!')
                                            else:
                                                if(Employee.isIdExist(reset_id)):
                                                    if(Employee.resetPasswordbyId(reset_id)):
                                                        print('Password updated!')
                                                        break
                                                    else:
                                                        print('Password not updated!')
                                                        break
                                                else:
                                                    print('Id doesnot exist')
                                                    break
                                    choice=input('\nDo you want to continue?(y/n):')
                                    if(choice=='Y' or choice=='y'):
                                        pass
                                    else:
                                        break
                                else:
                                    while True:
                                        try:
                                            choice=int(input('\n1.View Profile\n2.Employees\n3.Add Employee\n4.Exit\nEnter choice:'))
                                        except Exception as e:
                                            print('\nInvalid choice!')
                                        else:
                                            if(choice==1):
                                                info=list([Employee.viewProfile(id)])
                                                fields=['A/c No','Id','Name','Gender','Dob','Balance(₹)','isAdmin']
                                                print(tabulate(info,headers=fields,tablefmt='grid',floatfmt=f".{2}f"))

                                                isViewPass=input('Do you want to see your password(y/n):')
                                                if(isViewPass=='Y'or isViewPass=='y'):
                                                    your_pass=list([Employee.getPass(id)])
                                                    fields=['Your Password']
                                                    print(tabulate(your_pass,headers=fields,tablefmt='grid',floatfmt=f".{2}f"))
                                                else:
                                                    pass
                                            elif(choice==2):
                                                employees=Employee.viewEmployees()
                                                fields=['A/c No','Id','Name','Gender','Dob','Balance(₹)','isAdmin']
                                                print(tabulate(employees,headers=fields,tablefmt='grid',floatfmt=f".{2}f"))
                                            elif(choice==3):
                                                E=Employee()
                                                isEmployeeAdded=E.inputEmployee(False)
                                                if(isEmployeeAdded):
                                                    print('Employee added!')
                                                else:
                                                    print('Employee not added!')
                                            elif(choice==4):
                                                break
                                    break
                    elif(choice==4):
                        break
                    else:
                        print('\nEnter valid choice!')
    elif choice=='N' or choice=='n':
        while True:
            choice=input('\nAre you sure you want to exit?(y/n):')
            if choice=='Y'or choice=='y':
                Employee.closeConnection()
                MasterAdmin.closeConnection()
                Transaction.closeConnection()
                exit()
            elif choice=='N' or choice=='n':
                break
            else:
                print('\nInvalid Choice')
    else:
        print('\nInvalid choice!')
