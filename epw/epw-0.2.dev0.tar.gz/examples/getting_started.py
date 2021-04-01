#!/usr/bin/env python3

import epw.core
import matplotlib.pyplot as plt

sub_dict = {("WindowMaterial:SimpleGlazingSystem", "Solar Heat Gain Coefficient"): 9.99}

df = epw.core.make_idf_and_run_eplus("~/Téléchargements/cube3_CGCS_0500_TL_0739.idf",
                                     weather_file_path="~/bin/energyplus/WeatherData/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw",
                                     sub_dict=sub_dict)

df.plot()
plt.show()

#epw.core.run_eplus("~/bin/energyplus/ExampleFiles/1ZoneUncontrolled.idf", weather_file_path="~/bin/energyplus/WeatherData/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw")
