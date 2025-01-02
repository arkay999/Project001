# {Banking System},{Author-Arkay}
from colorama import Fore, Back, Style, init
init()
import time
import random
import hashlib
import os


def Main_menu():
    while True:
          print(Style.DIM + Fore.MAGENTA + "Welcome to Arkay Banking System" + Style.RESET_ALL)
          print()
          print("1. Create Account.")
          print("2. Login.")
          print("3. Exit")
          print()
          choice=input("Enter your choice:")
          if choice=="1":
             Create_Acc()
          elif choice=="2":
             username = Login()
             if username:
               User_dashboard(username)
          elif choice=="3":
            print("Thankyou for using Arkay Banking system! Goodbye!")
            break
          else:
            print("Please enter valid choice!")
                     
def hash_password(password):
   salt=os.urandom(32)
   hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
   return salt + hashed_password 
 
def verify_password(stored_password, entered_password):
    salt = stored_password[:32]  
    stored_hash = stored_password[32:]  
    entered_hash = hashlib.pbkdf2_hmac('sha256', entered_password.encode('utf-8'), salt, 100000)  # Hash the entered password with the same salt
    return stored_hash == entered_hash   
    
def Create_Acc():
    print("__Create new account__")
    name=input("Enter your Name:")
    while True:
         username=input("Enter your Username:")
         with open("accounts.txt","a+") as acc:
             acc.seek(0)
             accounts= acc.readlines()
             if any (username in account for account in accounts):
                 print("username already taken, try another one!")
             else:
                 break
    while True:         
        password=input("Enter your password:")
        confirm_password=input("Confirm your Password:")
        if password==confirm_password:
          break
        else:
            print("Password does not match!")
    salt = os.urandom(16)  # 16-byte random salt
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    # Store salt and hashed password in the file as strings (hexadecimal representation)
    salt_hex = salt.hex()  # Convert to hex string for easy storage
    hashed_password_hex = hashed_password.hex()  # Convert hash to hex string
  
            
    initial_amount= 0
    account_number=acc_no()
   
    with open("accounts.txt","a") as acc :
        acc.write(f"{account_number},{name},{username},{salt_hex},{hashed_password_hex},{initial_amount}\n")
        print("Account created succesfully!")
        print(f"Your Account number is: {account_number} ")
          
def acc_no():
    account_number=random.randint(1000,9999)
    with open("accounts.txt","r") as acc:
        accounts=acc.readlines()
        used_acc_nums=[line.split(",")[0] for line in accounts]
        while str(account_number)  in used_acc_nums:
            account_number=random.randint(1000,9999)
    return account_number
        
def Login():
   while True: 
       print("__Login to your Account__")
       username=input("Enter username:")
       password=input("Enter Password:")
       with open("accounts.txt","r") as acc:
           accounts=acc.readlines()
           for account in accounts:
               account_data= account.strip().split(",")
               if username == account_data[2]:
                    # Retrieve the salt and hashed password stored in the file
                    salt = bytes.fromhex(account_data[3])  # Convert from hex back to bytes
                    stored_hash = bytes.fromhex(account_data[4])  # Convert from hex back to bytes
                    
                    # Hash the entered password with the stored salt
                    entered_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
                    current_balance = float(account_data[5]) 
                    print("Login succesfully!")
                    print(f"Welcome:{account_data[1]}, (Current Balance: ₹{account_data[5]}) ")
                    return username
              
           print("Invalid credentials")
              
def User_dashboard(username):
    while True:
        print("__User Dashboard__")
        print("1. Check Balance.")
        print("2. Deposite.")
        print("3. Withdraw.")
        print("4. Transaction Log.")
        print("5. Log out")
        choice2=input("Enter your choice:")
        if choice2=="1":
            check_balance(username)
          
        elif choice2=="2":
            amount=input("Enter your Amount:")
            deposite(username,amount)
        elif choice2=="3":
            amount=input("Enter your Amount:")
            withdraw(username,amount)
        elif choice2=="4":
            trx_log(username)
        elif choice2=="5":
            print("Logging Out.....Goodbye")
            break
        else:
            print("Invalid choice!")
    
def deposite(username,amount):
    amount=float(amount)
    if amount<0:
        print("invalid amount")
        return
    updated=False
    new_account=[]
    with open("accounts.txt","r") as acc:
        accounts=acc.readlines()
        for account in accounts:
            account_data=account.strip().split(",")
            if account_data[2]==username:
                current_balnce=float(account_data[5])
                new_balance=current_balnce+amount
                account_data[5]=str(new_balance)
                updated=True
                print(f"Current balance is: ₹{new_balance}")
                print("Transaction Successfull !")
            new_account.append(",".join(account_data))
    if updated:
        with open("accounts.txt","w")as acc:
            acc.writelines("\n".join(new_account)+"\n")
        with open("transaction.txt","a") as trx:
            trx.write(f"{username},deposit,{amount},{time.strftime('%Y-%m-%d %H:%M:%S')}, **Transaction successfull** \n")
    else:
        print("Deposite failed")
                   
def withdraw(username,amount):
    amount=float(amount)
    if amount<0:
        print("Invalid amount")
        return
    updated=False
    new_account=[]
    with open("accounts.txt","r") as acc:
        accounts=acc.readlines()
        for account in accounts:
            account_data=account.strip().split(",")
            if account_data[2]==username:
                current_balance=float(account_data[5])
                if current_balance>=amount:
                    new_balance=current_balance-amount
                    account_data[5]=str(new_balance )
                    updated=True
                    
                    print(f"Withdrawl sucessfull, current balance is: ₹{new_balance}")
                    print("Transaction successfull !")
               
                
                else:
                    print("Insufficient balance!")
                    return
                new_account.append(",".join(account_data))
            
    if updated:
        with open("accounts.txt","w") as acc:
            acc.writelines("\n".join(new_account) + "\n")
        with open("transaction.txt", "a") as trx:
            trx.write(f"{username},withdraw,{amount},{time.strftime('%Y-%m-%d %H:%M:%S')},**Transaction successfull** \n")
    else:
        print("Account not found! Withdrawal failed.")
                    
def check_balance(username):
    with open("accounts.txt","r") as acc:
        accounts= acc.readlines()
        for account in accounts:
            account_data=account.strip().split(",")
            stored_username=account_data[2]
            if username == stored_username:
                current_balance=account_data[5]
                print(f"Your current balance is: ₹{current_balance}")
                return current_balance
    
def trx_log(username):
    print(f"Transaction Log for user:{username}")
    try:
        with open("transaction.txt","r") as trx:
            for transaction in trx:
                if transaction.startswith(username+","):
                    print(transaction.strip())
    except FileNotFoundError:
        print("Transaction file not found")
    
Main_menu()
    



                             
                       
                         
                 
                
                         
                
                                
                            
                               
                          
                               
                           
                          
                           
                           
                     
                 
                 
                       
            
             
     
             
