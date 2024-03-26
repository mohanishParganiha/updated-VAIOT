# from queue import Queue
# from threading import Lock, Thread
# from time import sleep


# class Pipeline:
#     def __init__(self) -> None:
#         self.data = Queue()
#         self.lock = Lock()

#     def setData(self, data)->None:
#         with self.lock:
#             self.data.put(data)

#     def getData(self)->str:
#         with self.lock:
#             data = self.data.get()
#         return data


from multiprocessing import Process, Event,JoinableQueue
from queue import Empty

def listener(q, stop_event):
    while not stop_event.is_set():
        data = input("text: ")
        q.put(data)
        if data == "stopListening":
            break
    stop_event.set()
    

def speaker(q, stop_event):
    while not stop_event.is_set():
            try:
                data = q.get()
                if data is None:
                    continue
                if data == "stopListening":
                    break
                print("speaker received:", data)
            except Exception:
                q.task_done()

if __name__ == "__main__":
    data_queue = JoinableQueue()
    stop_event = Event()
    
    listener_process = Process(target=listener, args=(data_queue, stop_event))
    speaker_process = Process(target=speaker, args=(data_queue, stop_event))

    listener_process.start()
    speaker_process.start()

    listener_process.join()
    speaker_process.join()
