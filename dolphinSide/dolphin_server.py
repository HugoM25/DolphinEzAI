
'''
This file is the server that will be used to communicate with the emulator.
'''

import asyncio
import socket
import threading
import queue
from dolphin import event, memory, controller, savestate 
import json
import os
import inspect

'''
Global variables
----------------
'''

# The queue that will be used to store the inputs to execute at the next frame
input_action_queue = queue.Queue()

# Initialize the current inputs list
gc_inputs_controllers = [ controller.get_gc_buttons(0), controller.get_gc_buttons(1), controller.get_gc_buttons(2), controller.get_gc_buttons(3) ]

# Get the script directory
script_directory = os.path.abspath(inspect.getsourcefile(lambda:0)).replace("dolphin_server.py", "")

# The memory adresses to watch (this will be populated using the csv next to this file)
memory_adresses_to_watch = {}

'''
Functions for the setup of the server
-------------------------------------
'''

def load_memory_adresses_to_watch() -> bool:
    '''
    Get the memory adresses to watch from the csv next to this file
    The csv file is formatted like this :
    <name>,<type>,<adress>,<description>
    @return: True if the csv was found and read, False otherwise
    '''

    csv_path = script_directory + "watch_list.csv"
    with open(csv_path, "r") as csv_file:
        # Read the csv file (skip the first line because it's the header)
        csv_file.readline()
        for line in csv_file.readlines():
            # Split the line
            splitted_line = line.split(",")
            # Get the name
            name = splitted_line[0]
            # Get the type
            type = splitted_line[1]
            # Get the adress
            adress = splitted_line[2]
            # Get the description
            #description = splitted_line[3]
            # Add the adress to the memory adress to watch
            memory_adresses_to_watch[name] = {"type":type, "adress":adress}
    
    if len(memory_adresses_to_watch) == 0 :
        return False
    return True

def load_config() -> bool:
    '''
    Load the config file
    @return: True if the config file was found and is valid, False otherwise
    '''
    config_path = script_directory + "config.json"
    return True

def check_for_available_port(config_infos:any) -> int: 
    '''
    Check for an available port to use for the server (in the config file)
    @param config_infos: The config infos
    @return: The available port (or -1 if no port is available)
    '''

    # Get the port from the config file
    ports_to_check = config_infos['data']["ports_to_check"]

    # Check if the port is available
    for port in ports_to_check:
        if is_port_available(port):
            return port
        
    return -1

