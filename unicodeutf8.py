def convert_integer_to_string(intArray):
    combined_binary = ""
    for integer in intArray:
        binary_value = str(bin(integer))
        index_at_ten = binary_value.find("10")
        if index_at_ten < 0:
            index_at_ten = 0
        combined_binary += binary_value[(index_at_ten+2):]    
    combined_binary_as_integer = int(combined_binary,2)
    print(combined_binary,combined_binary_as_integer,chr(combined_binary_as_integer))

def convert_binary_to_string(bin_array):
    combined_binary = ""
    for binary in bin_array:
        index_at_ten = binary.find("10")
        if index_at_ten < 0:
            index_at_ten = 0            
        combined_binary += binary[(index_at_ten+2):]

    combined_binary_as_integer = int(combined_binary,2)
    print(combined_binary,combined_binary_as_integer,chr(combined_binary_as_integer))

def convert_hexadecimal_to_str(hex_value_array):
    combined_bytes = b""
    for hex_value in hex_value_array:
        byte = bytes.fromhex(hex_value[2:])
        combined_bytes += byte

    unicode_string = combined_bytes.decode("UTF-8")

    print(unicode_string)

def convert_char_to_char(string):
    binary_value = bin(ord(string))
    binary_as_integer = int(binary_value,2)
    print(bin(ord(string)),binary_as_integer,chr(binary_as_integer))






convert_integer_to_string([125,255])  
# #Result = ä

convert_binary_to_string(["0b11100010", "0b10000000", "0b10110000"]) 
# #Result = ‰

convert_hexadecimal_to_str(['0xc3', '0xbc']) 
#Result = ü

convert_char_to_char("ÿ")




