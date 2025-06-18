import random

computer = random.randint(0, 2)
try:
    user = int(input("Enter 0 for Stone, 1 for Paper, and 2 for Scissor:"))
    if user not in [0, 1, 2]:
       raise ValueError
except:
    print("Invaild Input, Please enter numbers from 0, 1, or 2")
    exit()

choices = ["Stone", "Paper", "Scissor"]
def game(computer, user):

    if (computer==user):
        return 0
    elif (computer==0 and user==1):
        return 1
    elif (computer==0 and user==2):
        return -1
    elif (computer==1 and user==2):
        return -1
    elif (computer==1 and user==0):
        return -1
    elif (computer==2 and user==0):
        return 1
    elif (computer==2 and user==1):
        return -1

print("Computer's choice is:", choices[computer])
print("Your choice:", choices[user])

a = game(computer, user)
if (a==0):
    print("It is a draw")
elif (a==-1):
    print("You Win!")
elif (a==1):
    print("You Lose!")