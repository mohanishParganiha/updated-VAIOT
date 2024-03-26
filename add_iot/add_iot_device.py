import json

# Function to generate a new IoT device entry
def generate_device_entry(device_id, device_type, protocol, ip_address):
    return {
        "id": device_id,
        "type": device_type,
        "protocol": protocol,
        "ip_address": ip_address
    }

# Function to add a new device entry to the JSON file
def add_device_entry(device_entry, json_file):
    try:
        with open(json_file, 'r+') as file:
            data = json.load(file)
            # Check if device ID and IP address combination already exists
            for entry in data:
                if entry['id'] == device_entry['id'] or entry['ip_address'] == device_entry['ip_address']:
                    return ("Error: Device ID or IP address combination already exists.")
            data.append(device_entry)
            file.seek(0)
            json.dump(data, file, indent=4)
            return 0
    except FileNotFoundError:
        return("Error: JSON file not found.")
    except json.JSONDecodeError:
        return("Error: Unable to decode JSON data.")
    except Exception as e:
        return(f"An unexpected error occurred: {str(e)}") 
        
# Main function to add a new device entry
# def main():
#     # Get input from user
#     device_id = input("Enter ID (name) of the device: ")
#     device_type = input("Enter type of device: ")
#     protocol = input("Enter protocol of device: ")
#     ip_address = input("Enter IP address of the device: ")

#     # Generate new device entry
#     new_device_entry = generate_device_entry(device_id, device_type, protocol, ip_address)

#     # Add the new device entry to the JSON file
#     add_device_entry(new_device_entry, 'iot_device.json')

#     print("New device entry added successfully.")

# if __name__ == "__main__":
#     main()
