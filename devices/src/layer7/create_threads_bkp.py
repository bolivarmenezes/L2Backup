import threading


# Creating threads
import time


def create_threads_bkp(list, function):
    threads = []

    for ip in list:
        th = threading.Thread(target=function, args=(ip,))  # args is a tuple with a single element
        time.sleep(2)
        th.start()
        threads.append(th)

    for th in threads:
        th.join()