# EndOfTheWorld

## Sources de nos données:

### Air quality
https://openaq.org/                          OpenAQ airquality datas  
http://waqi.info/                            World Air-polution (real time)  

### pollution
https://openweathermap.org/api               OpenWheatherMap (API), used to get datas about polution only.  

### Ocean related topic
https://api.tidesandcurrents.noaa.gov/       real time water level datas.(API)  
https://www.marinetraffic.com                real time ship location  

### Global monitoring
https://earthdata.nasa.gov/                  datas about environemental metrics (C02 emission, temperature anomalie, deforestation)  

### Human lifespan (death rate and their cause)
https://www.worldometers.info/               Datas about human death rate in the world.

## Comment entrainer notre model?
Idée: On récupere les données sur la mortalité des personnes par pays pour une année précise. On croisera ces données avec les emissions de GES par pays et peut être d'autres données qu'on aura réccuperer.  
En input, l'utilisateur indique son pays (ou continent) et on recupère les données environnemental / social / économique de ce pays. On fait tourner le model et bim on a l'année de la mort!
