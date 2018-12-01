## Configuration

The WeatherPoly node server has the following user configuration
parameters:

- Port : The TCP port to listen on for connections from weather software.
- Units : The units used to display the data. Valid settings are: 'metric', 'us', or 'uk'. The default is 'metric'
- IncomingUnits: The units used by the data provider. Valid settings are 'metric', 'us', and 'uk'. Default is 'metric'.

A mapping between the incoming data fields and the node server's nodes must be configured.  The key is a node and data type combination and the value represents the incoming data field. How a data field is represented depends on the weather software.

Valid nodes are: temperature, humidity, pressure, rain, wind, light, and lightning

### Cumulus software
Cumulus software allows you to configure what text string is used to represent each value.  See the Cumulus documentation for a list of valid tags.  A Cumulus HTTP API value of:

http://<node server ip>:8080/cumulus?temp=<#temp>&humidity=<#humidity>

Will send temperature and humidity data.  This can be mapped to node server nodes using:

temperature-main : temp
humidity-main : humidity

### acuparse
acuparse software for Acurite weather stations https://github.com/acuparse/acuparse can be configured to send data to a generic service.  To configure acuparse to send data to WeatherPoly, set the gennice URL to:

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

### MeteoBridge
MeteoBridge data is supported using the Home Weather Station weather network configuration.  For the API URL use

http://<node server ip>:8080/

MeteoBridge will send a space separated list of values. These are mapped to the node server's nodes using the value's position in that list. The table below shows the values and numeric position.

#### MegeoBridge Field list
MeteoBridge tag | Mapping field #
--------------- | ---------------
[DD]/[MM]/[YYYY] | 0
[hh]:[mm]:[ss] | 1
[th0temp-act:--] | 2
[th0hum-act:--] | 3
[th0dew-act:--] | 4
[wind0avgwind-act:--] | 5
[wind0wind-act:--] | 6
[wind0dir-act:--] | 7
[rain0rate-act:--] | 8
[rain0total-daysum:--] | 9
[thb0seapress-act:--] | 10
[wind0dir-act:--] | 11
[wind0wind-act=bft.0:--] | 12
m/s | 13
C | 14
hPa | 15
mm | 16
-- | 17
[thb0seapress-val60:--] | 18
[rain0total-monthsum:--] | 19
[rain0total-yearsum:--] | 20
[rain0total-ydaysum:--] | 21
[thb0temp-act:--] | 22
[thb0hum-act:--] | 23
[wind0chill-act:--] | 24
[th0temp-val60:--] | 25
[th0temp-dmax:--] | 26
[th0temp-dmaxtime:--] | 27
[th0temp-dmin:--] | 28
[th0temp-dmintime:--] | 29
[wind0avgwind-dmax:--] | 30
[wind0avgwind-dmaxtime:--] | 31
[wind0wind-dmax:--] | 32
[wind0wind-dmaxtime:--] | 33
[thb0seapress-dmax:--] | 34
[thb0seapress-dmaxtime:--] | 35
[thb0seapress-dmin:--] | 36
[thb0seapress-dmintime:--] | 37
[mbsystem-swversion:--] | 38
[mbsystem-buildnum:--] | 39
[wind0wind-max10:--] | 40
-- | 41
-- | 42
[uv0index-act:--] | 43
-- | 44
[sol0rad-act:--] | 45
[wind0dir-avg10:--] | 46
[rain0total-sum60:--] | 47
-- | 48
[mbsystem-daynightflag:--] | 49
-- | 50
[wind0dir-avg10:--] | 51
-- | 52
m | 53
-- | 54
[mbsystem-daylength:--] | 55
-- | 56
-- | 57
[uv0index-dmax:--] | 58
[th0hum-dmax:--] | 59
[th0hum-dmaxtime:--] | 60
[th0hum-dmin:--] | 61
[th0hum-dmintime:--] | 62
[th0dew-dmax:--] | 63
[th0dew-dmaxtime:--] | 64
[th0dew-dmin:--] | 65
[th0dew-dmintime:--] | 66
[th0temp-val15:â€”] | 67
[th0hum-val15:â€”] | 68
[th0dew-val15:â€”] | 69
[thb0temp-val15:â€”] | 70
[thb0hum-val15.0:--] | 71
[wind0wind-avg15:â€”] | 72
[wind0wind-avg30:â€”] | 73
[lgt0energy-act:--] | 74
[lgt0dist-act:--] | 75
[lgt0dist-age:--] | 76
[lgt0total-daysum.0:--] | 77
[lgt0total-monthsum.0:--] | 78
[lgt0total-yearsum.0:--] | 79
[sol0rad-dmax:--] | 80
[mbsystem-uptime:â€”-] | 81
[th0temp-ydmax:--] | 82
[th0temp-ydmaxtime:--] | 83
[th0temp-ydmin:--] | 84
[th0temp-ydmintime:--] | 85
[th0temp-mmax:--] | 86
[th0temp-mmaxtime:--] | 87
[th0temp-mmin:--] | 88
[th0temp-mmintime:--] | 89
[th0temp-ymax:--] | 90
[th0temp-ymaxtime:--] | 91
[th0temp-ymin:--] | 92
[th0temp-ymintime:--] | 93
[wind0wind-ydmax:--] | 94
[wind0wind-ydmaxtime:--] | 95
[wind0wind-mmax:--] | 96
[wind0wind-mmaxtime:--] | 97
[wind0wind-ymax:--] | 98
[wind0wind-ymaxtime:--] | 99
[rain0total-ydmax:--] | 100
[rain0total-mmax:--] | 101
[rain0total-mmaxtime:--] | 012
[rain0total-ymax:--] | 103
[rain0total-ymaxtime:--] | 104
[sol0rad-dmax:--] | 105
[sol0rad-dmaxtime:--] | 106
[sol0rad-ydmax:--] | 107
[sol0rad-ydmaxtime:--] | 108
[sol0rad-mmax:--] | 109
[sol0rad-mmaxtime:--] | 110
[sol0rad-ymax:--] | 111
[sol0rad-ymaxtime:â€”] | 112
[uv0index-dmaxtime:--] | 113
[uv0index-ydmax:--] | 114
[uv0index-ydmaxtime:--] | 115
[uv0index-mmax:--] | 116
[uv0index-mmaxtime:--] | 117
[uv0index-ymax:--] | 118
[uv0index-ymaxtime:â€”] | 119
[thb0temp-dmax:--] | 120
[thb0temp-dmin:--] | 121
