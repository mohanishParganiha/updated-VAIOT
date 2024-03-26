import json
import requests

# Function to perform actions based on device type and action
def perform_action(device_id, action, action_value=None):
    # Load devices from JSON file
    with open('iot_device.json', 'r') as file:
        devices = json.load(file)
    
    # Find the device with the given ID
    device = next((d for d in devices if d['id'] == device_id), None)
    if device:
        device_type = device['type']
        ip = device['ip_address']

        if device_type == 'bulb':
            if action == 'turn_on':
                print(f"Bulb {device_id} is turned on")
                perform(ip=ip,endpoint="/led",value=1)

            elif action == 'turn_off':
                print(f"Bulb {device_id} is turned off")
                perform(ip=ip,endpoint="/led",value=0)

            elif action == 'dim':
                if action_value is not None:
                    print(f"Bulb {device_id} is dimmed to {action_value}")
                else:
                    print("Action value is required for dimming action")
            elif action == 'increase_brightness':
                print(f"Bulb {device_id} brightness increased")
            elif action == 'decrease_brightness':
                print(f"Bulb {device_id} brightness decreased")
            else:
                print(f"Unsupported action for Bulb: {action}")
        
        elif device_type == 'fan':
            if action == 'turn_on':
                print(f"Fan {device_id} is turned on")
            elif action == 'turn_off':
                print(f"Fan {device_id} is turned off")
            elif action == 'change_speed':
                if action_value is not None:
                    print(f"Fan {device_id} speed changed to {action_value}")
                else:
                    print("Action value is required for changing fan speed")
            elif action == 'increase_speed':
                print(f"Fan {device_id} speed increased")
            elif action == 'decrease_speed':
                print(f"Fan {device_id} speed decreased")
            else:
                print(f"Unsupported action for Fan: {action}")
       
        elif device_type == 'ac':
            if action == 'turn_on':
                print(f"AC {device_id} is turned on")
            elif action == 'turn_off':
                print(f"AC {device_id} is turned off")
            elif action == 'set_timer':
                print(f"Timer set for AC {device_id}")
            elif action == 'set_temperature':
                if action_value is not None:
                    print(f"AC {device_id} temperature set to {action_value}°C")
                else:
                    print("Action value is required for setting temperature")
            elif action == 'set_speed':
                if action_value is not None:
                    print(f"AC {device_id} fan speed set to {action_value}")
                else:
                    print("Action value is required for setting fan speed")
            elif action == 'set_mode':
                if action_value is not None:
                    print(f"AC {device_id} mode set to {action_value}")
                else:
                    print("Action value is required for setting mode")
            else:
                print(f"Unsupported action for AC: {action}")
        else:
            print(f"Unsupported device type: {device_type}")
    else:
        print(f"Device with ID {device_id} not found")



def perform(ip, endpoint, value):
    base_url = f"http://{ip}"
    url = f"{base_url}{endpoint}?value={value}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Action '{endpoint}' performed successfully")
        else:
            print(f"Failed to perform action '{endpoint}'. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")



# Main function
# def main():
#     # Example usage
#     perform_action('front door camera', 'turn_on')
#     perform_action('living room fan', 'change_speed', 4)
#     perform_action('bedroom ac', 'set_temperature', 25)
#     perform_action('kitchen lights', 'turn_off')
#     perform_action('bedroom ac', 'set_mode', 'cool')

if __name__ == "__main__":
    perform_action('living room light','turn_off')