import random


class RPSGame:
    choice = ['rock', 'scissors', 'paper']

    def main_menu(self):
        username = self.greet()
        starting_rating = self.check_user_in_rating(username)
        choice_list = self.get_choices()
        print("Okay, let's start")
        while True:
            user_choice = self.UI()
            if user_choice == '!exit':
                print("Bye!")
                break
            if user_choice == '!rating':
                print(f"Your rating: {starting_rating}")
                continue

            bot_choice = random.choice(choice_list)
            result = self.determine_winner(user_choice, bot_choice, choice_list)
            starting_rating = self.update_rating(starting_rating, result)
            self.print_result(bot_choice, result)

    def get_choices(self):
        uinput = input()
        if uinput == '':
            return self.choice
        choice_list = uinput.split(',')
        return choice_list

    def update_rating(self, rating, result):
        new_rating = rating
        if result == 'win':
            new_rating += 100
        elif result == 'draw':
            new_rating += 50
        return new_rating

    def greet(self):
        name = input('Enter your name: ')
        print("Hello, " + name)
        return name

    def check_user_in_rating(self, username):
        user_rating_dict = {}
        rating = open("rating.txt", 'r')
        for line in rating:
            name, value = line.split()
            value = value.rstrip('\n')
            user_rating_dict[name] = (int(value))
        rating.close()
        if username in user_rating_dict:
            return user_rating_dict[username]
        else:
            return 0

    def UI(self):
        ui = input()
        return ui

    def determine_winner(self, user_choice, bot_choice, choice_list):
        if user_choice not in choice_list:
            return 'invalid'
        if user_choice == bot_choice:
            return 'draw'
        if choice_list == self.choice:
            if user_choice == 'rock':
                if bot_choice == 'paper':
                    return 'lose'
                return 'win'
            if user_choice == 'paper':
                if bot_choice == 'scissors':
                    return 'lose'
                return 'win'
            if user_choice == 'scissors':
                if bot_choice == 'rock':
                    return 'lose'
                return 'win'
        x = choice_list.index(user_choice)
        new_choices = choice_list[x:]
        new_choices.extend(choice_list[:x])
        del new_choices[0]
        half_len = (len(new_choices) // 2)
        bot_choice_index = new_choices.index(bot_choice)
        if bot_choice_index < half_len:
            return 'lose'
        else:
            return 'win'

    def print_result(self, bot_choice, result):
        if result == 'win':
            print(f"Well done. Computer chose {bot_choice} and failed")
        elif result == 'lose':
            print(f"Sorry but computer chose {bot_choice}")
        elif result == 'draw':
            print(f"There is a draw ({bot_choice})")
        elif result == 'invalid':
            print("Invalid input")



game = RPSGame()
game.main_menu()
