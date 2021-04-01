from enum import Enum


class RequestEnum(Enum):
    OPEN_CONNECTION = "openConnection"
    CONNECTION_SYNC = "connectionSync"
    CREATE_STATEMENT = "createStatement"
    CLOSE_STATEMENT = "closeStatement"
    PREPARE_AND_EXECUTE = "prepareAndExecute"
    FETCH = "fetch"
    CLOSE_CONNECTION = "closeConnection"


if __name__ == '__main__':
    print(RequestEnum.OPEN_CONNECTION.value)
