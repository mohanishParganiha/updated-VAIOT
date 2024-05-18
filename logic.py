from multiprocessing import Process,Pipe,Queue,Lock,Event
from listen_and_speak import Listening 
import pyttsx3
import requests
import webbrowser
from urllib.parse import quote
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal


from iot_device_controller import perform_action
from gui.main_window_design_3 import Ui_MainWindow
from do_tasks import open_app, search, visit_site, tomorrowsWeather,currentWeather, getNewsByCategory, save_list_to_file, weatherForecastOnSpeceficDay, getNews

class requestNLU():
    def __init__(self,start_event) -> None:
        self.lock = Lock()
        self.start_event = start_event

    def send_and_get(self,listener_in,logic_in):
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
                    logic_in.send([intent,entity_value])

   

class VA():


    def __init__(self,start_event):
        super().__init__()
        self.lock = Lock()
        self.start_event = start_event
        self.listener = Listening()

    def va(self,listener_in,logic_out,speaker_in,print_to_screen_out):  
        while True:
            if self.start_event.is_set():
                #listend and then send input to nlu process
                query = self.listener.listen(listener_in)

                dataReturnedFromNlu = logic_out.recv()
                intent = dataReturnedFromNlu[0]
                if intent == "greet" :
                    print_to_screen_out.send('SAM: hello i am sam , how can i help you?')
                    speaker_in.send('hello i am sam , how can i help you?')
                    count = 0
                    while count <8:
                        #listend and then send input to nlu process
                        query = self.listener.listen(listener_in)

                        #check the output from nlu again
                        dataReturnedFromNlu = logic_out.recv()
                        intent = dataReturnedFromNlu[0]
                        entity = dataReturnedFromNlu[1]

                        print('intent: ',intent)
                        print("entity: ",entity)
                        # print(intent)

                        if intent == "goodbye" :
                            print_to_screen_out.send('SAM: have a good day')
                            speaker_in.send('have a good day')

                            break
                        elif intent == "question_asked" :
                            print_to_screen_out.send('SAM: question asked')
                            speaker_in.send('question asked')

                        elif intent == "get_current_weather" :
                            print_to_screen_out.send('SAM: getting current weather')
                            speaker_in.send('getting current weather')
                            for w in currentWeather():
                                print_to_screen_out.send(w)
                                speaker_in.send(w)


                        elif intent == "get_weather_tomorrow" :
                            print_to_screen_out.send("SAM: gettign tomorrow's weather")
                            speaker_in.send("gettign tomorrow's weather")
                            for w in tomorrowsWeather():
                                print_to_screen_out.send(w)
                                speaker_in.send(w)

                        elif intent == "get_weather_forecast" :
                            print_to_screen_out.send(f'SAM: getting weather forecast for {str(entity[0]["date"])}')
                            speaker_in.send(f'getting weather forecast for {str(entity[0]["date"])}')
                            for w in weatherForecastOnSpeceficDay(str(entity[0]["date"])):
                                print_to_screen_out.send(w)
                                speaker_in.send(w)


                        elif intent == "get_news" :
                            print_to_screen_out.send('SAM: getting news')
                            speaker_in.send('getting news')
                            title, description, sources = getNews()
                            for i in range(3):
                                print_to_screen_out.send(f"SAM: {str(title[i])}    {str(description[i])} by {str(sources[i])}")
                                speaker_in.send(f"{str(title[i])}    {str(description[i])} by {str(sources[i])}")


                        elif intent == "get_news_category" :
                            print_to_screen_out.send(f'SAM: getting news by {entity[0]["topic"]}')
                            speaker_in.send(f'getting news by {entity[0]["topic"]}')
                            title, description, sources = getNewsByCategory(entity[0]['topic'])
                            for i in range(3):
                                print_to_screen_out.send(f"SAM: {str(title[i])}    {str(description[i])} by {str(sources[i])}")
                                speaker_in.send(f"{str(title[i])}    {str(description[i])} by {str(sources[i])}")

                        elif intent == "make_list" :
                            print_to_screen_out.send('SAM: these functionality are currently under development')
                            speaker_in.send('this functionality are currently under development')
                            # speaker_in.send('making a list, please specify the topic of list')
                            # while True:
                            #     query = listener_out_queue.get()
                            #     if query == 'none':
                            #         pass
                            #     else:
                            #         topic = query
                            #         break
                          
                            # items = []
                            # speaker_in.send("Start making the list. When you're done, end it by saying 'end the list' to finish.")
                            # counter = 0
                            # while True:
                            #     query = listener_out_queue.get()
                            #     if query != "none":
                            #         speaker_in.send(f"adding {query} to list")
                            #         items.append(query)
                            #     elif query.lower() == "end_list":
                            #         break
                    
                            #     else:
                            #         counter += 1
                            #         if counter == 3:
                            #             speaker_in.send('sorry looks like you did not want to add any more items , the list is being closed and saved')
                            #             break
                            #         speaker_in.send('sorry I did not understand , could you please repeat')

                            # save_list_to_file(topic, items)


                        elif intent == "take_notes" :
                            print_to_screen_out.send('SAM: these functionality are currently under development')
                            speaker_in.send('these functionality are currently under development')

                        elif intent == "open_app" :
                            print_to_screen_out.send(f'SAM: opening {entity[0]["app_name"]}')
                            speaker_in.send(f'opening {entity[0]["app_name"]}')
                            open_app(entity[0]['app_name'])

                        elif intent == "open_file" :
                            print_to_screen_out.send('SAM: these functionality are currently under development')
                            speaker_in.send('these functionality are currently under development')
                            

                        elif intent == "visit_page" :
                            print_to_screen_out.send(f'SAM: visiting {entity[0]["platform"]}')
                            speaker_in.send(f'visiting {entity[0]["platform"]}')
                            visit_site(entity[0]["platform"])
                            

                        elif intent == "search" :
                            print_to_screen_out.send('SAM: searching')
                            speaker_in.send('searching ')
                            search(engine=entity[1]['app_name'],searchItem=entity[0]['search_item'])
                            

                        elif intent == "send_social_media_message" :
                            print_to_screen_out.send('SAM: these functionality are currently under development')
                            speaker_in.send('these functionality are currently under development')
                            

                        elif intent == "send_text_message" :
                            print_to_screen_out.send('SAM: these functionality are currently under development')
                            speaker_in.send('these functionality are currently under development')
                            

                        elif intent == "send_email" :
                            print_to_screen_out.send('SAM: these functionality are currently under development')
                            speaker_in.send('these functionality are currently under development')
                            

                        elif intent == 'set_alarm':
                            print_to_screen_out.send('SAM: these functionality are currently under development')
                            speaker_in.send('these functionality are currently under development')
                            

                        elif intent == 'check_alarms':
                            print_to_screen_out.send('SAM: these functionality are currently under development')
                            speaker_in.send('these functionality are currently under development')
                            

                        elif intent == 'delete_alarm':
                            print_to_screen_out.send('SAM: these functionality are currently under development')
                            speaker_in.send('these functionality are currently under development')
                            

                        elif intent == 'light_on':
                            print_to_screen_out.send(f'SAM: turning on the {entity[0]["device"]}')
                            speaker_in.send(f'turning on the {entity[0]["device"]}')
                            perform_action(device_id=entity[0]["device"],action='turn_on')

                        elif intent == 'light_off':
                            print_to_screen_out.send(f'SAM: turning off the {entity[0]["device"]}')
                            speaker_in.send(f'turning off the {entity[0]["device"]}')
                            perform_action(device_id=entity[0]["device"],action='turn_off')

                        elif intent == 'light_change_color':
                            print_to_screen_out.send(f'SAM: changing the color of {entity[0]["device"]}')
                            speaker_in.send(f'changing the color of {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'light_change_color')


                        elif intent == 'light_change_brightness':
                            print_to_screen_out.send(f'SAM: adjusting the brightness of the {entity[0]["device"]}')
                            speaker_in.send(f'adjusting the brightness of the {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'light_change_brightness')


                        elif intent == 'fan_on':
                            print_to_screen_out.send(f'SAM: turning on the {entity[0]["device"]}')
                            speaker_in.send(f'turning on the {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'fan_on')


                        elif intent == 'fan_off':
                            print_to_screen_out.send(f'SAM: turning off the {entity[0]["device"]}')
                            speaker_in.send(f'turning off the {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'fan_off')


                        elif intent == 'fan_speed_set':
                            print_to_screen_out.send(f'SAM: setting the {entity[0]["device"]} speed')
                            speaker_in.send(f'setting the {entity[0]["device"]} speed')
                            # perform_action(entity[0]["device"],'fan_speed_set')


                        elif intent == 'fan_speed_medium':
                            print_to_screen_out.send(f'SAM: setting the {entity[0]["device"]} speed to medium')
                            speaker_in.send(f'setting the {entity[0]["device"]} speed to medium')
                            # perform_action(entity[0]["device"],'fan_speed_medium')


                        elif intent == 'fan_speed_up':
                            print_to_screen_out.send(f'SAM: increasing the {entity[0]["device"]} speed')
                            speaker_in.send(f'increasing the {entity[0]["device"]} speed')
                            # perform_action(entity[0]["device"],'fan_speed_up')


                        elif intent == 'fan_speed_down':
                            print_to_screen_out.send(f'SAM: reducing the {entity[0]["device"]} speed')
                            speaker_in.send(f'reducing the {entity[0]["device"]} speed')
                            # perform_action(entity[0]["device"],'fan_speed_down')


                        elif intent == 'tv_on':
                            print_to_screen_out.send(f'SAM: turning on the {entity[0]["device"]}')
                            speaker_in.send(f'turning on the {entity[0]["device"]}')
                            # perform_action(entity[0]["device"],'tv_on')

                    #change form here needed in entity -----------------------------------------
                        elif intent == 'tv_off':
                            print_to_screen_out.send(f'SAM: turning off the {entity[0]}')
                            speaker_in.send(f'turning off the {entity[0]}')
                            # perform_action(entity[0],'tv_off')


                        elif intent == 'tv_channel':
                            print_to_screen_out.send(f'SAM: changing the {entity[0]} channel')
                            speaker_in.send(f'changing the {entity[0]} channel')
                            # perform_action(entity[0],'tv_channel')


                        elif intent == 'tv_volume_medium':
                            print_to_screen_out.send(f'SAM: setting the {entity[0]} volume to medium')
                            speaker_in.send(f'setting the {entity[0]} volume to medium')
                            # perform_action(entity[0],'tv_volume_medium')


                        elif intent == 'tv_volume_up':
                            print_to_screen_out.send(f'SAM: increasing the {entity[0]} volume')
                            speaker_in.send(f'increasing the {entity[0]} volume')
                            # perform_action(entity[0],'tv_volume_up')


                        elif intent == 'tv_volume_down':
                            print_to_screen_out.send(f'SAM: reducing the {entity[0]} volume')
                            speaker_in.send(f'reducing the {entity[0]} volume')
                            # perform_action(entity[0],'tv_volume_down')


                        elif intent == 'tv_app':
                            print_to_screen_out.send(f'SAM: opening the {entity[0]} application')
                            speaker_in.send(f'opening the {entity[0]} application')
                            # perform_action(entity[0],'tv_app')


                        elif intent == 'tv_mute':
                            print_to_screen_out.send(f'SAM: muting the {entity[0]}')
                            speaker_in.send(f'muting the {entity[0]}')
                            # perform_action(entity[0],'tv_mute')


                        elif intent == 'smart_switch_on':
                            print_to_screen_out.send(f'SAM: turning on the {entity[0]}')
                            speaker_in.send(f'turning on the {entity[0]}')
                            # perform_action(entity[0],'smart_switch_on')


                        elif intent == 'smart_switch_off':
                            print_to_screen_out.send(f'SAM: turning off the {entity[0]}')
                            speaker_in.send(f'turning off the {entity[0]}')
                            # perform_action(entity[0],'smart_switch_off')


                        elif intent == 'smart_switch_status':
                            print_to_screen_out.send(f'SAM: checking the status of the {entity[0]}')
                            speaker_in.send(f'checking the status of the {entity[0]}')
                            # perform_action(entity[0],'smart_switch_status')


                        elif intent == 'iot_query':
                            print_to_screen_out.send(f'SAM: querying the {entity[0]}')
                            speaker_in.send(f'querying the {entity[0]}')
                            # perform_action(entity[0],'iot_query')


                        elif intent == 'iot_device_on':
                            print_to_screen_out.send(f'SAM: turning on the {entity[0]}')
                            speaker_in.send(f'turning on the {entity[0]}')
                            # perform_action(entity[0],'iot_device_on')


                        elif intent == 'iot_device_off':
                            print_to_screen_out.send(f'SAM: turning off the {entity[0]}')
                            speaker_in.send(f'turning off the {entity[0]}')
                            # perform_action(entity[0],'iot_device_off')


                        elif intent == 'iot_device_status':
                            print_to_screen_out.send(f'SAM: checking the status of the {entity[0]}')
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
    # listener = Listening(start_event=start_event)

    Va = VA(start_event=start_event)

    speaker = Speaker(start_event=start_event)

    request_nlu = requestNLU(start_event=start_event)

    listener_out,listener_in = Pipe()
    speaker_out,speaker_in = Pipe()
    listener_out_queue = Queue()
    logic_in,logic_out = Pipe()
    data_to_ui,data_from_va = Pipe()
    print_to_screen_in, print_to_screen_out = Pipe()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # listener_process = Process(target=listener.listen,args=(listener_out,listener_out_queue))
    nlu_process = Process(target=request_nlu.send_and_get,args=(listener_out,logic_in))
    speaker_process = Process(target=speaker.send_text_to_speaker, args=(speaker_out,))
    logic_process = Process(target=Va.va,args=(listener_in,logic_out,speaker_in,print_to_screen_in))

 
    
    logic_process.start()
    # listener_process.start()
    nlu_process.start()
    speaker_process.start()

    ui.pushButton.clicked.connect(lambda:set_start_event(start_event))

    def check_pipe_for_screen():
        if print_to_screen_out.poll():
            text = print_to_screen_out.recv()
            ui.progress.emit(text)

    timer = QtCore.QTimer()
    timer.timeout.connect(check_pipe_for_screen)
    timer.start(100)


    sys.exit(app.exec())
   
   