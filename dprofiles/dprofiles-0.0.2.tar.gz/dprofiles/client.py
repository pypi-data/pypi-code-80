import requests
import json



class Client():
    '''
    Class client. Can be declared using client = dscb_io.Client()
    get(user, Optimal[query], Optimal[save]) -> returns (specific) user information
    check_vote(user_a, user_b) -> checks if user a has voted for user b
    has_voted(user) -> returns True if the user has voted
    '''

    def __init__(self,base_url, api_token:str):
        self.base_url = base_url
        self.token = str(api_token)
    
    def get(self, id: int = None, query: str = None, save: bool = None):
        try:
            if len(self.token) != 35:
                raise TypeError("Tokens have a length of 35 characters.")
            else:
                if id is None:
                    # ID is required
                    raise TypeError("User-ID should be provided")
                try:
                    res = requests.get(f'{self.base_url}/{id}?token={self.token}')
                    res_json = res.json()
                    # response to json
                    if res_json == {"message": "Unauthorized."}:
                        raise TypeError("Wrong token provided.")
                    if res_json == {"message": 'User not found.'}:
                        #not a user
                        raise TypeError("No user with ID {} found".format(id))

                    if res_json == {"message": 'User is a bot.'}:

                        raise TypeError("Please provide a non bot user ID")
                    if res_json == {"message": 'No profile found.'}:
                        # no profile found
                        raise TypeError(f"No profile for user with ID {id} was found.")
                    if res_json == {"message": "User is banned from dprofiles."}:

                        raise Exception("The user with {} is banned from the site".format(id))

                    if res_json == {"message": "You are banned from dprofiles."}:
                        raise Exception("You are banned from using dprofiles.\nYour API-Token is not usable.")
                except requests.exceptions.ConnectionError:

                    raise TypeError("An error with the API occurred.\n"
                                        "Please contant an website administator.")

                if query is None:
                    response = res_json
                    # no query provided - whole response
                else:
                    try:
                        response = res_json[query]
                        # get value of query
                    except KeyError:
                        # no values at "index" of query
                        raise TypeError(f"Query `{query}` was not found.")

                if save is not None and save == True:
                    filename = f"{res_json['_id']}.json"  # creating filename "ID".json
                    try:
                        with open(filename, "w") as f:
                            # open json file , "w"= write "mode"
                            if query is None:
                                conf = response
                            else:
                                conf = {
                                    f"{query}": response
                                }
                            json.dump(conf, f, indent=4)
                            # dump values into file with indent 4
                    except Exception as e:
                        raise Exception(f"An error occurred by saving into `{filename}.\n"
                                        f"{e}")
                return response
        except Exception as e:
            raise Exception(e)

    def check_vote(self, voter:int, receiver:int):
        try:
            response = requests.get(f"{self.base_url}/{int(voter)}?token={self.token}")
            res = response.json()
            if res["voted_for"] != "User has not voted.":
                if int(res["voted_for"]) == int(receiver):
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception(e)
    

    def has_voted(self, user_id :int):
        try:
            response = requests.get(f"{self.base_url}/{int(user_id)}?token={self.token}")
            res = response.json()
            if res["voted_for"] == "User has not voted.":
                return False
            else:
                return True
        except Exception as e:
            raise Exception(e)
        
