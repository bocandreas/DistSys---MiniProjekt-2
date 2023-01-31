from aiohttp import web
import requests
import random
import time
import datetime
from multiprocessing import Process, Queue

routes = web.RouteTableDef()
@routes.post("/client_content")
async def client_content(request):
    data = await request.json()
    #print(data)
    
    for dictionary in data:
        #print(dictionary)
        #print(dictionary['code'])
        pass
    dictionary = dictionary["code"]
    
    processes = []
    q = Queue()
    num_workers = random.choice([5,11])
        
    for i in range(num_workers):
        create_worker(i, processes, q, dictionary)
    start_workers(processes, q)
    
    for i, dictionary in enumerate(data):
        processes = []
        create_worker(i, processes, q, dictionary["code"])
        start_workers(processes, q)

    return web.json_response(status=200)

def worker_func(worker_id, d, q):
    time.sleep(random.uniform(0.1, 0.3))
    total_words = 0
    for string in d:
        words = string.split()
        num_words = len(words)
        total_words += num_words

    worker_data = {"worker_id": worker_id, "result": total_words}
    q.put(worker_data)

def create_worker(worker_id, processes, q, dictionary):
    d = dictionary
    p = Process(target=worker_func, args=(worker_id, d, q))
    processes.append(p)

def start_workers(processes, q):
    num_sent_tasks = 0
    num_received_tasks = 0
    for p in processes:
        p.start()
        num_sent_tasks += 1
        print(f"{datetime.datetime.now()} - Sent task to worker {p.pid}, total sent tasks: {num_sent_tasks}")
    for p in processes:
        p.join()
        num_received_tasks += 1
        result = q.get()
        print(f"{datetime.datetime.now()} - Received result from worker {result['worker_id']}, total received tasks: {num_received_tasks}. Number of words in dict is: {result['result']}")

if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.post("/client_content", client_content)])
    web.run_app(app, host="127.0.0.1", port=8081)
