import time
import speech_recognition as sr
import SpotifyClient
import utility
import string


stop_listening_flag = False

#TODO (on going): Make it listen in the background // use threading?

def recognize():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening (standby)")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print(text)

            
            if (text == "hey John" or text == "hey john"):
                with sr.Microphone() as source2:
                    print("yes?")
                    new_audio = r.listen(source2)
                    

                try:
                    newT = r.recognize_google(new_audio)
                    array = newT.split()

                    if(array[0] == "play"):
                        new_array = " ".join(array[1:])
                        print("Playing " + new_array)

                        # why doesn't this work, why
                        if (new_array != None or new_array != ""):
                            return new_array
                        else : 
                            return "Beneath The Brine"
                except :
                    return "Beneath The Brine"
            else:
                return recognize()
            
        except:
            print("Please repeat")

def recognize2():
  # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening (standby)")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print(text)
            return text
        
        except:
            print("Please repeat")
            return "nope"

"""
This function parses the text_input for the different commands.
It assumes the vocal assistant keyword "Hey John" to be already stripped
from the text data.
"""
def command_parser(text, spot_client):
    
    if (text == "hey John" or text == "hey john"):
        novo_texto = recognize2()
        return command_parser(novo_texto, spot_client)
    

    input_text_list = text.split()

    weather_commands = ["weather"]

    #command_mega_list = [spotify_commands, weather_commands]

    for command in SpotifyClient.spotify_commands:
        if command == input_text_list[0]:
            # TODO: get corresponding function to be called
            spot_client.execute_command(input_text_list)
            return    

    print("nao deu certo brother")
    




#Don't remember this function working, check later
def launch_listening_thread():
    """ Launches another listening thread
        The function returns an array containing the words
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("yes?")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            stop_listening_flag =  True #Tells the program to put the background listening thread back up
            return text
            
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))

        
 


   

#TODO : replace the function above with the code below, still needs testing
def callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio)
        words = text.split()

        for i in range(0, len(words)-1):
            if(words[i] == "hey" and words[i+1] == "John"):
                if(i + 1 == len(words)):
                    #stop background listener
                    stop_listening_flag =  True
                    return_text = launch_listening_thread()
                    return return_text
                else:
                    # TODO : Make a command parser and pass it the rest of the string
                    return words[i + 1:]
            else:
                print("I understood : {}".format() + " no 'Hey John' call.")
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))
    
    

def main():
    isRunning = True
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.2

    mic = sr.Microphone()
    with mic as source:
        print("Getting noise values")
        recognizer.adjust_for_ambient_noise(source, 2)
        print("All set")

    #This line starts a background listening thread, (takes in an audio source and a function to execute)
    #It then returns a function object that when called will stop this background thread
    stop_listening = recognizer.listen_in_background(mic, callback)

    for _ in range(600):
        time.sleep(0.1)  # Random computation, to keep the main thread busy
        if (stop_listening_flag and isRunning):
            print("yep, its the end")
            stop_listening(wait_for_stop=False)
            isRunning = False
        elif (not stop_listening and not isRunning):
            print("re-opening background listening thread")
            stop_listening = recognizer.listen_in_background(mic, callback)
            isRunning = True
    
    print("End of program")
if __name__ == "__main__":
    main()