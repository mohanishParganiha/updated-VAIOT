from typing import Any
import speech_recognition as sr
from multiprocessing import Lock, Process, Queue

class Listening:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.lock = Lock()
        self.text = 'none'
        self.start_event = True

    def listen(self, listener_in):
        if self.start_event:
            try:
                with sr.Microphone() as mic:
                    print('listening....')
                    audio = self.recognizer.listen(mic)
                    if audio is None:
                        pass
                try:
                    self.text = self.recognizer.recognize_google(audio)

                except sr.UnknownValueError:
                    self.text = 'none'

                except sr.RequestError as e:
                    print(e)
                except Exception:
                    print('error')

                with self.lock:
                    print("listener heard",self.text)
                listener_in.send(self.text)
        
            except StopListeningException:
                print('listening stopped')

        return self.text

    # def start_listening(self):
    #     self.isListening = True
    #     print("starting listener function",self.isListening)
    # def stop_listening(self):
    #     self.isListening = False
    #     print("stoping listener function",self.isListening)


class StopListeningException(Exception):
    pass


class StopSpeakingException(Exception):
    pass




# def speaker(queue: Queue):
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 135)
#     # isSpeakerRunning = status
#     while True:
#         try:
#             text = queue.get()
#             if not text is None:
#                 engine.say(text)
#                 print('speaker said:', text)
#                 # Wait for the speech to complete, timeout after 10 seconds
#                 engine.runAndWait()
#                 engine.stop()
#             else:
#                 print("queue is empty")

#         except StopSpeakingException:
#             print('speaking stopped')

#         except Exception as e:
#             print("execption occured:", e)

# class Speaker:
#     def __init__(self):
#         self.queue = Queue()
#         self.engine = pyttsx3.init()
#         self.engine.setProperty('rate', 135)
#         self.is_running = False

#     def start(self):
#         self.is_running = True
#         self.process = Process(target=self._run)
#         self.process.start()

#     def stop(self):
#         self.is_running = False
#         self.process.join()

#     def _run(self):
#         while self.is_running:
#             try:
#                 text = self.queue.get()
#                 if text == "goodbye":
#                     break
#                 if text is not None:
#                     self.engine.say(text)
#                     print('speaker said:', text)
#                     self.engine.runAndWait()
#                     self.engine.stop()
#             except Exception as e:
#                 print('Exception occurred:', e)

#     def add_text(self, text):
#         self.queue.put(text)


def stop_speaking():
    raise StopSpeakingException

# class speakerProcess(Process):
#     def __init__(self,queue:Queue) -> None:
#         super().__init__()
#         self.queue = queue
#         self.isSpeakerRunning = False
#         self.engine = pyttsx3.init()

#     def run(self):
#         while self.isSpeakerRunning:
#             text = self.queue.get()
#             try:
#                 self.engine.say(text)
#                 print('speaker said:',text)
#                 self.engine.runAndWait()
#                 self.engine.stop()

#             except StopSpeakingException:
#                 print('speaking stopped')

#             except Exception:
#                 pass


# while True:
#     try:
#         data = self.input_conn.recv()
#         if data is None:
#             continue
#         if data == "stopListening":
#             break
#         with self.lock:
#             print("speaker :", data)

#     except Exception:
#         pass


# if __name__ =="__main__":
#     regconizer = sr.Recognizer()
#     while True:
#         with sr.Microphone() as mic:
#             audio = regconizer.listen(mic)
#         try:
#             text = regconizer.recognize_google(audio)
#         except Exception as e:
#             print
