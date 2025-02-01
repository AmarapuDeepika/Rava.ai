#Regular threads or NON-Daemon threads

import threading
import time

def regular_thread():
    for i in range(5):
        print(f"Regular thread is running: {i}")
        time.sleep(1)

# Create a regular thread
thread = threading.Thread(target=regular_thread)
thread.start()

# Main program waits for the regular thread to finish
print("Main program completed!")
thread.join()


#Daemon threads

# import threading
# import time

# def daemon_thread_task():
#     for i in range(5):
#         print(f"Daemon thread running: {i}")
#         time.sleep(1)

# # Create a daemon thread
# thread = threading.Thread(target=daemon_thread_task)
# # thread.setDaemon(True)
# thread.daemon=True
# thread.start()
# print("Main program completed!")
