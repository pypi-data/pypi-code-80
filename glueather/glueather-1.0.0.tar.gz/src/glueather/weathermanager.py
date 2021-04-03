# Copyright (C) 2021 Vasco Costa (gluon) <vascomacosta at gmail dot com>
#
# This file is part of glueather.
#
# glueather is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# glueather is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

import calendar
import datetime
import math
from pyowm import OWM
from pyowm.commons.exceptions import UnauthorizedError, APIRequestError, NotFoundError

class WeatherError(Exception):
    def __init__(self, message):
        self.message = message

class WeatherManager:
    def __init__(self, api_key, units):
        self.api_key = api_key
        if units.lower() == 'c' or units.lower() == 'celsius':
            self.units = 'celsius'
        elif units.lower() == 'f' or units.lower() == 'fahrenheit':
            self.units = 'fahrenheit'
        else:
            self.units = 'celsius'
        self.owm = OWM(self.api_key)
        self.wm = self.owm.weather_manager()

    def _wind_cardinal(self, angle):
        try:
            angle = int(angle)
            if angle < 0 or angle > 360:
                return 'N/A'
        except:
            return 'N/A'
        index = math.floor((angle / 22.5) + 0.5)
        cardinal = ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")
        return cardinal[index % 16]

    def current(self, location):
        try:
            observation = self.wm.weather_at_place(location.lower())
            location = observation.location
            w = observation.weather
        except APIRequestError:
            raise WeatherError("The location was not provided.")
        except NotFoundError:
            raise WeatherError("The location provided could not be found.")
        except UnauthorizedError:
            raise WeatherError("The API key is invalid. Get one here:\nhttps://home.openweathermap.org/users/sign_up")
        except ValueError:
            raise WeatherError("The temperature units are invalid.")
        except Exception:
            raise WeatherError("An unknown error occurred.")
        return {'location':    f"{location.name}",
                'description': f"{w.detailed_status[0].upper()}{w.detailed_status[1:]}",
                'temperature': f"{math.ceil(w.temperature(self.units)['temp'])}{self.units[0].upper()}",
                'humidity':    f"{w.humidity}%",
                'pressure':    f"{w.pressure['press']}hPa",
                'wind':        f"{w.wind()['speed']}m/s @ {self._wind_cardinal(w.wind()['deg'])}"}

    def hourly(self, location):
        try:
            three_h_forecast = self.wm.forecast_at_place(location.lower(), '3h').forecast
            f = []
            for i, w in enumerate(three_h_forecast, start=1):
                f.append({'location':    f"{three_h_forecast.location.name}",
                          'description': f"{w.detailed_status[0].upper()}{w.detailed_status[1:]}",
                          'temperature': f"{math.ceil(w.temperature(self.units)['temp'])}{self.units[0].upper()}",
                          'humidity':    f"{w.humidity}%",
                          'pressure':    f"{w.pressure['press']}hPa",
                          'wind':        f"{w.wind()['speed']}m/s @ {self._wind_cardinal(w.wind()['deg'])}"})
                if i >= 4:
                    break
        except APIRequestError:
            raise WeatherError("The location was not provided.")
        except NotFoundError:
            raise WeatherError("The location provided could not be found.")
        except UnauthorizedError:
            raise WeatherError("The API key is invalid. Get one here:\nhttps://home.openweathermap.org/users/sign_up")
        except ValueError:
            raise WeatherError("The temperature units are invalid.")
        except Exception:
            raise WeatherError("An unknown error occurred.")
        return f

    def daily(self, location):
        try:
            daily_forecast = self.wm.forecast_at_place(location, 'daily').forecast
            f = []
            for i, w in enumerate(daily_forecast, start=1):
                day = calendar.day_name[datetime.datetime.strptime(w.reference_time('iso'),"%Y-%m-%d %H:%M:%S%z").weekday()]
                f.append({'location':    f"{daily_forecast.location.name}",
                          'day':         f"{day}",
                          'description': f"{w.detailed_status[0].upper()}{w.detailed_status[1:]}",
                          'max':         f"{math.ceil(w.temperature(self.units)['max'])}{self.units[0].upper()}",
                          'min':         f"{math.ceil(w.temperature(self.units)['min'])}{self.units[0].upper()}",
                          'humidity':    f"{w.humidity}%",
                          'pressure':    f"{w.pressure['press']}hPa",
                          'wind':        f"{w.wind()['speed']}m/s @ {self._wind_cardinal(w.wind()['deg'])}"})
                if i >= 7:
                    break
        except APIRequestError:
            raise WeatherError("The location was not provided.")
        except NotFoundError:
            raise WeatherError("The location provided could not be found.")
        except UnauthorizedError:
            raise WeatherError("The API key is invalid. Get one here:\nhttps://home.openweathermap.org/users/sign_up")
        except ValueError:
            raise WeatherError("The temperature units are invalid.")
        except Exception:
            raise WeatherError("An unknown error occurred.")
        return f
