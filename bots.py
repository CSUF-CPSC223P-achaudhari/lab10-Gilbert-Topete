import threading
import json
from time import sleep


def bot_fetcher(items, cart_list, lock):

    inventory = {}
    with open('inventory.dat','r') as file: 
        inventory = json.load(file)
    
    for key in items:
        value = inventory[key]
        duration = value[1]
        item = value[0]
        sleep(duration)
        lock.acquire()
        cart_list.append([key,item])
        lock.release()

def bot_clerk(items):

    cart_list = []
    rfl1 = []
    rfl2 = []
    rfl3 = []
    lock = threading.Lock()

    for i, key in enumerate(items):
        r_counter = i%3
        if r_counter == 0:
            rfl1.append(key)
        elif r_counter == 1:
            rfl2.append(key)
        elif r_counter == 2:
            rfl3.append(key)

    threads = []
    if len(rfl1) > 0:
        t = threading.Thread(target=bot_fetcher,args=(rfl1 ,cart_list, lock))
        t.start()
        threads.append(t)
    
    if len(rfl2) > 0:
        t = threading.Thread(target=bot_fetcher,args=(rfl2 ,cart_list, lock))
        t.start()
        threads.append(t)

    if len(rfl3) > 0:
        t = threading.Thread(target=bot_fetcher,args=(rfl3 ,cart_list, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    return cart_list
    


