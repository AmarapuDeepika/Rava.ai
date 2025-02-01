import threading
import os
def task1():
    print("task1 assigned to process: {}".format(threading.current_thread().name))
    print("Id of process running task1: {}".format(os.getpid()))
def task2():
    print("task1 assigned to process: {}".format(threading.current_thread().name))
    print("Id of process running task1: {}".format(os.getpid()))
if __name__ == "__main__":
    print("ID of process running main process: {}".format(os.getpid()))
    print("main thread name: {}".format(threading.current_thread().name))
    t1=threading.Thread(target=task1,name='t1')
    t2=threading.Thread(target=task2,name='t2')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
