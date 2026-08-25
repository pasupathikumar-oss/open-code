class radio:
    initialized = False
    def __init__(self,controller):
        self.params = self.getDefaultParams()
        self.joy = controller
        self.axis = self.joy.axisValues
        
    def getDefaultParams(self):
        params = {}
        params['twr'] = 9.5 #thrust to weight ratio of the quad
        params['rate'] = 1.0 #your rc rate from betaflight
        params['pitchExpo'] = .7 #expo from betaflight
        params['rollExpo'] = .7
        params['yawExpo'] = .7
        
        #min and max resolution of your radio inputs
        params['minThrottle'] = -32767 
        params['maxThrottle'] = 32767
        params['minYaw'] = -32767
        params['maxYaw'] = 32767
        params['minPitch'] = -32767
        params['maxPitch'] = 32767
        params['minRoll'] = -32767
        params['maxRoll'] = 32767
        params['minArm'] = -32767
        params['maxArm'] = 32767
        params['minReset'] = -32767
        params['maxReset'] = 32767
        
        #which radio channel we'd like to assign to our functions
        params['throttleChannel'] = 2 #moving up and down stick (the one without a spring)
        params['yawChannel'] = 0      #turning left and right
        params['pitchChannel'] = 1    #turning up and down
        params['rollChannel'] = 3     #rolling side to side
        params['armChannel'] = 5
        params['resetChannel'] = 4

        params['resetSetpoint'] = .75      #arm above or below this percent
        params['resetInverted'] = True     #only arm when switch is high, or low

        params['armSetpoint'] = .25      #arm above or below this percent
        params['armInverted'] = False     #only arm when switch is high, or low
        params['cameraTilt'] = 45 

        #center offsets
        params['rollOffset'] = 0
        params['yawOffset'] = 0
        params['pitchOffset'] = 0

        params['dedicatedThrottleStick'] = True
        return params
        
    def getStickPercentage(self,min,max,value):
        resolution = abs(min)+abs(max)
        percent = abs((value/resolution)+.5)
        return percent

    def setup(self,camera,angle):
        try:
            own['setup']
        except:
            angle = (angle/180)*math.pi
            camera.applyRotation([angle,0,0],True)
            own['setup'] = True
            own['canReset'] = False
        
    def getSwitchValue(self,switchPercent,switchSetpoint,switchInverted):
        if(switchInverted):
            switch = switchPercent>switchSetpoint
        else:
            switch = switchPercent<switchSetpoint
        return switch
    def resetGame(self):
        act = own.actuators["restart"]
        act.useRestart = True
        cont.activate(act)

    def getPitchPercent(self):
        pitch = self.axis[self.params['pitchChannel']]
        pitchPercent = self.getStickPercentage(self.params['minPitch'],self.params['maxPitch'],pitch)
        return pitchPercent
    
    def getRollPercent(self):
        roll = self.axis[self.params['rollChannel']]
        rollPercent = self.getStickPercentage(self.params['minRoll'],self.params['maxRoll'],roll)
        return rollPercent
        
    def getAllRawinputs(self):
        return self.axis
        
    def foobar(self):
        #xbox controllers....
        if(params['dedicatedThrottleStick'] == False):
            axis[params['throttleChannel']] -= (params['maxThrottle']-params['minThrottle'])/2

        #stick offsets
        axis[params['rollChannel']]+=params['rollOffset']
        axis[params['yawChannel']]+=params['yawOffset']
        axis[params['pitchChannel']]+=params['pitchOffset']
        values = []
        center = 7000
        sensativity = .0008
        for value in axis:
            values.append((value-center)*sensativity)
            
        throttle = (axis[params['throttleChannel']])
        yaw = axis[params['yawChannel']]
        
        
        armSwitch = axis[params['armChannel']]
        resetSwitch = axis[params['resetChannel']]

        throttlePercent = (getStickPercentage(params['minThrottle'],params['maxThrottle'],throttle))
        yawPercent = getStickPercentage(params['minYaw'],params['maxYaw'],yaw)
        
        
        armPercent = getStickPercentage(params['minArm'],params['maxArm'],armSwitch)
        resetPercent = getStickPercentage(params['minReset'],params['maxReset'],resetSwitch)
        armed = getSwitchValue(armPercent,params['armSetpoint'],params['armInverted']) 
        reset = getSwitchValue(resetPercent,params['resetSetpoint'],params['resetInverted'])
        rotationActuator = cont.actuators["movement"]