import ciso8601
import time

values_inside_configuration = ["variables", "scenarios", "models"]

class InsertExperimentDTO:
    def __init__(self,
                 name=None,
                 temporalResolution="DAILY",
                 temporalResolutionAggFunction={},
                 variables=[],
                 scenarios=[],
                 models=[],
                 baconfiguration=[],
                 spatialResolution="NATIVE",
                 spatialResolutionAggFunction={},
                 datasetProjection={},
                 datasetReference={},
                 spatialCoverage=None,
                 outputFormat="netcdf",
                 validation="NONE",
                 mask="NONE"
                 ):

        self.name = name
        self.temporalResolution = temporalResolution
        self.temporalResolutionAggregationFunctions = temporalResolutionAggFunction
        self.variables = variables
        self.scenarios = scenarios
        self.models = models
        self.baconfiguration = baconfiguration
        self.spatialResolution = spatialResolution
        self.spatialResolutionAggregationFunctions = spatialResolutionAggFunction
        self.datasetProjection = datasetProjection
        self.datasetReference = datasetReference
        self.spatialCoverage = spatialCoverage
        self.outputFormat = outputFormat
        self.validation = validation
        self.mask = mask

    def get_dict(self):
        d = self.__dict__.copy()
        d['configuration'] = {}
        for key, value in self.__dict__.items():
            if key in values_inside_configuration:
                if key == 'scenarios':
                    for i in range(len(d[key])):
                        if type(d[key][i]['startDate']) is not int:
                            start = ciso8601.parse_datetime(d[key][i]['startDate'])
                            end = ciso8601.parse_datetime(d[key][i]['endDate'])
                            # to get time in seconds:
                            time_start = int(time.mktime(start.timetuple()) * 1000)
                            time_end = int(time.mktime(end.timetuple()) * 1000)
                            d[key][i]['startDate'] = time_start
                            d[key][i]['endDate'] = time_end
                d['configuration'][key] = d[key]

            if value is None:
                d.pop(key)

        for key in values_inside_configuration:
            del d[key]
        return d