def is_port_available(port:int) -> bool:
    '''
    Check if the port is available
    @param port: The port to check
    @return: True if the port is available, False otherwise
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0
    
'''
Functions activable by the server
-----------------------------------
'''

def say_hello() -> None:
    '''
    Say hello
    @return: None
    '''
    print("Hello!")

def load_save_state_from_slot(slot_number:int) -> None :
    '''
    Load a save state from a slot
    @param slot_number: The slot number of the save state
    @return: None
    '''
    savestate.load_from_slot(slot_number)
    print("Loading save state from slot " + str(slot_number))

def get_memory_adresses_values() -> any:
    '''
    Get the values of the memory adresses on the watch list
    @return: The values of the memory adresses on the watch list
    '''
    memory_adresses_values = {}

    try : 
        for name, infos in memory_adresses_to_watch.items():

            memory_adress = int(infos["adress"], 0)
            variable_type = infos["type"]
            # Use the right function to read the memory adress depending on the type
            if variable_type == "u8" :
                memory_adresses_values[name] = memory.read_u8(memory_adress)
            elif variable_type == "u16" :
                memory_adresses_values[name] = memory.read_u16(memory_adress)
            elif variable_type == "u32" :
                memory_adresses_values[name] = memory.read_u32(memory_adress)
            elif variable_type == "f32" :
                memory_adresses_values[name] = memory.read_f32(memory_adress)
            else :
                print("Error : Invalid type for the memory adress " + name)
    except :
        return {}
    
    return memory_adresses_values

def change_controller_inputs(new_inputs) -> None:
    '''
    Change the inputs of the controller
    @param new_inputs: The new inputs to set
    @return: None
    '''
    # Get the controller id
    controller_id = new_inputs["ID"]

    # Change the curr input to the new inputs map
    gc_inputs_controllers[controller_id]["A"] = new_inputs["A"]
    gc_inputs_controllers[controller_id]["B"] = new_inputs["B"]
    gc_inputs_controllers[controller_id]["X"] = new_inputs["X"]
    gc_inputs_controllers[controller_id]["Y"] = new_inputs["Y"]
    gc_inputs_controllers[controller_id]["Z"] = new_inputs["Z"]
    gc_inputs_controllers[controller_id]["L"] = new_inputs["L"]
    gc_inputs_controllers[controller_id]["R"] = new_inputs["R"]
    gc_inputs_controllers[controller_id]["Start"] = new_inputs["Start"]
    gc_inputs_controllers[controller_id]["StickX"] = new_inputs["StickX"]
    gc_inputs_controllers[controller_id]["StickY"] = new_inputs["StickY"]
    gc_inputs_controllers[controller_id]["CStickX"] = new_inputs["CStickX"]
    gc_inputs_controllers[controller_id]["CStickY"] = new_inputs["CStickY"]
    gc_inputs_controllers[controller_id]["TriggerLeft"] = new_inputs["TriggerLeft"]
    gc_inputs_controllers[controller_id]["TriggerRight"] = new_inputs["TriggerRight"]

    controller.set_gc_buttons(controller_id, gc_inputs_controllers[controller_id])

def apply_controllers_input() -> None:
    '''
    Apply the current input for each controller
    @return: None
    '''
    for controller_id in range(0, 4):
        controller.set_gc_buttons(controller_id, gc_inputs_controllers[controller_id])

    
async def handle_client(reader, writer) -> None:
    '''
    Handle the client connection requests and send the responses
    @param reader: The reader of the socket
    @param writer: The writer of the socket
    @return: None
    '''
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        
        req_json = json.loads(message)

        print(f"Action received : {req_json['action']}")

        if req_json["action"] == "load_save_state_from_slot" :
            # Load the save state from the slot
            load_save_state_from_slot(req_json["slot_number"])
            server_response = '{"status":"ok"}'

        elif req_json["action"] == "get_watch_list_values" :
            # Get the values of the memory adresses on the watch list
            memory_adresses_values = get_memory_adresses_values()
            server_response = '{"values":' + json.dumps(memory_adresses_values) + ',"status":"ok"}'
        
        elif req_json["action"] == "set_inputs" :
            # Add the input to the queue (to be processed at the next frame)
            input_action_queue.put(req_json["inputs"])
            server_response = '{"status":"ok"}'
        elif req_json["action"] == "say_hello" :
            say_hello()
            server_response = '{"status":"ok", "message":"Hello"}'
        else : 
            server_response = '{"status":"error", "message":"Invalid action : ' + req_json["action"] + '"}'

        writer.write(server_response.encode())
        await writer.drain()
    writer.close()


def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_coro = asyncio.start_server(handle_client, '127.0.0.1')
    server = loop.run_until_complete(server_coro)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    write_server_info(addr[0], addr[1])


    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

def write_server_info(host:str, port:int) :
    '''
    Write the server info (host, port) in a file dolphin_instances.txt
    @return: None
    '''
    print("Writing server info in dolphin_instances.txt")
    print("Host : " + host)
    print("Port : " + str(port))

    # Write the server info in a file
    file_path: str = script_directory + "dolphin_instances.txt"
    with open(file_path, "a") as file:
        file.write(host + "," + str(port) + "\n")
    
def execute_input_queue():
    
    # If there is new inputs to execute change the current inputs
    if not input_action_queue.empty():
        change_controller_inputs(input_action_queue.get())
    
    # Apply the current inputs
    apply_controllers_input()


if __name__ == "__main__":

    # Get the memory adresses to watch
    has_loaded_memory_adresses = load_memory_adresses_to_watch()
    if not has_loaded_memory_adresses :
        print("Error : No memory adresses to watch")
    else :
        print("Memory adresses to watch : ")
        print(memory_adresses_to_watch)

    
    # Start the server
    threading.Thread(target=start_server).start()
    while True :
        # Wait for the next frame
        await event.frameadvance()
        # Handle the inputs
        execute_input_queue()
