from isnumber import is_user_input_a_number  # import function to check input


def tower_of_hanoi():
    n = int(is_user_input_a_number())  # converting result of function to an integer
    print(f"You need {str((2**n-1))} turns.")  # printing calculated number of turns casted into a string


tower_of_hanoi()
