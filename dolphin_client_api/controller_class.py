'''
The classes here are used to store the inputs of a controller
'''


'''
This class is used to store the inputs of a controller that will be sent to the server
The format readable by the server is the GameCube controller format
'''
class Controller() : 
    def __init__(self) -> None:
        '''
        Initialize the inputs of the controller
        '''
        self.Left: int = 0
        self.Right: int = 0
        self.Down: int = 0
        self.Up: int = 0
        self.Z: int = 0
        self.R: int = 0
        self.L: int = 0
        self.A: int = 0
        self.B: int = 0
        self.X: int = 0
        self.Y: int = 0
        self.Start: int = 0
        self.StickX: int = 128 # 0-255, 128 is neutral 
        self.StickY: int = 128 # 0-255, 128 is neutral
        self.CStickX: int = 128 # 0-255, 128 is neutral
        self.CStickY: int = 128 # 0-255, 128 is neutral
        self.TriggerLeft: int = 255 # 0-255
        self.TriggerRight: int = 255 # 0-255
        self.AnalogA: int = 255 # 0-255
        self.AnalogB: int =255 # 0-255
        self.Connected: int = 0
        self.ID: int = 0


'''
This class is used to store the inputs of a controller 
( Using the GameCube controller format )
'''
class GCInputs(Controller) :
    def __init__(self) -> None:
        '''
        Initialize the inputs of the controller
        '''
        super().__init__()

'''
This class is used to store the inputs of a controller
( Using the PS2 controller format ) 
TO DO : Complete the class with the PS2 controller format
'''
class PS2Inputs(Controller) :
    def __init__(self) -> None:
        '''
        Initialize the inputs of the controller
        '''
        super().__init__()

    @property
    def X(self):
        return self.Controller.A
    
    @X.setter
    def X(self, value):
        self.Controller.A = value

    

    
