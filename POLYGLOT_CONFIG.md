## Configuration

The WeatherPoly node server has the following user configuration
parameters:

- Port : The TCP port to listen on for connections from weather software.
- Units : If the data received is in metric units, changing this will change how the data is displayed. Valid settings are: 'metric', 'US', or 'UK' units.

A mapping between the incoming data fields and the node server's nodes must be configured.  The key is a node and data type combination and the value represents the incoming data field. How a data field is represented depends on the weather software.

Valid nodes are: temperature, humidity, pressure, rain, wind, light, and lightning

Cumulus software allows you to configure what text string is used to represent each value.  See the Cumulus documentation for a list of valid tags.  A Cumulus HTTP API value of:

http://<node server ip>:8080/cumulus?temp=<#temp>&humidity=<#humidity>

Will send temperature and humidity data.  This can be mapped to node server nodes using:

temperature-main : temp
humidity-main : humidity


