x = """Mickie Studioz!

42-Q Help Window
-----------------------------------------
Importing the module

>>> import mesconduit 

-----------------------------------------
Creating a session:

>>> session = mesconduit.conduit("http://sanmmed-conduit.42-q.com:18003/conduit","1002440","R129","565","mp5678dc1a")

#  endpoint   => "http://sanmmed-conduit.42-q.com:18003/conduit"
#  Username   => "1002440"
#  password   => "R129"
#  station_id => "565"
#  client_id  => "mp5678dc1a"

-----------------------------------------
Stage Pasing the unit

>>> session.mes_PassUnit("123456")

#  Unit Serial Number   => "123456"

-----------------------------------------
Applying Admeo
>>> session.mes_ApplyMeo("123456","Screw 1 - Passed")

#  Unit Serial Number   => "123456"
#  Added MEO Message    => "Screw = 1" 

-----------------------------------------
Adding non tracked component 

>>> session.mes_AddNonTrackedComponent(mes,"123456","Strip","345363"):


#  Unit Serial Number   => "123456"
#  Component Key        => "Strip" 
#  Component Value      => "345363" 

-----------------------------------------
"""