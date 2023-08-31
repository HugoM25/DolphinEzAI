'''
This file is used to communicate with the dolphin_server.py file. It contains various functions that can be used to send commands to the server.
'''
import json
import socket

'''
This class is used to communicate with the server
You can use it to send commands to the server and get the response
You can instantiate as many clients as you want as long as you don't use the same port
'''
class DCA_client() :
    def __init__(self, host:str = 'localhost', port:int = 12345) -> None:
        # The host and port of the server to connect to
        self.HOST = host
        self.PORT = port

    def reset(self) -> None : 
        '''
        Ask the server to reset the emulator
        @return: The response of the server (success or error)
        '''
        server_response = self.send_message('{"action":"reset"}')
        return json.loads(server_response)

    def get_watch_list_values(self) -> any:
        '''
        Ask the server for the current observation of the game and return it
        @return: The server response (containing the observation)
        '''
        server_response = self.send_message('{"action":"get_watch_list_values"}')
        return json.loads(server_response)

    def load_save_state_from_slot(self, slot_number:int) -> any :
        '''
        Ask the server to load a save state from a slot
        @param slot_number: The slot number of the save state
        @return: The response of the server (success or error)
        '''
        server_response = self.send_message('{"action":"load_save_state_from_slot", "slot_number":' + str(slot_number) + '}')
        return server_response

    def send_inputs(self, inputs:any) -> any:
        '''
        Send the inputs to the server to be executed by controller id
        @param inputs: The inputs to set
        @return: The response of the server (success or error)
        '''
        server_response = self.send_message('{"action":"set_inputs", "inputs":' + json.dumps(vars(inputs)) + '}')
        return server_response

    def send_message(self, message):
        '''
        Send a message to the server
        @param message: The message to send
        '''
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((self.HOST, self.PORT))

        client_socket.sendall(message.encode())  # Send the message to the server
        data_server = client_socket.recv(1024)  # Receive data from the server

        # Close the client socket
        client_socket.close()

        return data_server.decode()
    
    def connect(self, host:str = 'localhost', port:int = 12345) -> None:
        '''
        Connect to the server
        @param host: The host of the server to connect to
        @param port: The port of the server to connect to
        '''
        self.HOST = host
        self.PORT = port