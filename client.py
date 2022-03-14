import time
import requests

def main():
    url = 'https://distributed-systems-project.herokuapp.com/'
    active = True
    player = 1


    while(active):
        counter = 0 
        value = input("Give your answer (Kivi / Paperi / Sakset, 0 = Exit): ")
        if not check_if_player_continues(value):
            return

        if value == "Kivi" or value == "Paperi" or value == "Sakset":
            send_request(url, player, value)
            while(True):
                time.sleep(1)
                counter += 1
                y = requests.get(url)
                print("Waiting for the other player ({}/15)".format(counter))
                if y.text != "Game is still ongoing":
                    print("Getting data: " + y.text)
                    break

                if counter == 15:
                    send_request(url, player, None)
                    print("Timeout")
                    break
        else:
            print("Invalid input, try again")


def check_if_player_continues(msg):
    if msg == "0" or msg == 0:
        active = False
        return False
    return True

def send_request(url, player, value):
    obj = {'player': player, 'value': value}
    x = requests.post(url, json=obj)
    print("Sending data: " + x.text)

if (__name__) == ("__main__"):
    main()