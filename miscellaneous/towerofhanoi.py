# import function to check input
from miscellaneous.isnumber import is_user_input_a_number


def tower_of_hanoi():
    # converting result of function to an integer
    n = int(is_user_input_a_number())
    # printing calculated number of turns casted into a string
    print(f"You need {str((2**n-1))} turns.")


tower_of_hanoi()
