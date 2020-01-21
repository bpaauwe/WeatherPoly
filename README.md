
# Weather Station Polyglot

This is the local weather station poly for the Universal Devices ISY994i](https://www.universal-devices.com/residential/ISY) [Polyglot interface](http://www.universal-devices.com/developers/polyglot/docs/) with  [Polyglot V2](https://github.com/Einstein42/udi-polyglotv2)
(c) 2018 Robert Paauwe
MIT license.

This node server is intended to support various weather software packages. 
Currently, the following software packages are supported:
   * Cumulus - http://www.sandaysoft.com/
   * Weather Display
   * MeteoBridge

The WeatherPoly node server runs a simple web server process that listens
for data packets from your weather software package.   The packets are parsed
and sent on to the ISY.  This all happens on your local network, without
any dependency on cloud/web based services.

## Installation

1. Backup Your ISY in case of problems!
   * Really, do the backup, please
2. Go to the Polyglot Store in the UI and install.
3. Add NodeServer in Polyglot Web
   * After the install completes, Polyglot will reboot your ISY, you can watch the status in the main polyglot log.
4. Once your ISY is back up open the Admin Console.
5. Configure the node server field mapping (see below).

### Node Settings
The settings for this node are:

#### Short Poll
   * Not used
#### Long Poll
   * Not currently used
#### port
   * Configure the port the node server will listen on
#### Units
   * Configure the units used when displaying data. Choices are:
   *   metric - SI / metric units
   *   us     - units generally used in the U.S.
   *   uk     - units generally used in the U.K.

### Weather software configuration
Most weather software packages have a way to send data to a web based weather
service.  This node server takes advantage of that and acts like a web based
weather serivce. It starts a simple local web server on the port specified
in the configuration. It listens for basic HTTP GET requests from from your
weather software and parses the results.  Most of the weather software 
packages allow you to customize the data that is sent to a user defined web
service. Below is some guidence on how to configure the weather software
supported by this node server.  Other weather software may work if it can be
configured in a similar maner.

#### Cumulus software by SandaySoft
Under internet settings, there is an option for Custom HTTP.  Configure the URL
with your Polyglot's IP/Host and the port number specified above. I.E.

  http://192.168.1.12:8080

Append to that "cumulus" followed by data value names, tags for the weather
data you want to track.  You'll use the same value names in the node server
configuration to map the data to ISY node values.  As an example:

  http://192.168.1.12:8080/cumulus?temp=<#temp>&pressure=<#press>

Then in your node server configuration you'll map:

  temperature-main = temp
  pressure-station = pressure


#### MeteoBridge
Set up a new weather Network using the Home Weather Station option and enter
your node server IP/Host and port number specified above as the API URL. For
example:

   API URL: http://192.168.1.12:8080/

MeteoBridge has a pre-defined template that it uses so send data to this 
service.  The node server will map the fields from this as described in the
mapping below.

#### Node and Driver values
The complete list of available node/driver values that can be mapped are:
```
        temperature-main
        temperature-dewpoint
        temperature-windchill
        temperature-heatindex
        temperature-apparent
        temperature-inside
        temperature-extra1
        temperature-extra2
        temperature-extra3
        temperature-extra4
        temperature-extra5
        temperature-extra6
        temperature-extra7
        temperature-extra8
        temperature-extra9
        temperature-extra10
        temperature-max
        temperature-min
        temperature-soil

        humidiy-main
        humidiy-inside
        humidiy-extra1
        humidiy-extra2
        humidiy-extra3
        humidiy-extra4
        humidiy-extra5

        pressure-station
        pressure-sealevel
        pressure-trend

        wind-windspeed
        wind-winddir
        wind-gustspeed
        wind-gustdir
        wind-lullspeed
        wind-avgwindspeed

        rain-rate
        rain-hourly
        rain-daily
        rain-weekly
        rain-monthly
        rain-yearly
        rain-maxrate
        rain-yesterday

        light-uv
        light-solar_radiation
        light-illuminace
	light-solar_percent

        lightning-strikes
        lightning-distance
```


## Requirements

1. Polyglot V2 itself should be run on Raspian Stretch.
  To check your version, ```cat /etc/os-release``` and the first line should look like
  ```PRETTY_NAME="Raspbian GNU/Linux 9 (stretch)"```. It is possible to upgrade from Jessie to
  Stretch, but I would recommend just re-imaging the SD card.  Some helpful links:
   * https://www.raspberrypi.org/blog/raspbian-stretch/
   * https://linuxconfig.org/raspbian-gnu-linux-upgrade-from-jessie-to-raspbian-stretch-9
2. This has only been tested with ISY 5.0.13 so it is not guaranteed to work with any other version.

## Configuring your weather software

This node server starts a simple web server. The server will wait for
connections from the weather software and process the data sent by the
weather software.  You will need to configure your weather software to send
data periodically to the node server.  This configuration will be similar
to how you configure it to send data to other weather services. Typically,
you will need to supply the URL and data schema. The URL will be be composed
of the IP address or name of of the machine running Polyglot along with the
port number you defined in the configuration. For example:

http://192.168.1.40:8080

Data schema, instructions TBD

# Upgrading

Open the Polyglot web page, go to nodeserver store and click "Update" for "WeatherPoly".

For Polyglot 2.0.35, hit "Cancel" in the update window so the profile will not be updated and ISY rebooted.  The install procedure will properly handle this for you.  This will change with 2.0.36, for that version you will always say "No" and let the install procedure handle it for you as well.

Then restart the Weather Poly nodeserver by selecting it in the Polyglot dashboard and select Control -> Restart, then watch the log to make sure everything goes well.

The Weather Poly nodeserver keeps track of the version number and when a profile rebuild is necessary.  The profile/version.txt will contain the Weather Poly profile_version which is updated in server.json when the profile should be rebuilt.

# Release Notes

- 0.1.7 01/20/2020
   - Add support for POST requests.
   - Parse WeeWX post request with cumulus realtime data in the body
- 0.1.6 03/20/2019
   - Set initial on-line status to true
- 0.1.5 11/30/2018
   - Add support for acuparse data. https://github.com/acuparse/acuparse allows data collection form Acurite weather stations.
- 0.1.4 11/19/2018
   - Add rising slowly/rapidly and falling slowly/rapidly to pressure trend.
- 0.1.3 11/12/2018
   - Clear node lists before creating the nodes to add and node mappings
   - Map Cumulus pressure trend strings to node integers
- 0.1.2 10/26/2018
   - Fix editors for temperature and rain
   - Add incoming unit config and conversions
   - Add MeteoBridge configuration help
- 0.1.1 10/11/2018
   - Fix nodedef creation
   - Trap errors
   - Fix controller node name
- 0.1.0 09/27/2018
   - Initial version released published to github
