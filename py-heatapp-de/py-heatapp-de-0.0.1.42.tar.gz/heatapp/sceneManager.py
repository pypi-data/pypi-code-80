from .contracts.scenes import Scenes

class SceneManager():
    """Class that interacts with an apimethods object to control scenes / create an one stop point for interacting with scenes"""
    headers = { 'Accept': 'application/json, application/xml, text/plain, text/html, *.*', 'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8' }

    def __init__(self, apiMethodsObj):
        """Constructor for the apiMethods."""
        self.apiMethodsObj = apiMethodsObj

    def isSavedMemberOfScene(self, id, scene):
        sceneRooms = self.apiMethodsObj.getSavedSceneRooms(scene)
        for i in range(len(sceneRooms)):
            if sceneRooms[i] == id:
                return True
        #If no match found return false
        return False

    def isMemberOfScene(self, id, scene):
        roomData = self.apiMethodsObj.getSpecificRoom(id)
        sceneCodes = {
            43 : "Party",
            99 : "Problem",
            127 : "Holiday",
            132 : "Standby",
            130 : "Go",
            46  : "Boost",
            122 : "Schedule",
            51  : "Manual heating",
            41  : "Manual cooling"
        }

        if sceneCodes.get(roomData["data"]["roomstatus"]) == scene:
            return True
        else:
            return False

    def clearSceneRooms(self, scene):
        return self.apiMethodsObj.setSceneRooms(scene, [])

    def getMembersOfScene(self, scene):
        return self.apiMethodsObj.getSavedSceneRooms(scene)

    def isSceneActive(self, scene):
        sceneStatus = self.apiMethodsObj.getSpecficScene(scene)
        return sceneStatus["isActive"]

    def addMemberToScene(self, id, scene, active):
        sceneRooms = [id]
        #reset scene for newly specified duration if already active
        duration = self.apiMethodsObj.getSceneDuration(scene)
        if self.isSceneActive(scene):
            if self.isMemberOfScene(id, scene):
                #Nothing todo scene already active and member exists
                return
            else:
            #TODO rewrite this to dynamic compare of roomstatus vs scene code list
                sceneRooms = self.apiMethodsObj.getSavedSceneRooms(scene)
                if id not in sceneRooms:
                    sceneRooms.append(id)
            self.apiMethodsObj.setScene(scene, duration, "false", sceneRooms)

        self.apiMethodsObj.setSceneRooms(scene, sceneRooms)
        self.apiMethodsObj.setScene(scene, duration, "true", sceneRooms)

    def removeMemberFromScene(self, id, scene, active):
        if self.isMemberOfScene(id, scene) == False:
            #room not part of scene. Therefore, nothing left to do
            return
        #Perhaps change this to a dynamic build up of rooms that are actively put in standby instead of looking at saved objects
        sceneRooms = self.apiMethodsObj.getSavedSceneRooms(scene)
        
        if id in sceneRooms:
            sceneRooms.remove(id)

        #reset scene for newly specified duration if already active
        self.apiMethodsObj.setSceneRooms(scene, sceneRooms) 
        duration = self.apiMethodsObj.getSceneDuration(scene)
    
        if self.isSceneActive(scene):
            self.apiMethodsObj.setScene(scene, duration, "false", sceneRooms)
    

        self.apiMethodsObj.setSceneRooms(scene, sceneRooms)

#        active = "false"
        if len(sceneRooms) > 0:
            active = "true"
        self.apiMethodsObj.setScene(scene, duration, active, sceneRooms)

        
