def is_user_input_a_number():  # function declaration
    number_of_turns = 0
    user_input = input()  # assign user input to a variable
    try:  # try code below
        number_of_turns = int(user_input)
        print("Input is a number")
        # return input casted into integer
    except Exception as error:
        print(f"Input is not a number: {error}")  # if not successfull
    return number_of_turns
