## Configuration

The WeatherPoly node server has the following user configuration
parameters:

- Port : The TCP port to listen on for connections from weather software.
- Units : The units used to display the data. Valid settings are: 'metric', 'us', or 'uk'. The default is 'metric'
- IncomingUnits: The units used by the data provider. Valid settings are 'metric', 'us', and 'uk'. Default is 'metric'.

A mapping between the incoming data fields and the node server's nodes must be configured.  The key is a node and data type combination and the value represents the incoming data field. How a data field is represented depends on the weather software.

Valid nodes are: temperature, humidity, pressure, rain, wind, light, and lightning. See [node-value combinations](NODE_VALUE.md) for a full list of node-values that can be used.

### Cumulus software
Cumulus software allows you to configure what text string is used to represent each value.  See the Cumulus documentation for a list of valid tags.  A Cumulus HTTP API value of:

http://<node server ip>:8080/cumulus?temp=<#temp>&humidity=<#humidity>

Will send temperature and humidity data.  This can be mapped to node server nodes using:

temperature-main : temp
humidity-main : humidity

### acuparse
acuparse software for Acurite weather stations https://github.com/acuparse/acuparse can be configured to send data to a generic service.  To configure acuparse to send data to WeatherPoly, set the generic URL to:

http://<node server ip>:8080/acuparse

#### Configure WeatherPoly with the following mapping:
* temperature-main = tempf
* temperature-dewpoint = dewptf
* humidity-main = humidity
* pressure-sealevel = baromin
* wind-windspeed = windspeedmph
* wind-winddir = winddir
* wind-avgwindspeed = windspdmph_avg2m
* rain-rate = rainin
* rain-daily = dailyrainin

Input units should be set as US.

### WeeWX
WeeWX data is supported through an extension to WeeWX called weewx-crt which can output the data in Cumulus Real Time format. The weewx-crt extension is configured by setting the realtime_url to:

http://<node server ip>:8080/weewx

#### Configure WeatherPoly mappings:
The real-time data file is a fixed format file with the weather values separated by spaces. This is split so that the space separated value's index is mapped to the node servers nodes-values. For example:
* temperature-main = 2
* temperature-dewpoint = 3
* humidity-main = 4
* etc.


### MeteoBridge
MeteoBridge data is supported using the Home Weather Station weather network configuration.  For the API URL use

http://<node server ip>:8080/

MeteoBridge will send a space separated list of values. These are mapped to the node server's nodes using the value's position in that list. The table below shows the values and numeric position.

#### MeteoBridge Field list
[MeteoBridge field list](METEOBRIDGE.md)
