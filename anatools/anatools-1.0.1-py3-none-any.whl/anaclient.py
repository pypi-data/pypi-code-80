"""AnaClient is a python module for accessing Rendered.AI's Ana Platform API."""

class AnaClient:

    def __init__(self, workspace=None, environment='prod', verbose=False):
        import pyrebase, getpass, keyring, time, requests, base64, json
        import anatools.envs as envs
        self.verbose = verbose
        if environment not in ['dev','test','prod']: 
            print('Invalid environment argument, must be \'dev\', \'test\' or \'prod\'.')
            return None
        self.__environment = environment
        encodedbytes = envs.envs.encode('ascii')
        decodedbytes = base64.b64decode(encodedbytes)
        decodedenvs = json.loads(decodedbytes.decode('ascii'))
        envdata = decodedenvs[environment]
        self.__keyservice = 'ana-{}'.format(environment)
        self.__firebase = pyrebase.initialize_app(envdata)
        self.__url = envdata['rachaelURL']
        self.__auth = self.__firebase.auth()
        self.__timer = int(time.time())
        email =     keyring.get_password(self.__keyservice,'email')
        password =  keyring.get_password(self.__keyservice,'password')
        if email and password: self.__user = self.__auth.sign_in_with_email_and_password(email, password)
        else:
            print('Enter your credentials for the {}.'.format(envdata['name'])) 
            email = input('Email: ')
            invalidpass = True
            failcount = 1
            while invalidpass:
                try:    
                    password = getpass.getpass()
                    self.__user = self.__auth.sign_in_with_email_and_password(email, password)
                    keyring.set_password(self.__keyservice,'email',email)
                    keyring.set_password(self.__keyservice,'password',password)
                    invalidpass = False
                except:
                    if failcount < 5:
                        print('\rInvalid password, please enter your password again.')
                        failcount += 1
                    else:
                        print('\rInvalid password, please consider resetting your password at {}/forgot-password.'.format(envdata['website']))
                        return None
        self.__uid = self.__user['localId']
        self.__headers = {'uid':self.__uid, 'idtoken':self.__user['idToken']}
        self.__logout = False
        if self.verbose == 'debug': print(self.__user['idToken'])
        if workspace:   self.__workspace = workspace
        else:
            response = requests.post(
                url = self.__url, 
                headers = self.__headers, 
                json = {
                    "operationName": "getWorkspaces",
                    "variables": { "uid": self.__uid },
                    "query": """query getWorkspaces($uid: String!) {
                                    getWorkspaces(uid: $uid) {
                                        workspaceid:    id
                                        name:           name
                                        owner:          owner
                                    }
                                }""" })
            if self.verbose == 'debug': print(response.status_code, response.json())
            if response.status_code == 200 and response.json()['data']['getWorkspaces']: 
                workspaces = response.json()['data']['getWorkspaces']
            self.__workspace = workspaces[0]['workspaceid']
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getChannelsWithWorkspace",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": self.__workspace },
                "query": """query getChannelsWithWorkspace($uid: String!, $workspaceId: String!) {
                                getChannelsWithWorkspace(uid: $uid, workspaceId: $workspaceId) {
                                    channelid:  channelID
                                    name:       channelName    
                                }
                            }""" })
        self.__channels = {}
        if self.verbose: print(response.status_code, response.json())
        if response.status_code == 200:
            if self.verbose: print('\rSigned into {} with {}, using workspace {}.'.format(envdata['name'],email, self.__workspace))
            del email, password
            for channel in response.json()['data']['getChannelsWithWorkspace']: self.__channels[channel['name']] = channel['channelid']
            if not len(self.__channels.keys()):
                print('No channels found for workspace. Contact info@rendered.ai for help with this issue.')
                if self.verbose: print(response.status_code, response.json())   
                return
        else:
            if self.verbose: print(response.status_code, response.json())
            print("Error connecting to endpoint. Contact info@rendered.ai for help with this issue.")
            return

    
    def __refresh_token(self):
        import time, keyring
        if int(time.time())-self.__timer > int(self.__user['expiresIn']):
            email =     keyring.get_password(self.__keyservice,'email')
            password =  keyring.get_password(self.__keyservice,'password')
            self.__user = self.__auth.sign_in_with_email_and_password(email, password)
            self.__headers = {'uid':self.__uid, 'idtoken':self.__user['idToken']}
            del email, password


    def __check_logout(self):
        if self.__logout:
            print('You are currently logged out, login to access the Ana tool.')
            return True
        self.__refresh_token()
        return False


    def logout(self):
        import keyring
        if self.__check_logout(): return
        keyring.delete_password(self.__keyservice,'email')
        keyring.delete_password(self.__keyservice,'password')
        self.__logout = True
        del self.__keyservice, self.__firebase, self.__url, self.__auth, self.__user, self.__uid, self.__headers, self.__workspace, self.__channels

    
    def login(self, workspace=None, environment='prod'):
        self.__init__(workspace, environment, self.verbose)


    def get_workspace(self):
        if self.__check_logout(): return
        return self.__workspace


    def set_workspace(self, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if workspaceid is None: workspaceid = self.__uid
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getChannelsWithWorkspace",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid },
                "query": """query getChannelsWithWorkspace($uid: String!, $workspaceId: String!) {
                                getChannelsWithWorkspace(uid: $uid, workspaceId: $workspaceId) {
                                    channelid:  channelID
                                    name:       channelName
                                }
                            }""" })
        self.__channels = {}
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200: 
            for channel in response.json()['data']['getChannelsWithWorkspace']: self.__channels[channel['name']] = channel['channelid']
            self.__workspace = workspaceid
            return
        else: print('Failed to set workspace.')


    def create_workspace(self, name, channels, description=None):
        import requests
        if self.__check_logout(): return
        if name is None: name = self.__uid
        if description is None: description = ''
        channelids = [self.__channels[channel] for channel in channels]
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createWorkspace",
                "variables": {
                    "uid": self.__uid,
                    "workspaceName": name,
                    "channels": channelids,
                    "description": description },
                "query": """mutation createWorkspace($uid: String!, $workspaceName: String!, $channels: [String]!, $description: String!) {
                                createWorkspace(uid: $uid, workspaceName: $workspaceName, channels: $channels, description: $description) {
                                    id
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createWorkspace']:
            print(response.json())
            return response.json()['data']['createWorkspace']['id']
        else: print('Failed to create the new workspace.')


    def delete_workspace(self, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if workspaceid is None: workspaceid = self.__workspace 
        response = input('This will remove any configurations, graphs and datasets associated with this workspace.\nAre you certain you want to delete this workspace? (y/n)  ')
        if response not in ['Y', 'y', 'Yes', 'yes']: return
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deleteWorkspace",
                "variables": { 
                    "uid": self.__uid,
                    "workspaceId": workspaceid },
                "query": """mutation deleteWorkspace($uid: String!, $workspaceId: String!) {
                                deleteWorkspace(uid: $uid, workspaceId: $workspaceId)
                            }""" })
        self.__channels = {}
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deleteWorkspace']: 
            return response.json()['data']['deleteWorkspace'].lower() == 'success'
        else: print("Failed to delete workspace.")


    def update_workspace(self, description, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if description is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "updateWorkspace",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "description": description },
                "query": """mutation updateWorkspace($uid: String!, $workspaceId: String!, $description: String!){
                                updateWorkspace(uid: $uid, workspaceId: $workspaceId, description: $description)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['updateWorkspace']:
            return response.json()['data']['updateWorkspace'].lower() == 'success'
        else: print('Failed to update the workspace description.')
    
    
    def get_workspaces(self):
        import requests
        if self.__check_logout(): return
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaces",
                "variables": { "uid": self.__uid },
                "query": """query getWorkspaces($uid: String!) {
                                getWorkspaces(uid: $uid) {
                                    workspaceid:    id
                                    name:           name
                                    owner:          owner
                                }
                            }""" })
        self.__channels = {}
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaces']: 
            return response.json()['data']['getWorkspaces']
        else: print('Failed to get workspaces.')    


    def get_members(self, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaceMembers",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid },
                "query": """query getWorkspaceMembers($uid: String!, $workspaceId: String!){
                                getWorkspaceMembers(uid: $uid, workspaceId: $workspaceId){
                                    email: userEmail
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaceMembers']:
            return [member['email'] for member in response.json()['data']['getWorkspaceMembers']]
        else: print('Failed to query workspace members.')


    def add_members(self, members, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if members is None: return
        if type(members) is str: members = [members]
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createWorkspaceMembers",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "members": members},
                "query": """mutation createWorkspaceMembers($uid: String!, $workspaceId: String!, $members: [String]!){
                                createWorkspaceMembers(uid: $uid, workspaceId: $workspaceId, members: $members)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createWorkspaceMembers']:
            return response.json()['data']['createWorkspaceMembers']
        else: print('Failed to add new members to workspace.')


    def remove_members(self,members, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if members is None: return
        if type(members) is str: members = [members]
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deleteWorkspaceMembers",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "members": members},
                "query": """mutation deleteWorkspaceMembers($uid: String!, $workspaceId: String!, $members: [String]!){
                                deleteWorkspaceMembers(uid: $uid, workspaceId: $workspaceId, members: $members)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deleteWorkspaceMembers']:
            return response.json()['data']['deleteWorkspaceMembers']
        else: print('Failed to delete new members to workspace.')


    def get_channels(self):
        if self.__check_logout(): return
        return [key for key in self.__channels.keys()]

    
    def get_graphs(self, graphid=None, name=None, owner=None, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if graphid is None: graphid = ''
        if name is None: name = ''
        if owner is None: owner = ''
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaceGraphs",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid,
                    "member": owner,
                    "name": name },
                "query": """query getWorkspaceGraphs($uid: String!, $workspaceId: String!, $graphId: String!, $member: String!, $name: String!){
                                getWorkspaceGraphs(uid: $uid, workspaceId: $workspaceId, graphId: $graphId, member: $member, name: $name){
                                    graphid:        graphid
                                    name:           name
                                    serial:         sn
                                    channel:        channel
                                    owner:          user
                                    description:    description
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaceGraphs']:
            return response.json()['data']['getWorkspaceGraphs']
        else: print('Failed to query graphs.')

    
    def create_graph(self, name, channel, graph, workspaceid=None):
        import requests, json
        if self.__check_logout(): return
        if name is None or channel is None or graph is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createGraph",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "channelId": self.__channels[channel],
                    "graph": json.dumps(graph),
                    "name": name },
                "query": """mutation createGraph($uid: String!, $workspaceId: String!, $channelId: String!, $graph: String!, $name: String!){
                                createGraph(uid: $uid, workspaceId: $workspaceId, channelId: $channelId, graph: $graph, name: $name){
                                    id
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createGraph']:
            return response.json()['data']['createGraph']['id']
        else: print('Failed to create the new graph.')

    
    def update_graph(self, graphid, description, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if graphid is None or description is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "updateWorkspaceGraph",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid,
                    "description": description },
                "query": """mutation updateWorkspaceGraph($uid: String!, $workspaceId: String!, $graphId: String!, $description: String!){
                                updateWorkspaceGraph(uid: $uid, workspaceId: $workspaceId, graphId: $graphId, description: $description)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['updateWorkspaceGraph']:
            return response.json()['data']['updateWorkspaceGraph'].lower() == 'success'
        else: print('Failed to update the graph description.')


    def delete_graph(self, graphid, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if graphid is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deleteWorkspaceGraph",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid},
                "query": """mutation deleteWorkspaceGraph($uid: String!, $workspaceId: String!, $graphId: String!){
                                deleteWorkspaceGraph(uid: $uid, workspaceId: $workspaceId, graphId: $graphId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deleteWorkspaceGraph']:
            return response.json()['data']['deleteWorkspaceGraph'].lower() == 'success'
        else: print('Failed to delete the graph.')

    
    def download_graph(self, graphid, workspaceid=None):
        import requests, json
        if self.__check_logout(): return
        if graphid is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaceGraphs",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid,
                    "member": '',
                    "name": '' },
                "query": """query getWorkspaceGraphs($uid: String!, $workspaceId: String!, $graphId: String!, $member: String!, $name: String!){
                                getWorkspaceGraphs(uid: $uid, workspaceId: $workspaceId, graphId: $graphId, member: $member, name: $name){
                                    graph:          graph
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaceGraphs']:
            return json.loads(response.json()['data']['getWorkspaceGraphs'][0]['graph'])
        else: print('Failed to find graph.')

    
    def get_datasets(self, datasetid=None, name=None, owner=None, status=None, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if datasetid is None: datasetid = ''
        if name is None: name = ''
        if owner is None: owner = ''
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaceDatasets",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "datasetId": datasetid,
                    "member": owner,
                    "name": name },
                "query": """query getWorkspaceDatasets($uid: String!, $workspaceId: String!, $datasetId: String!, $member: String!, $name: String!){
                                getWorkspaceDatasets(uid: $uid, workspaceId: $workspaceId, datasetId: $datasetId, member: $member, name: $name){
                                    datasetid:          datasetid
                                    serial:             serial
                                    owner:              user
                                    channel:            channel
                                    description:        description
                                    status:             status
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaceDatasets']:
            if status:
                datasets = [dataset for dataset in response.json()['data']['getWorkspaceDatasets'] if dataset['status'] == status]
                return datasets
            else: return response.json()['data']['getWorkspaceDatasets']
        else: print('Failed to query datasets.')


    def create_dataset(self, name, graphid, description=None, interpretations=1, priority=1, seed=1, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if name is None or graphid is None: return
        if description is None: description = ''
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createJobWithUserVersion",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid,
                    "dataset": name,
                    "interpretations": interpretations,
                    "description": description,
                    "priority": priority,
                    "seed": seed },
                "query": """mutation createJobWithUserVersion($uid: String!, $workspaceId: String!, $dataset: String!, $description: String!, $graphId: String!, $interpretations: String!, $priority: String!, $seed: String!) {
                                createJobWithUserVersion(uid: $uid, workspaceId: $workspaceId, dataset: $dataset, description: $description, graphId: $graphId, interpretations: $interpretations, priority: $priority, seed: $seed) {
                                    id
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createJobWithUserVersion']:
            return response.json()['data']['createJobWithUserVersion']['id']
        else: print('Failed to create the new dataset.')

    
    def update_dataset(self, datasetid, description, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if datasetid is None or description is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "updateWorkspaceDataset",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "datasetId": datasetid,
                    "description": description },
                "query": """mutation updateWorkspaceDataset($uid: String!, $workspaceId: String!, $datasetId: String!, $description: String!){
                                updateWorkspaceDataset(uid: $uid, workspaceId: $workspaceId, datasetId: $datasetId, description: $description)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['updateWorkspaceDataset']:
            return response.json()['data']['updateWorkspaceDataset'].lower() == 'success'
        else: print('Failed to update the dataset description.')


    def delete_dataset(self, datasetid, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if datasetid is None: datasetid
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deleteWorkspaceDataset",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "datasetId": datasetid},
                "query": """mutation deleteWorkspaceDataset($uid: String!, $workspaceId: String!, $datasetId: String!){
                                deleteWorkspaceDataset(uid: $uid, workspaceId: $workspaceId, datasetId: $datasetId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deleteWorkspaceDataset']:
            return response.json()['data']['deleteWorkspaceDataset'].lower() == 'success'
        else: print('Failed to delete the dataset.')


    def download_dataset(self, datasetid, workspaceid=None):
        import requests
        if self.__check_logout(): return
        if datasetid is None: datasetid
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getDownloadDataset",
                "variables": {
                    "uid": self.__uid,
                    "datasetId": datasetid,
                    "workspaceId": workspaceid },
                "query": """mutation getDownloadDataset($uid: String!, $datasetId: String!, $workspaceId: String!) {
                                getDownloadDataset(uid: $uid, datasetId: $datasetId, workspaceId: $workspaceId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getDownloadDataset']:
            url = response.json()['data']['getDownloadDataset']
            fname = url.split('?')[0].split('/')[-1]
            downloadresponse = requests.get(url=url)
            with open(fname, 'wb') as outfile:
                outfile.write(downloadresponse.content)
            del downloadresponse
            return fname
        else: print('Failed to download the dataset.')


    def register_docker(self, channel):
        import requests, docker, base64, json, time
        import anatools.envs as envs
        if self.__environment != 'dev': 
            print('Docker containers can only be registered in the Development environment.')
            return False
        if self.__check_logout(): return
        if channel is None: return False
        encodedbytes = envs.envs.encode('ascii')
        decodedbytes = base64.b64decode(encodedbytes)
        decodedenvs = json.loads(decodedbytes.decode('ascii'))
        envdata = decodedenvs[self.__environment]
        
        # check if channel image is in docker
        dockerclient = docker.from_env()
        try: channelimage = dockerclient.images.get(channel)
        except docker.errors.ImageNotFound:
            print('Could not find Docker image with name {channel}.')
            return False
        except:
            print('Error connecting to Docker.')
            return False
        
        # get ecr password
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "registerChannelDocker",
                "variables": {
                    "channelId": self.__channels[channel] },
                "query": """mutation registerChannelDocker($channelId: String!) {
                                registerChannelDocker(channelId: $channelId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['registerChannelDocker']:
            encodedpass = response.json()['data']['registerChannelDocker']
            encodedbytes = encodedpass.encode('ascii')
            decodedbytes = base64.b64decode(encodedbytes)
            decodedpass = decodedbytes.decode('ascii').split(':')[-1]
        else: 
            print('Failed to retrieve Docker credentials.')
            return

        # tag and push image
        print(f"Pushing {channel} Docker Image. This could take awhile...", end='')
        time.sleep(1)
        reponame = envdata['ecrURL'].replace('https://','')+'/'+channel
        resp = channelimage.tag(reponame)
        if self.verbose == 'debug': print( dockerclient.images.push(reponame, auth_config={'username':'AWS', 'password':decodedpass}) )
        else: resp = dockerclient.images.push(reponame, auth_config={'username':'AWS', 'password':decodedpass})
        print("Complete!")

        # confirm image pushed / start registration
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "registerChannel",
                "variables": {
                    "channelId": self.__channels[channel] },
                "query": """mutation registerChannel($channelId: String!) {
                                registerChannel(channelId: $channelId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        docker_registered = False
        if response.status_code == 200 and response.json()['data']['registerChannel']:
            if response.json()['data']['registerChannel'] == 'success': docker_registered = True
        if not docker_registered: print('Failed to confirm Docker upload.')

        # cleanup docker
        resp = dockerclient.images.remove(reponame)
        return docker_registered

    
    def register_channel_owner(self, email, channel):
        import requests, json
        if email is None or channel is None: return False
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "registerChannelOwner",
                "variables": {
                    "email": email, 
                    "channelId": self.__channels[channel] },
                "query": """mutation registerChannelOwner($email: String!, $channelId: String!) {
                                registerChannelOwner(email: $email, channelId: $channelId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['registerChannelOwner'] == "success":
            return True
        else: 
            print('Failed to register owner.')
            return False


    def register_data(self,package,location):
        import requests, os

        # make sure the package data is 
        if package not in os.listdir(location):
            return
        fileroot = os.path.abspath(os.path.join(location,package))
        uploadfiles = []

        # recursively search directory for upload files
        for root, dirs, files in os.walk(fileroot):
            for upfile in files:
                uploadfiles.append(os.path.join(root,upfile))
        
        # for each file, generate a presigned-url and upload via requests
        numfiles = len(uploadfiles)
        getkey = None
        presignedurl = None
        for i,filepath in enumerate(uploadfiles):
            filename = filepath.split('/')[-1]
            print(f'Uploading file {i} of {numfiles}:    {filename}', end='/r')
            key = filepath.replace(fileroot,'').replace(filename,'')
            if getkey != key:
                getkey = key
                response = requests.post(
                    url = self.__url, 
                    headers = self.__headers, 
                    json = {
                        "operationName": "registerPackageData",
                        "variables": {
                            "package": package, 
                            "key": key },
                        "query": """mutation registerPackageData($package: String!, $key: String!) {
                                        registerPackageData(package: $package, key: $key)
                                    }""" })
                if self.verbose == 'debug': print(response.status_code, response.json())
                if response.status_code == 200 and response.json()['data']['registerPackageData']['url']:
                    presignedurl = response.json()['data']['registerPackageData']['url']
                
            # upload the file
            with open(filename, 'rb') as data:
                files = {'file': (filename, data)}
                response = requests.post(presignedurl['url'], data=presignedurl['fields'], files=files)
                if response.status_code != 204: 
                    print('Upload failed.')
                    return
        print('Upload complete!')    


    def register_datafile(self,package,filepath):
        import requests, os
        key = filepath.split(f'/packages/{package}/')[-1]
        filename = key.split('/')[-1]
        key = key.replace(filename,'')
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "registerPackageData",
                "variables": {
                    "package": package, 
                    "key": key },
                "query": """mutation registerPackageData($package: String!, $key: String!) {
                                registerPackageData(package: $package, key: $key)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['registerPackageData']['url']:
            presignedurl = response.json()['data']['registerPackageData']['url']

        with open(filepath, 'rb') as data:
            files = {'file': (filename, data)}
            response = requests.post(presignedurl['url'], data=presignedurl['fields'], files=files)
            if response.status_code != 204: 
                print('Upload failed.')
                return
        print('Upload complete!') 


    def create_channel(self, channel, packages=None, instance=None, organizations=None):
        import requests
        if channel is None or instance is None: 
            print('Must provide channel and instance type.')
            return
        if packages is None: packages = []
        if organizations is None: organizations = []
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createChannel",
                "variables": {
                    "name": channel, 
                    "packages": packages,
                    "instance": instance,
                    "organizations": organizations },
                "query": """mutation createChannel($name: String!, $packages: [String!], $instance: String!, $organizations: [String!]) {
                                createChannel(name: $name, packages: $packages, instance: $instance, organizations: $organizations)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createChannel']:
            return response.json()['data']['createChannel']
        return False


    def deploy_channel(self, channel, environment='test'):
        import requests
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deployChannel",
                "variables": {
                    "channelId": self.__channels[channel], 
                    "environment": environment },
                "query": """mutation deployChannel($channelId: String!, $environment: String!) {
                                deployChannel(channelId: $channelId, environment: $environment)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deployChannel'] == "success":
            return True
        return False
