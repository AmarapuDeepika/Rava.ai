# from threading import *
# from time import sleep

# class Hello(Thread):
#     def run(self):
#         for i in range(10):
#             print("Hello")
#             sleep(1)
# class Hi(Thread):
#     def run(self):
#         for i in range(10):
#             print("Hi")
#             sleep(1)
# t1=Hello()
# t2=Hi()

# t1.start()
# t2.start()

# t1.join()
# t2.join()
# print("bye")

import threading
def print_cube(num):
    print("cube: {}".format(num,num,num))
def print_square(num):
    print("square: {}".format(num,num))
if __name__ == "__main__":
    t1=threading.Thread(target=print_cube,args=(10,))
    t2=threading.Thread(target=print_square,args=(10,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("bye")
