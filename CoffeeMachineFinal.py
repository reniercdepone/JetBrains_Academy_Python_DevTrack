class CoffeeMachine:
    def __init__(self):
        self.money_have = 550
        self.water_have = 400
        self.milk_have = 540
        self.beans_have = 120
        self.cups_have = 9
        self.main_menu()

    def main_menu(self):
        while True:
            action = input("Write action (buy, fill, take, remaining, exit):\n")
            if action == 'buy':
                self.buy()
            elif action == 'fill':
                self.fill()
            elif action == 'take':
                self.take()
            elif action == 'exit':
                break
            elif action == 'remaining':
                self.print_remain()

    def buy(self):
        coffee_type = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - capuccino, back - to main menu:\n")
        # espresso 250ml water, 16g coffee, costs 4 
        if coffee_type == '1':
            if self.water_have < 250 or self.beans_have < 16 or self.cups_have == 0:
                print("Sorry, not enough resources")
                return 1
            self.water_have -= 250
            self.beans_have -= 16
            self.money_have += 4
            self.cups_have -= 1
        # latte 350ml water, 75ml milk, 20g coffee, costs 7
        elif coffee_type == '2':
            if self.water_have < 350 or self.beans_have < 20 or self.cups_have == 0 or self.milk_have < 75:
                print("Sorry, not enough resources")
                return 1
            self.water_have -= 350
            self.milk_have -= 75
            self.beans_have -= 20
            self.money_have += 7
            self.cups_have -= 1
        elif coffee_type == 'back':
            return 1
        # capuccino 200ml water, 100ml milk, 12g coffee, costs 6
        else:
            if self.water_have < 200 or self.beans_have < 12 or self.cups_have == 0 or self.milk_have < 100:
                print("Sorry, not enough resources")
                return 1
            self.water_have -= 200
            self.milk_have -= 100
            self.beans_have -= 12
            self.money_have += 6
            self.cups_have -= 1

    def fill(self):
        self.water_have += int(input("Write how many ml of water to add:\n"))
        self.milk_have += int(input("Write how many ml of milk to add:\n"))
        self.beans_have += int(input("Write how many grams of coffee beans do you want to add:\n"))
        self.cups_have += int(input("Write how many disposable cups do you want to add:\n"))

    def take(self):
        print(f"I gave you ${self.money_have}")
        self.money_have = 0

    def print_remain(self):
        print("")
        print("The coffee machine has:")
        print(f"{self.water_have} of water")
        print(f"{self.milk_have} of milk")
        print(f"{self.beans_have} of coffee beans")
        print(f"{self.cups_have} of disposable cups")
        print(f"${self.money_have} of money")

Vendo = CoffeeMachine()