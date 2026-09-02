import os
import platform

def Clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def Menu():
    Clear()
    print("==================")
    print("1.) Create Account")
    print("2.) Login")
    print("3.) Exit")
    print("==================")

    selection = input("\n> ")
    return selection

def Home(username):
    Clear()
    print("===================")
    print(f"Welcome {username}")
    print("===================")
    print("1.) List Accounts")
    print("2.) Create Account")
    print("3.) Modify Account")
    print("4.) Delete Account")
    print("===================")

    selection = input("\n> ")
    return selection

