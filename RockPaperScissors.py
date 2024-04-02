import random
import os
liste = ["Rock", "Paper", "Scissors"]

while True :
    user_input = input("Rock , Paper , Scissors ? :").capitalize()
    computer = random.choice(liste)
    if user_input in liste:
        if computer == "Rock" and user_input == "Paper":
            print(f"Computer chose {computer}")
            print("Congratulations!, you win!")
        elif computer == "Rock" and user_input == "Scissors":
            print(f"Computer chose {computer}")
            print("Sorry , You lose")
        elif computer == "Paper" and user_input == "Rock":
            print(f"Computer chose {computer}")
            print("Sorry , You lose")
        elif computer == "Paper" and user_input == "Scissors":
            print(f"Computer chose {computer}")
            print("Congratulations!, you win!")
        elif computer == "Scissors" and user_input == "Rock":
            print(f"Computer chose {computer}")
            print("Congratulations!, you win!")
        elif computer == "Scissors" and user_input == "Paper":
            print(f"Computer chose {computer}")
            print("Sorry , You lose")
        else:
            print(f"Computer chose {computer}")
            print("Equality")
        x = input("Do you want to contunie , Yes or No ?").capitalize()
        while x not in ["Yes","No"]:
            os.system("cls")
            print("invalide option please try again")
            x = input("Do you want to contunie , Yes or No ?")
        if x in ["Yes","No"]:
            if x == "Yes":
                continue
            else:
                break
    else:
        os.system("cls")
        print("Invalid option")
