class OProgressBar():
    def __init__(
        self,
        completeState = 100,
        *,
        prefix = "Progress: ",
        suffix = "Complete",
        length = 60,
        decimalPlaces = 1,
        fill = "█",
        printEnd= "\r"
    ):

        self.completeState = completeState
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.decimalPlaces = decimalPlaces
        self.fill = fill
        self.printEnd = printEnd

    def PrintProgress(self, progressState):
        percent = ("{0:." + str(self.decimalPlaces) + "f}").format(100 * (progressState / float(self.completeState)))
        filledLength = int(self.length * progressState // self.completeState)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.printEnd)
        # Print New Line on Complete
        if progressState == self.completeState: 
            print()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

class OTimedProgressBar():
    from timeit import default_timer as timer
    from datetime import timedelta

    def __init__(
        self,
        completeState = 100,
        *,
        prefix = "Progress: ",
        suffix = "Complete",
        length = 60,
        decimalPlaces = 1,
        fill = "█",
        printEnd= "\r",
        Etc = False,
        EtcText = "Etc: ",
        elapsedTimeText = "Elapsed Time: "
    ):

        self.completeState = completeState
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.decimalPlaces = decimalPlaces
        self.fill = fill
        self.printEnd = printEnd
        self.EtcText = EtcText
        self.elapsedTimeText = elapsedTimeText
        self.FirstTime = True
        self.InitialTime = self.timer()
        self.Etc = Etc
        self.lastElapsedTime = "!No time registred yet!"

    def PrintProgress(self, progressState):
        if self.FirstTime: 
            self.InitialTime = self.timer()
            self.FirstTime = False
            EtcTime = None
        else:
            EtcTime = (((self.timedelta(seconds=self.timer()-self.InitialTime))/progressState)*(self.completeState-progressState))

        percent = ("{0:." + str(self.decimalPlaces) + "f}").format(100 * (progressState / float(self.completeState)))
        filledLength = int(self.length * progressState // self.completeState)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix}|{bar}| {percent}% {self.suffix} | {(self.EtcText+str(EtcTime)) if self.Etc else ""}', end = self.printEnd)
        
        # Print New Line on Complete
        if progressState == self.completeState: 
            self.lastElapsedTime = self.timer()-self.InitialTime
            print(f'\r{self.prefix}|{self.fill*self.length}| 100% {self.suffix} | {self.elapsedTimeText}{self.timedelta(seconds=self.lastElapsedTime)}\n')
            self.FirstTime = True

    def GetLasElapsedTime(self):
        return self.lastElapsedTime

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

class OLogger():
    import logging
    from pathlib import Path
    import __main__
    import traceback
    from datetime import datetime

    logFormat = "%(asctime)s:%(msecs)d -- %(levelname)s -- %(message)s"
    logFormatWLoggerName = "%(asctime)s:%(msecs)d -- %(name)s: %(levelname)s -- %(message)s"
    dateFormat = "%Y-%m-%d|%H:%M:%S"
    logging.basicConfig(level=logging.NOTSET, format=logFormat, datefmt=dateFormat)
    logTime = datetime.now().strftime("[%Y-%m-%d]-[%H-%M-%S]")
    mainPyScriptName = str(Path(__main__.__file__).stem)
    mainPyScriptPath = str(Path(__main__.__file__)).replace(f"{Path(__main__.__file__).stem}.py","")
    level = logging

    def __init__(self, *, streamLoggin = True, fileLoggin = False, loggerName = mainPyScriptName, logFileLevel = "NOTSET", showLoggerNameOnFile = False):
        self.logger = self.logging.getLogger(f"{loggerName}_Logger" if loggerName == self.mainPyScriptName else loggerName)

        logLevelList = {
            "NOTSET": self.logging.NOTSET,
            "DEBUG": self.logging.DEBUG,
            "INFO": self.logging.INFO,
            "WARNING": self.logging.WARNING,
            "ERROR": self.logging.ERROR,
            "CRITICAL": self.logging.CRITICAL,
        }
        default = self.logging.NOTSET

        if fileLoggin:
            try:
                import os
                folderCreationFlag = False

                if "Logs" not in list(os.listdir(self.mainPyScriptPath)):
                    os.mkdir(f"{self.mainPyScriptPath}Logs")
                    folderCreationFlag = True

                fileHandler = self.logging.FileHandler(f"{self.mainPyScriptPath}/Logs/{self.mainPyScriptName}-{self.logTime}.log")
                fileHandler.setLevel(logLevelList[logFileLevel])
                fileHandler.setFormatter(self.logging.Formatter(self.logFormat if not showLoggerNameOnFile else self.logFormatWLoggerName, datefmt=self.dateFormat))
                self.logger.addHandler(fileHandler)

                if folderCreationFlag == True:
                    self.LogInfo("Logs Folder was created!")

            except Exception:
                print(self.traceback.format_exc())

        if not streamLoggin:
            self.logger.propagate = False

    def LogDebug(self, infoMessege):
        self.logger.debug(infoMessege)

    def LogInfo(self, infoMessege):
        self.logger.info(infoMessege)

    def LogWarning(self, WarningMessege):
        self.logger.warning(WarningMessege)

    def LogError(self, errorMessege):
        self.logger.error(errorMessege)

    def LogExceptError(self, errorMessege):
        self.logger.critical(f"{errorMessege}: {self.traceback.format_exc()}")  

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

