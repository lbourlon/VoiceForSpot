from main import isDebugging

"""
This file will contain any utility funtion
"""


def responseDebugg(response, queryName = "None"):
    """Toggleable debug function for responses"""

    if (isDebugging == False) :
        return

    print(queryName + " query reponse : ", end = "")

    if(response.status_code in range(200, 299)):
        print(response.status_code, end = " - OK\n")
        
    else:
        if(response.json()): print(response.json())
    
"""
Splits a text into a list of words.
"""
def slow_split(input_text):
    exit_list = []

    for element in input_text:
        temp_word = ""

        if element != " ":
            temp_word += element
        else:
            exit_list.append(temp_word)

    return exit_list

def get_new_volume(current_volume, option):
    volume = current_volume
    if option == "louder": volume += 20
    elif option == "quieter": volume -= 20

    if volume > 100 : volume = 100
    elif volume < 0 : volume = 0 

    return volume
