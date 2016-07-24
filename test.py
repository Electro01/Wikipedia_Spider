import threading, queue
import time

dish_queue = queue.Queue()

def putt():
    global dish_queue
    i = 1
    while True:
        dish_queue.put(i)
        i += 1
        time.sleep(4)
        
def gett():
    global dish_queue
    while True:
        dish = dish_queue.get()
        print(dish)

def runn():
    putt_thread = threading.Thread(target = putt)
    #gett_thread = threading.Thread(target = gett)
    putt_thread.start()
    #gett_thread.start()
    gett()

runn()
print("end")