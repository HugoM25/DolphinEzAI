import argparse
import subprocess
import time
import os
import dolphin_client_api as dca 

class DolphinEzAIManager() :
    def __init__(self) -> None:
        self.dolphin_instances_list: list[dca.DCA_client] = []

    def setup_dolphin(self, instances_nb:int, dolphin_path:str, game_path:str) -> None:
        '''
        Setup the dolphin instances
        @param instances_nb: The number of dolphin instances to start
        @param dolphin_path: The path to the dolphin executable
        @param game_path: The path to the game to launch
        @return: The dolphin instances list (host, port)
        '''
        # Clear the dolphin instances file
        with open("dolphinSide/dolphin_instances.txt", "w") as f:
            f.write("")

        # Start the dolphin instances
        for _ in range(instances_nb) :
            folder_path = os.path.dirname(os.path.realpath(__file__))
            cmd = f'{dolphin_path} --script {folder_path}/dolphinSide/dolphin_server.py --e "{game_path}"'
            subprocess.Popen(cmd, shell=True)
            # Wait for the dolphin instance to start before starting the next one
            time.sleep(1)

        # Wait for the dolphin instances to start
        time.sleep(5)

        # Get the dolphin instances list by checking the dolphin instances file
        dolphin_instances = []
        with open("dolphinSide/dolphin_instances.txt", "r") as f:
            for line in f:
                host, port = line.strip().split(",")
                dolphin_instance = dca.DCA_client(host, int(port))
                dolphin_instances.append(dolphin_instance)
        
        self.dolphin_instances_list = dolphin_instances
    
    def get_instance_dolphin(self, index: int) -> dca.DCA_client :
        return self.dolphin_instances_list[index]
    
if __name__ == "__main__" :
    # Parse the arguments
    parser = argparse.ArgumentParser(description='The dolphin ez AI manager')
    parser.add_argument('-n','--instances-nb', type=int, default=1, help='The number of dolphin to start')
    parser.add_argument('-d','--dolphin-path', type=str, default="", help='The path to the dolphin executable', required=True)
    parser.add_argument('-g','--game-path', type=str, default="", help='The path to the game to launch', required=True)
    args = parser.parse_args()

    # Print the arguments
    print("==============DolphinEzAI================")
    print("Starting " + str(args.instances_nb) + " dolphin instances")
    print("Dolphin path : " + args.dolphin_path)
    print("Game path : " + args.game_path)
    print("=========================================")

    # Setup the dolphin instances
    dolphinEzAIManager = DolphinEzAIManager()
    dolphinEzAIManager.setup_dolphin(args.instances_nb, args.dolphin_path, args.game_path)

    print("Dolphin instances successfully launched :")
    for dolphin_instance in dolphinEzAIManager.dolphin_instances_list :
        print(str(dolphin_instance))
    print("=========================================")

    print("Trying to connect to the dolphin instances...")
    for dolphin_instance in dolphinEzAIManager.dolphin_instances_list :
        print("Connecting to " + str(dolphin_instance))
        print(dolphin_instance.say_hello())
    print("Dolphin instances successfully connected")
    print("=========================================")
