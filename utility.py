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
    

