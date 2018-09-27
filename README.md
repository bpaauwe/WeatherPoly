
# Weather Station Polyglot

This is the local weather station poly for the Universal Devices ISY994i](https://www.universal-devices.com/residential/ISY) [Polyglot interface](http://www.universal-devices.com/developers/polyglot/docs/) with  [Polyglot V2](https://github.com/Einstein42/udi-polyglotv2)
(c) 2018 Robert Paauwe
MIT license.

This node server is intended to support various weather software packages. TBD

## Installation

1. Backup Your ISY in case of problems!
   * Really, do the backup, please
2. Go to the Polyglot Store in the UI and install.
3. Add NodeServer in Polyglot Web
   * After the install completes, Polyglot will reboot your ISY, you can watch the status in the main polyglot log.
4. Once your ISY is back up open the Admin Console.
5. Configure - TBD

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

- 0.1.0 09/27/2018
   - Initial version released published to github
