from multiprocessing import Process,Pipe,Queue,Lock,Event
from listen_and_speak import Listening 
import pyttsx3
import requests
import webbrowser
from urllib.parse import quote
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


from iot_device_controller import perform_action
from gui.main_window_design_3 import Ui_MainWindow

class requestNLU:
    def __init__(self,start_event) -> None:
        self.lock = Lock()
        self.start_event = start_event

    def send_and_get(self,listener_in,logic_out):
        while True:
           
            if self.start_event.is_set():
                try:
                    message = listener_in.recv()
                except Exception as e:
                    print(e)
                
                if message != 'none':
                    message = message.strip()
                    result = requests.post('http://localhost:5005/model/parse',json={'text':message}).json()
                    intent = result['intent']['name']
                    entities = result['entities']
                    entity_value = []
                    for e in entities:
                        entity_value.append({e['entity']:e['value']})
                    
                    # print(entity_value)
                    logic_out.send([intent,entity_value])

   


class VA:

    def __init__(self,start_event) -> None:
        self.lock = Lock()
        self.start_event = start_event

    def va(self,logic_in,speaker_in):  
        while True:
           
            if self.start_event.is_set():
                dataReturnedFromNlu = logic_in.recv()
                intent = dataReturnedFromNlu[0]
                # print(intent)
                # query = listener_out_queue.get()
                if intent == "greet" :
                    speaker_in.send('hello, how can i help you?')
                    count = 0
                    while count <8:
                        #check the output from nlu again
                        dataReturnedFromNlu = logic_in.recv()
                        intent = dataReturnedFromNlu[0]
                        entity = dataReturnedFromNlu[1]
                        print(entity)
                        # print(intent)

                        if intent == "goodbye" :
                            speaker_in.send('have a good day')
                            break
                        elif intent == "question_asked" :
                            speaker_in.send('question asked')

                        elif intent == "get_current_weather" :
                            speaker_in.send('getting current weather')

                        elif intent == "get_weather_tomorrow" :
                            speaker_in.send("gettign tomorrow's weather")

                        elif intent == "get_weather_forecast" :
                            speaker_in.send('getting weather forecast')

                        elif intent == "get_news" :
                            speaker_in.send('getting news')

                        elif intent == "get_news_category" :
                            speaker_in.send('getting news by catergory')

                        elif intent == "make_list" :
                            speaker_in.send('making a list')

                        elif intent == "take_notes" :
                            speaker_in.send('taking notes')

                        elif intent == "open_app" :
                            speaker_in.send('opening app')

                        elif intent == "open_file" :
                            speaker_in.send('opening file')

                        elif intent == "visit_page" :
                            speaker_in.send('visiting page')

                        elif intent == "search" :
                            speaker_in.send('searching ')

                        elif intent == "send_social_media_message" :
                            speaker_in.send('sending social message on social media')

                        elif intent == "send_text_message" :
                            speaker_in.send('sending text message ')

                        elif intent == "send_email" :
                            speaker_in.send('sending email')

                        elif intent == 'set_alarm':
                            speaker_in.send('setting alarm')

                        elif intent == 'check_alarms':
                            speaker_in.send('checking alarms')

                        elif intent == 'delete_alarm':
                            speaker_in.send('deleting alarm')

                        elif intent == 'light_on':
                            speaker_in.send(f'turning on the {entity[0]["device"]}')
                            perform_action(entity[0]["device"],'light_on')

                        elif intent == 'light_off':
                            speaker_in.send(f'turning off the {entity[0]["device"]}')
                            perform_action(entity[0]["device"],'light_off')

                        elif intent == 'light_change_color':
                            speaker_in.send(f'changing the color of {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'light_change_color')


                        elif intent == 'light_change_brightness':
                            speaker_in.send(f'adjusting the brightness of the {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'light_change_brightness')


                        elif intent == 'fan_on':
                            speaker_in.send(f'turning on the {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'fan_on')


                        elif intent == 'fan_off':
                            speaker_in.send(f'turning off the {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'fan_off')


                        elif intent == 'fan_speed_set':
                            speaker_in.send(f'setting the {entity[0]["device"]} speed')
                            # perform_action(entity[0]["device"],'fan_speed_set')


                        elif intent == 'fan_speed_medium':
                            speaker_in.send(f'setting the {entity[0]["device"]} speed to medium')
                            # perform_action(entity[0]["device"],'fan_speed_medium')


                        elif intent == 'fan_speed_up':
                            speaker_in.send(f'increasing the {entity[0]["device"]} speed')
                            # perform_action(entity[0]["device"],'fan_speed_up')


                        elif intent == 'fan_speed_down':
                            speaker_in.send(f'reducing the {entity[0]["device"]} speed')
                            # perform_action(entity[0]["device"],'fan_speed_down')


                        elif intent == 'tv_on':
                            speaker_in.send(f'turning on the {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'tv_on')

                    #change form here needed in entity -----------------------------------------
                        elif intent == 'tv_off':
                            speaker_in.send(f'turning off the {entity[0]}')
                            # perform_action(entity[0],'tv_off')


                        elif intent == 'tv_channel':
                            speaker_in.send(f'changing the {entity[0]} channel')
                            # perform_action(entity[0],'tv_channel')


                        elif intent == 'tv_volume_medium':
                            speaker_in.send(f'setting the {entity[0]} volume to medium')
                            # perform_action(entity[0],'tv_volume_medium')


                        elif intent == 'tv_volume_up':
                            speaker_in.send(f'increasing the {entity[0]} volume')
                            # perform_action(entity[0],'tv_volume_up')


                        elif intent == 'tv_volume_down':
                            speaker_in.send(f'reducing the {entity[0]} volume')
                            # perform_action(entity[0],'tv_volume_down')


                        elif intent == 'tv_app':
                            speaker_in.send(f'opening the {entity[0]} application')
                            # perform_action(entity[0],'tv_app')


                        elif intent == 'tv_mute':
                            speaker_in.send(f'muting the {entity[0]}')
                            # perform_action(entity[0],'tv_mute')


                        elif intent == 'smart_switch_on':
                            speaker_in.send(f'turning on the {entity[0]}')
                            # perform_action(entity[0],'smart_switch_on')


                        elif intent == 'smart_switch_off':
                            speaker_in.send(f'turning off the {entity[0]}')
                            # perform_action(entity[0],'smart_switch_off')


                        elif intent == 'smart_switch_status':
                            speaker_in.send(f'checking the status of the {entity[0]}')
                            # perform_action(entity[0],'smart_switch_status')


                        elif intent == 'iot_query':
                            speaker_in.send(f'querying the {entity[0]}')
                            # perform_action(entity[0],'iot_query')


                        elif intent == 'iot_device_on':
                            speaker_in.send(f'turning on the {entity[0]}')
                            # perform_action(entity[0],'iot_device_on')


                        elif intent == 'iot_device_off':
                            speaker_in.send(f'turning off the {entity[0]}')
                            # perform_action(entity[0],'iot_device_off')


                        elif intent == 'iot_device_status':
                            speaker_in.send(f'checking the status of the {entity[0]}')
                            # perform_action(entity[0],'iot_device_status')



                        else:
                            count += 1


    


class Speaker:
    def __init__(self,start_event) -> None:
        self.isSpeakerRunning: bool = False
        self.lock = Lock()
        self.start_event = start_event

    def send_text_to_speaker(self,speaker_out):
        engine = pyttsx3.init()
        engine.setProperty('rate', 200)
        while True:
            if self.start_event.is_set():
                try:
                    text = speaker_out.recv()
                except Exception as e:
                    print(e)
                # text = speaker_queue.get()
                if text:
                    engine.say(text)
                    engine.runAndWait()
                    engine.stop()
                    text = None
    
    


def set_start_event(event):
    if event.is_set():
        event.clear()
    else:
        event.set()

if __name__ == "__main__":
    start_event = Event()
    # data_queue = Queue()
    listener = Listening(start_event=start_event)

    Va = VA(start_event=start_event)

    speaker = Speaker(start_event=start_event)

    request_nlu = requestNLU(start_event=start_event)

    listener_out,listener_in = Pipe()
    speaker_out,speaker_in = Pipe()
    listener_out_queue = Queue()
    logic_in,logic_out = Pipe()

    listener_process = Process(target=listener.listen,args=(listener_out,listener_out_queue))
    nlu_process = Process(target=request_nlu.send_and_get,args=(listener_in,logic_out))
    speaker_process = Process(target=speaker.send_text_to_speaker, args=(speaker_out,))
    logic_process = Process(target=Va.va,args=(logic_in,speaker_in))


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    logic_process.start()
    listener_process.start()
    nlu_process.start()
    speaker_process.start()

    ui.pushButton.clicked.connect(lambda:set_start_event(start_event))

    sys.exit(app.exec())
   
   