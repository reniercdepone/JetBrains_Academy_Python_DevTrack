# Write your code here
import random
import sqlite3

database = sqlite3.connect("card.s3db")
database_cur = database.cursor()
database_cur.execute("DROP TABLE card")
database_cur.execute("CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")


class BankingSystem:
    user_database = {}
    logged_in = False
    user_id = 0
    current_user = ''

    def MainMenu(self):
        while True:
            if self.logged_in == False:
                print("""1. Create an account
    2. Log into account
    0. Exit""")
                user_input = input()
                if user_input == '1':
                    self.createAcct()
                elif user_input == '2':
                    self.login()
                elif user_input == '0':
                    break
            if self.logged_in == True:
                print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
                user_input = input()
                if user_input == '1':
                    self.showBalance()
                if user_input == '2':
                    self.addIncome()
                if user_input == '3':
                    self.doTransfer()
                if user_input == '4':
                    self.closeAcct()
                elif user_input == '5':
                    print("You have successfully logged out!")
                    self.logged_in = False
                elif user_input == '0':
                    break


    def createAcct(self):
        IIN = "400000"
        list_10 = []
        generated_pin = []
        dig_sum = 0
        for i in range(9):
            x = random.randint(0, 9)
            list_10.append(str(x))
        # Luhn's Algorithm to get Last Digit checksum
        list_check = list_10[:]
        for digit in range(9):
            if digit % 2 == 0:
                list_check[digit] = str(int(list_check[digit]) * 2)
        for digit in list_check:
            if int(digit) > 9:
                digit = str(int(digit) - 9)
            dig_sum += int(digit)
        checksum_digit = (dig_sum + 8) % 10
        if checksum_digit != 0:
            checksum_digit = 10 - checksum_digit


        CardNum = IIN + ''.join(list_10) + str(checksum_digit)

        for i in range(4):
            y = random.randint(0, 9)
            generated_pin.append(str(y))
        CardPin = ''.join(generated_pin)

        print("Your card has been created")
        print("Your card number:")
        print(CardNum)
        print('Your card PIN:')
        print(CardPin)

        database_cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (self.user_id, CardNum, CardPin, 0))
        self.user_id += 1
        database.commit()
        self.user_database[CardNum] = CardPin

    def login(self):
        print("Enter your card number:")
        userCard = input("")
        print("\nEnter your PIN:")
        userPin = input()
        # database_cur.execute("SELECT number, pin FROM card")
        # user_number_pin = database_cur.fetchall()
        # if userCard not in user_number_pin:
        #     print("Wrong card number or PIN!")
        if userCard not in self.user_database:
            print("Wrong card number or PIN!")
        elif userPin != self.user_database[userCard]:
            print("Wrong card number or PIN!")
        else:
            print("\nYou have successfully logged in!")
            self.logged_in = True
            self.current_user = userCard

    def showBalance(self):
        database_cur.execute(f"SELECT balance FROM card WHERE number={self.current_user}")
        bal = database_cur.fetchone()
        print(f"Balance: {bal}")

    def closeAcct(self):
        database_cur.execute("DELETE FROM card WHERE number=(?)", (self.current_user,))
        database.commit()
        self.logged_in = False
        print("The account has been closed!")

    def addIncome(self):
        print("Enter income:")
        income = int(input())
        database_cur.execute("UPDATE card SET balance= (balance + (?)) WHERE number=(?)", (income, self.current_user))
        database.commit()
        print("Income was added!")


    def doTransfer(self):
        print("Transfer")
        print("Enter card number:")
        card2 = input()

        if card2 == self.current_user:
            print("You can't transfer money to the same account!")
            return 1

        # Luhn's Algorithm
        list_10 = list(card2[6:15])
        IIN = "400000"
        dig_sum = 0
        # Luhn's Algorithm to get Last Digit checksum
        list_check = list_10[:]
        for digit in range(9):
            if digit % 2 == 0:
                list_check[digit] = str(int(list_check[digit]) * 2)
        for digit in list_check:
            if int(digit) > 9:
                digit = str(int(digit) - 9)
            dig_sum += int(digit)
        checksum_digit = (dig_sum + 8) % 10
        if checksum_digit != 0:
            checksum_digit = 10 - checksum_digit
        CardNum2 = IIN + ''.join(list_10) + str(checksum_digit)

        database_cur.execute("SELECT number FROM card")
        card_database = database_cur.fetchall()

        if str(checksum_digit) != card2[-1] and card2[:6] == IIN:
            print("Probably you made mistake in the card number. Please try again!")
            return 1

        if card2 not in self.user_database:
            print("Such a card does not exist.")
            return 1
        # Success check
        database_cur.execute("SELECT number, balance FROM card WHERE number=(?)", (self.current_user,))
        bal = database_cur.fetchone()
        print("Enter how much money you want to transfer:")
        to_transfer = input()
        if int(to_transfer) > int(bal[1]):
            print("Not enough money!")
            return 1
        new_money = str(int(bal[1]) - int(to_transfer))
        database_cur.execute("UPDATE card SET balance=(?) WHERE number=(?)", (new_money, self.current_user))
        database_cur.execute("UPDATE card SET balance=(?) WHERE number=(?)", (to_transfer, card2))
        database.commit()
        print("Success!")







BDO = BankingSystem()
BDO.MainMenu()


