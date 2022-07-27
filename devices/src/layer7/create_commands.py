import threading
import time


# Creating threads
def create_threads(list, function):
    threads = []

    for ip in list:
        # args is a tuple with a single element
        th = threading.Thread(target=function, args=(ip,))
        time.sleep(2)
        th.start()
        threads.append(th)

    for th in threads:
        th.join()
