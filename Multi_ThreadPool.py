import concurrent.futures

def worker():
    print("Worker thread is runnig")
pool=concurrent.futures.ThreadPoolExecutor(max_workers=2)
pool.submit(worker)
pool.submit(worker)
pool.shutdown(wait=True)
print("main thread is running")
