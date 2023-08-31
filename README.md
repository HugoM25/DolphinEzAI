# DolphinEzAI
A framework aiming to provide an easy way to transform any dolphin game into an RL environment

# Context

You are looking for a Python API to use with the Dolphin emulator and don't want to be restrained by a embedded python interpreter ? Then this tool is for you ! 
# Prerequisites

To use this framework you'll need the modified dolphin version by Felk that you can find [here](https://github.com/Felk/dolphin).


# Installation


# Usage

##  Files explainations

In the ```dolphinSide``` folder you'll find :
- `dolphin_server.py` : This file is a socket server that will run on the custom dolphin and communicate with the dolphin client api.
- `watch_list.csv` : This file contains a list of memory adresses that the server should be tracking. Those values depends on the game. 

The dolphin_server.py needs to run on the custom dolphin, to do so you can either add it manually using the application interface or launch using a command like so :

```cmd
<path_to_dolphin> --script <path_to_dolphin_server_script>
```


## API documentation

