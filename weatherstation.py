#!/usr/bin/env python3
"""
Polyglot v2 node server for local weather station data.
Copyright (c) 2018 Robert Paauwe
"""
import polyinterface
import sys
import time
import datetime
#import urllib3
import urllib
import json
import socket
import math
import threading
import struct
import write_profile
import uom
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import http.server

LOGGER = polyinterface.LOGGER

class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'WeatherPoly'
        self.address = 'weather'
        self.primary = self.address
        self.port = 8080
        self_server_running = False
        self.units = ""
        self.in_units = ""
        self.temperature_list = {}
        self.humidity_list = {}
        self.pressure_list = {}
        self.wind_list = {}
        self.rain_list = {}
        self.light_list = {}
        self.lightning_list = {}
        self.map = {}
        self.myConfig = {}

        self.poly.onConfig(self.process_config)

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        if 'customParams' in config and self.myConfig:
            if config['customParams'] != self.myConfig:
                LOGGER.debug("Found difference with saved configuration.")
                self.removeNoticesAll()
                self.set_configuration(config)
                self.map_nodes(config)
                self.discover()
                try:
                    if config['customParams']['Port'] != self.myConfig['Port']:
                        self.addNotice("Restart node server for Port change to take effect")
                except:
                    self.addNotice("Must have a Port parameter set.")

                self.myConfig = config['customParams']

    def start(self):
        LOGGER.info('Starting WeatherPoly Node Server')
        self.set_logging_level()
        self.check_params()
        LOGGER.info('Calling discover')
        self.discover()

        LOGGER.info('starting web server thread')
        self.data_thread = threading.Thread(target = self.web_server)
        self.data_thread.daemon = True
        self.data_thread.start()

        #for node in self.nodes:
        #       LOGGER.info (self.nodes[node].name + ' is at index ' + node)
        LOGGER.info('WeatherPoly Node Server Started.')

    def shortPoll(self):
        pass

    def longPoll(self):
        pass

    def query(self):
        for node in self.nodes:
            self.nodes[node].reportDrivers()

    def discover(self, *args, **kwargs):
        """
        Add nodes for basic sensor type data
                - Temperature (temp, dewpoint, heat index, wind chill, feels)
                - Humidity
                - Pressure (abs, sealevel, trend)
                - Wind (speed, gust, direction, gust direction, etc.)
                - Precipitation (rate, hourly, daily, weekly, monthly, yearly)
                - Light (UV, solar radiation, lux)
                - Lightning (strikes, distance)

        The nodes need to have thier drivers configured based on the user
        supplied configuration. To that end, we should probably create the
        node, update the driver list, set the units and then add the node.
        """

        LOGGER.info("Creating nodes.")
        t_drvs = []
        h_drvs = []
        p_drvs = []
        w_drvs = []
        r_drvs = []
        l_drvs = []
        s_drvs = []

        for key in self.map:
            info = self.map[key]
            if info['node'] == 'temperature':
                t_drvs.append( {
                    'driver': info['driver'],
                    'value': 0,
                    'uom': uom.UOM[info['units']]
                    })
            elif info['node'] == 'humidity':
                h_drvs.append( {
                    'driver': info['driver'],
                    'value': 0,
                    'uom': uom.UOM[info['units']]
                    })
            elif info['node'] == 'pressure':
                p_drvs.append( {
                    'driver': info['driver'],
                    'value': 0,
                    'uom': uom.UOM[info['units']]
                    })
            elif info['node'] == 'wind':
                w_drvs.append( {
                    'driver': info['driver'],
                    'value': 0,
                    'uom': uom.UOM[info['units']]
                    })
            elif info['node'] == 'rain':
                r_drvs.append( {
                    'driver': info['driver'],
                    'value': 0,
                    'uom': uom.UOM[info['units']]
                    })
            elif info['node'] == 'light':
                l_drvs.append( {
                    'driver': info['driver'],
                    'value': 0,
                    'uom': uom.UOM[info['units']]
                    })
            elif info['node'] == 'lightning':
                s_drvs.append( {
                    'driver': info['driver'],
                    'value': 0,
                    'uom': uom.UOM[info['units']]
                    })
            else:
                LOGGER.debug(' - Skipping, no such node.')

        if len(t_drvs) > 0:
            LOGGER.info("Creating Temperature node")
            node = TemperatureNode(self, self.address, 'temperature',
                    'Temperatures')
            node.SetUnits(self.units, self.in_units)
            node.drivers = t_drvs;
            self.addNode(node)
        else:
            LOGGER.info('Deleting orphaned temperature node')
            self.delNode('temperature')

        if len(h_drvs) > 0:
            LOGGER.info("Creating Humidity node")
            node = HumidityNode(self, self.address, 'humidity', 'Humidity')
            node.drivers = h_drvs
            self.addNode(node)
        else:
            LOGGER.info('Deleting orphaned humidity node')
            self.delNode('humidity')

        if len(p_drvs) > 0:
            LOGGER.info("Creating Pressure node")
            node = PressureNode(self, self.address, 'pressure', 'Barometric Pressure')
            node.SetUnits(self.units, self.in_units)
            node.drivers = p_drvs
            self.addNode(node)
        else:
            LOGGER.info('Deleting orphaned pressure node')
            self.delNode('pressure')

        if len(w_drvs) > 0:
            LOGGER.info("Creating Wind node")
            node = WindNode(self, self.address, 'wind', 'Wind')
            node.SetUnits(self.units, self.in_units)
            node.drivers = w_drvs
            self.addNode(node)
        else:
            LOGGER.info('Deleting orphaned wind node')
            self.delNode('wind')

        if len(r_drvs) > 0:
            LOGGER.info("Creating Precipitation node")
            node = PrecipitationNode(self, self.address, 'rain', 'Precipitation')
            node.SetUnits(self.units, self.in_units)
            node.drivers = r_drvs
            self.addNode(node)
        else:
            LOGGER.info('Deleting orphaned rain node')
            self.delNode('rain')

        if len(l_drvs) > 0:
            LOGGER.info("Creating Light node")
            node = LightNode(self, self.address, 'light', 'Illumination')
            node.drivers = l_drvs
            self.addNode(node)
        else:
            LOGGER.info('Deleting orphaned light node')
            self.delNode('light')

        if len(s_drvs) > 0:
            LOGGER.info("Creating Lightning node")
            node = LightningNode(self, self.address, 'lightning', 'Lightning')
            node.SetUnits(self.units, self.in_units)
            node.drivers = s_drvs
            self.addNode(node)
        else:
            LOGGER.info('Deleting orphaned lightning node')
            self.delNode('lightning')


    def delete(self):
        self.stopping = True
        self.server.Stop = True
        LOGGER.info('Removing WeatherPoly node server.')

    def stop(self):
        self.stopping = True
        self.server.Stop = True
        self.server.socket.close()
        LOGGER.debug('Stopping WeatherPoly node server.')

    def check_params(self):

        self.set_configuration(self.polyConfig)

        # Make sure they are in the params
        LOGGER.info("Adding configuation")
        self.addCustomParam({
                    'Port': self.port,
                    'Units': self.units,
                    'IncomingUnits': self.in_units,
                    })

        self.map_nodes(self.polyConfig)
        self.myConfig = self.polyConfig['customParams']

        # Remove all existing notices
        LOGGER.info("remove all notices")
        self.removeNoticesAll()

        # Add a notice?

    def set_configuration(self, config):
        default_port = 8080
        default_elevation = 0

        LOGGER.info("Check for existing configuration value")

        if 'Port' in config['customParams']:
            self.port = int(config['customParams']['Port'])
        else:
            self.port = default_port

        if 'Units' in config['customParams']:
            self.units = config['customParams']['Units']
        else:
            self.units = 'metric'

        if 'IncomingUnits' in config['customParams']:
            self.in_units = config['customParams']['IncomingUnits']
        else:
            self.in_units = 'metric'

    def map_nodes(self, config):
        # Build up our data mapping tables. The customParams keys will
        # look like temperature-main and the value will match something
        # from the weather software (field #, key, etc.)
        #
        # What we really need to be able to do is map from the data
        # recieved to a node and driver.  So ideally, we have a dictionary
        # with the weather software "key" as the dictionary key and the
        # dictionary value be another dictionary with node name and driver.
        LOGGER.info("Trying to create a mapping")

        self.map.clear()
        self.temperature_list.clear()
        self.humidity_list.clear()
        self.pressure_list.clear()
        self.wind_list.clear()
        self.rain_list.clear()
        self.light_list.clear()
        self.lightning_list.clear()

        for key in config['customParams']:
            if not '-' in key:
                continue

            vmap = key.split('-')
            vval = config['customParams'][key]
            # Mapping needs to be a list for each node and each list item
            # is a 2 element list (or a dictionary?)
            LOGGER.info('MAPPING %s to %s' % (vval, key))

            if vmap[0] == 'temperature':
                self.temperature_list[vmap[1]] = 'I_TEMP_F' if self.units == 'us' else 'I_TEMP_C'
                self.map[vval] = {
                        'node': 'temperature',
                        'driver': write_profile.TEMP_DRVS[vmap[1]],
                        'units': self.temperature_list[vmap[1]]
                        }

            elif vmap[0] == 'humidity':
                self.humidity_list[vmap[1]] = 'I_HUMIDITY'
                self.map[vval] = {
                        'node': 'humidity',
                        'driver': write_profile.HUMD_DRVS[vmap[1]],
                        'units': self.humidity_list[vmap[1]]
                        }

            elif vmap[0] == 'pressure':
                if vmap[1] == 'trend':
                    self.pressure_list[vmap[1]] = 'I_TREND'
                else:
                    self.pressure_list[vmap[1]] = 'I_INHG' if self.units == 'us' else 'I_MB'
                self.map[vval] = {
                        'node': 'pressure',
                        'driver': write_profile.PRES_DRVS[vmap[1]],
                        'units': self.pressure_list[vmap[1]]
                        }

            elif vmap[0] == 'wind':
                if 'speed' in vmap[1]:
                    self.wind_list[vmap[1]] = 'I_KPH' if self.units == 'metric' else 'I_MPH'
                else:
                    self.wind_list[vmap[1]] = 'I_DEGREE'
                self.map[vval] = {
                        'node': 'wind',
                        'driver': write_profile.WIND_DRVS[vmap[1]],
                        'units': self.wind_list[vmap[1]]
                        }

            elif vmap[0] == 'rain':
                if 'rate' in vmap[1]:
                    self.rain_list[vmap[1]] = 'I_MMHR' if self.units == 'metric' else 'I_INHR'
                else:
                    self.rain_list[vmap[1]] = 'I_MM' if self.units == 'metric' else 'I_INCHES'
                self.map[vval] = {
                        'node': 'rain',
                        'driver': write_profile.RAIN_DRVS[vmap[1]],
                        'units': self.rain_list[vmap[1]]
                        }

            elif vmap[0] == 'light':
                self.light_list[vmap[1]] = write_profile.LITE_EDIT[vmap[1]]
                self.map[vval] = {
                        'node': 'light',
                        'driver': write_profile.LITE_DRVS[vmap[1]],
                        'units': self.light_list[vmap[1]]
                        }

            elif vmap[0] == 'lightning':
                if 'strike' in vmap[1]:
                    self.lightning_list[vmap[1]] = 'I_STRIKES'
                else:
                    self.lightning_list[vmap[1]] = 'I_KM' if self.units == 'metric' else 'I_MILE'
                self.map[vval] = {
                        'node': 'lightning',
                        'driver': write_profile.LTNG_DRVS[vmap[1]],
                        'units': self.lightning_list[vmap[1]]
                        }

        # Build the node definition
        LOGGER.info('Try to create node definition profile based on config.')
        write_profile.write_profile(LOGGER, self.temperature_list,
                self.humidity_list, self.pressure_list, self.wind_list,
                self.rain_list, self.light_list, self.lightning_list)

        # push updated profile to ISY
        try:
            self.poly.installprofile()
        except:
            LOGGER.error('Failed up push profile to ISY')

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all:')
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    def web_server(self):
        # Implement web server here
        try:
            #self.server = http.server.HTTPServer(('', self.port), weather_data_handler)
            self.server = Server(('', self.port), weather_data_handler)
            LOGGER.info('Started web server on port %d' % self.port)
            self_server_running = True
            self.server.serve_forever(self.map, self.nodes)
        except Exception as e:
            LOGGER.error('Web server failed to start. {}'.format(e))
            #self.server.socket.close()
            self_server_running = False
            self.addNotice("Failed to start weather monitoring service.")
            

    def SetUnits(self, u, i):
        self.units = u
        self.units_in = i

    def get_saved_log_level(self):
        if 'customData' in self.polyConfig:
            if 'level' in self.polyConfig['customData']:
                return self.polyConfig['customData']['level']

        return 0

    def save_log_level(self, level):
        level_data = {
            'level': level,
            }
        self.poly.saveCustomData(level_data)

    def set_logging_level(self, level=None):
        if level is None:
            try:
                level = self.get_saved_log_level()
            except:
                LOGGER.error('set_logging_level: get saved log level failed.')

            if level is None:
                level = 30

            level = int(level)
        else:
            level = int(level['value'])

        self.save_log_level(level)
        LOGGER.info('set_logging_level: Setting log level to %d' % level)
        LOGGER.setLevel(level)


    id = 'WeatherPoly'
    name = 'WeatherPolyPoly'
    address = 'weather'
    stopping = False
    hint = 0xffffff
    units = 'metric'
    commands = {
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'DEBUG': set_logging_level,
    }
    # Hub status information here: battery and rssi values.
    drivers = [
            {'driver': 'ST', 'value': 1, 'uom': 2},
            {'driver': 'GV0', 'value': 0, 'uom': 72},  # Air battery level
            {'driver': 'GV1', 'value': 0, 'uom': 72},  # Sky battery level
            {'driver': 'GV2', 'value': 0, 'uom': 25},  # Air RSSI
            {'driver': 'GV3', 'value': 0, 'uom': 25}   # Sky RSSI
            ]


class TemperatureNode(polyinterface.Node):
    id = 'temperature'
    hint = 0xffffff
    units = 'metric'
    units_in = 'metric'
    drivers = [ ]

    def SetUnits(self, u, i):
        self.units = u
        self.units_in = i

    # Assumes temp in C
    def Dewpoint(self, t, h):
        b = (17.625 * t) / (243.04 + t)
        rh = h / 100.0
        c = math.log(rh)
        dewpt = (243.04 * (c + b)) / (17.625 - c - b)
        return round(dewpt, 1)

    # Assumes temp in C and wind speed in m/s
    def ApparentTemp(self, t, ws, h):
        wv = h / 100.0 * 6.105 * math.exp(17.27 * t / (237.7 + t))
        at =  t + (0.33 * wv) - (0.70 * ws) - 4.0
        return round(at, 1)

    # Assumes temp in C and wind speed in m/s
    def Windchill(self, t, ws):
        # really need temp in F and speed in MPH
        tf = (t * 1.8) + 32
        mph = ws / 0.44704

        wc = 35.74 + (0.6215 * tf) - (35.75 * math.pow(mph, 0.16)) + (0.4275 * tf * math.pow(mph, 0.16))

        if (tf <= 50.0) and (mph >= 5.0):
            return round((wc - 32) / 1.8, 1)
        else:
            return t

    # Assumes temp in C
    def Heatindex(self, t, h):
        tf = (t * 1.8) + 32
        c1 = -42.379
        c2 = 2.04901523
        c3 = 10.1433127
        c4 = -0.22475541
        c5 = -6.83783 * math.pow(10, -3)
        c6 = -5.481717 * math.pow(10, -2)
        c7 = 1.22874 * math.pow(10, -3)
        c8 = 8.5282 * math.pow(10, -4)
        c9 = -1.99 * math.pow(10, -6)

        hi = (c1 + (c2 * tf) + (c3 * h) + (c4 * tf * h) + (c5 * tf *tf) + (c6 * h * h) + (c7 * tf * tf * h) + (c8 * tf * h * h) + (c9 * tf * tf * h * h))

        if (tf < 80.0) or (h < 40.0):
            return t
        else:
            return round((hi - 32) / 1.8, 1)

    # Convert temperature from incoming units to display units
    def convert(self, value):
        if self.units_in == 'us':
            if self.units != 'us':
                return round((value - 32) / 1.8, 2) # to C
        else:
            if self.units == 'us':
                return round((value * 1.8) + 32, 2) # to F
        return value

    def setDriver(self, driver, value):
        value = self.convert(value)
        super(TemperatureNode, self).setDriver(driver, round(value, 1), report=True, force=True)



class HumidityNode(polyinterface.Node):
    id = 'humidity'
    hint = 0xffffff
    units = 'metric'
    units_in = 'metric'
    drivers = [{'driver': 'ST', 'value': 0, 'uom': 22}]

    def SetUnits(self, u, i):
        self.units = u
        self.units_in = i

    def setDriver(self, driver, value):
        super(HumidityNode, self).setDriver(driver, value, report=True, force=True)

class PressureNode(polyinterface.Node):
    id = 'pressure'
    hint = 0xffffff
    units = 'metric'
    units_in = 'metric'
    drivers = [ ]
    mytrend = []


    def SetUnits(self, u, i):
        self.units = u
        self.units_in = i

    # convert station pressure in millibars to sealevel pressure
    def toSeaLevel(self, station, elevation):
        i = 287.05
        a = 9.80665
        r = 0.0065
        s = 1013.35 # pressure at sealevel
        n = 288.15

        l = a / (i * r)
        c = i * r / a
        u = math.pow(1 + math.pow(s / station, c) * (r * elevation / n), l)

        return (round((station * u), 3))

    # track pressures in a queue and calculate trend
    def updateTrend(self, current):
        t = 0
        past = 0

        if len(self.mytrend) == 180:
            past = self.mytrend.pop()

        if self.mytrend != []:
            past = self.mytrend[0]

        # calculate trend
        if ((past - current) > 1):
            t = -1
        elif ((past - current) < -1):
            t = 1

        self.mytrend.insert(0, current)
        return t

    def convert(self, value):
        if self.units_in == 'us':
            if self.units != 'us':
                return round(value / 0.02952998751, 3)
        else:
            if self.units == 'us':
                return round(value * 0.02952998751, 3)
        return value
        
    # We want to override the SetDriver method so that we can properly
    # convert the units based on the user preference.
    def setDriver(self, driver, value):
        value = self.convert(value)
        super(PressureNode, self).setDriver(driver, value, report=True, force=True)


class WindNode(polyinterface.Node):
    id = 'wind'
    hint = 0xffffff
    units = 'metric'
    units_in = 'metric'
    drivers = [ ]

    def SetUnits(self, u, i):
        self.units = u
        self.units_in = i

    def convert(self, value):
        if self.units_in == 'us' or self.units_in == 'uk':
            if self.units == 'metric':
                return round(value * 1.609344, 2)
        else:
            if self.units == 'us' or self.units == 'uk':
                return round(value / 1.609344, 2)
        return value

    def setDriver(self, driver, value):
        if (driver == 'ST' or driver == 'GV1' or driver == 'GV3'):
            value = self.convert(value)
        super(WindNode, self).setDriver(driver, value, report=True, force=True)

class PrecipitationNode(polyinterface.Node):
    id = 'precipitation'
    hint = 0xffffff
    units = 'metric'
    units_in = 'metric'
    drivers = [ ]
    hourly_rain = 0
    daily_rain = 0
    weekly_rain = 0
    monthly_rain = 0
    yearly_rain = 0

    prev_hour = 0
    prev_day = 0
    prev_week = 0

    def SetUnits(self, u, i):
        self.units = u
        self.units_in = i

    def hourly_accumulation(self, r):
        current_hour = datetime.datetime.now().hour
        if (current_hour != self.prev_hour):
            self.prev_hour = current_hour
            self.hourly = 0

        self.hourly_rain += r
        return self.hourly_rain

    def daily_accumulation(self, r):
        current_day = datetime.datetime.now().day
        if (current_day != self.prev_day):
            self.prev_day = current_day
            self.daily_rain = 0

        self.daily_rain += r
        return self.daily_rain

    def weekly_accumulation(self, r):
        current_week = datetime.datetime.now().day
        if (current_weekday != self.prev_weekday):
            self.prev_week = current_weekday
            self.weekly_rain = 0

        self.weekly_rain += r
        return self.weekly_rain

    def convert(self, value):
        if self.units_in == 'us':
            if self.units != 'us':
                return round(value / 0.03937, 2)
        else:
            if self.units == 'us':
                return round(value * 0.03937, 2)
        return value

        
    def setDriver(self, driver, value):
        value = self.convert(value)
        super(PrecipitationNode, self).setDriver(driver, value, report=True, force=True)

class LightNode(polyinterface.Node):
    id = 'light'
    units = 'metric'
    units_in = 'metric'
    hint = 0xffffff
    drivers = [ ]

    def SetUnits(self, u, i):
        self.units = u
        self.units_in = i

    def setDriver(self, driver, value):
        super(LightNode, self).setDriver(driver, value, report=True, force=True)

class LightningNode(polyinterface.Node):
    id = 'lightning'
    hint = 0xffffff
    units = 'metric'
    units_in = 'metric'
    drivers = [ ]

    def SetUnits(self, u, i):
        self.units = u
        self.units_in = i

    def convert(self, value):
        if self.units_in == 'us' or self.units_in == 'uk':
            if self.units == 'metric':
                return round(value * 1.609344, 1)
        else:
            if self.units == 'us' or self.units == 'uk':
                return round(value / 1.609344, 1)
        return value

    def setDriver(self, driver, value):
        if (driver == 'GV0'):
            value = self.convert(value)
        super(LightningNode, self).setDriver(driver, value, report=True, force=True)

class weather_data_handler(http.server.BaseHTTPRequestHandler):
    node_map = {}
    nodes = {}

    def log_message(self, format, *args):
        LOGGER.info("%s" % format%args)
        return

    # handle get requests
    def do_GET(self):
        message = "<head></head><body>Successful data submission</body>\n"

        # may want to move this below the response so we don't make
        # the client wait.
        self.process_data(self.path)

        self.send_response(200)  # OK
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(message.encode('utf_8'))

        return

    def do_POST(self):
        message = "<head></head><body>Successful data submission</body>\n"

        content_length = int(self.headers['content-Length'])
        post_data = self.rfile.read(content_length)

        self.process_post_data(self.path, post_data)

        self.send_response(200)  # OK
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(message.encode('utf_8'))

        return

    def process_data(self, path):
        # split the path into path/query components
        c = path.split('?')
        if len(c) > 1:
            data = urllib.parse.parse_qs(c[1])
            if 'mb.php' in c[0]:
                # MeteoBridge Home Weather Station template
                self.meteobridge(data)
            elif 'weather-display' in c[0]:
                # Custom Weather Display template
                self.weatherdisplay(data)
            elif 'weewx' in c[0]:
                # Custom WeeWX template
                self.weewx(data)
            elif 'cumulus' in c[0]:
                # Custom Cumulus template
                self.cumulus(data)
            elif 'acuparse' in c[0]:
                # Custom Acuparse template
                self.acuparse(data)
        return

    def process_post_data(self, path, data):
        if 'weewx' in path:
            self.weewx(data)
        return

    def meteobridge(self, data):
        # key = 'd'
        # data[key] = space separated list
        # Use node-value to field # mapping
        for key in data:
            fields = data[key][0].split(' ')
            for f in self.node_map:
                try:
                    i = int(f)
                except: 
                    continue

                m = self.node_map[f]

                try:
                    LOGGER.info(' - Set %s driver %s to %s' % 
                        (self.node_map[f]['node'], self.node_map[f]['driver'], fields[i]))

                    self.nodes[m['node']].setDriver(m['driver'], float(fields[i]))
                except Exception as e:
                    LOGGER.debug('  - setDriver failed %s  -> %s %s' % (f, m['node'], str(e)))

        return

    def weatherdisplay(self, data):
        LOGGER.debug('pressure = %s temp = %s' % (data['baro'], data['temp']))
        return

    def weewx(self, data):
        LOGGER.debug('Got some WeeWX data')
        fields = data.decode().split(' ')
        for f in self.node_map:
            try:
                i = int(f)
            except: 
                continue

            m = self.node_map[f]

            try:
                LOGGER.info(' - Set %s driver %s to %s' % 
                    (self.node_map[f]['node'], self.node_map[f]['driver'], fields[i]))

                self.nodes[m['node']].setDriver(m['driver'], float(fields[i]))
            except Exception as e:
                LOGGER.debug('  - setDriver failed %s  -> %s %s' % (f, m['node'], str(e)))
        return

    # convert cardinal direction to degrees
    def cardinal(self, direction):
        dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        try:
            ix = dirs.index(direction)
            return ix * 22.5
        except:
            LOGGER.error('Cannot convert ' + direction + ' to degrees')
            return 0

    def cumulus(self, data):
        # map key's to configuration node/driver
        LOGGER.debug('Got some cumulus data')
        for key in data:
            if key in self.node_map:
                m = self.node_map[key]
                LOGGER.info(' - Set %s driver %s to %s' % 
                        (self.node_map[key]['node'], self.node_map[key]['driver'], data[key]))

                # If pressure node trend driver the data isn't an integer but
                # a string.  Need to covnert the string to the proper int
                # representation of trend: 1, 2, 3
                if m['node'] == 'pressure' and m['driver'] == 'GV1':
                    if data[key][0] == 'Rising':
                        val = 2
                    elif data[key][0] == 'Falling':
                        val = 0
                    elif data[key][0] == 'Steady':
                        val = 1
                    elif data[key][0] == 'Rising slowly':
                        val = 3
                    elif data[key][0] == 'Rising rapidly':
                        val = 4
                    elif data[key][0] == 'Falling slowly':
                        val = 5
                    elif data[key][0] == 'Falling rapidly':
                        val = 6
                    else:
                        val = 7
                elif m['node'] == 'wind' and m['driver'] == 'GV0': # direction
                    if data[key][0].isnumeric():
                        val = float(data[key][0])
                    else:
                        val = self.cardinal(data[key][0])
                elif m['node'] == 'wind' and m['driver'] == 'GV2': # gust dir
                    if data[key][0].isnumeric():
                        val = float(data[key][0])
                    else:
                        val = self.cardinal(data[key][0])
                else:
                    val = float(data[key][0])

                self.nodes[m['node']].setDriver(m['driver'], val)
            else:
                LOGGER.info('map has %d entries, but not %s' % (len(self.node_map), key))
        return

    def acuparse(self, data):
        # map key's to configuration node/driver
        LOGGER.debug('Got some acuparse data')
        for key in data:
            if key in self.node_map:
                m = self.node_map[key]
                LOGGER.info(' - Set %s driver %s to %s' % 
                        (self.node_map[key]['node'], self.node_map[key]['driver'], data[key]))

                val = float(data[key][0])
                self.nodes[m['node']].setDriver(m['driver'], val)
            else:
                LOGGER.info('map has %d entries, but not %s' % (len(self.node_map), key))
        return



class Server(http.server.HTTPServer):
    stop = False

    def serve_forever(self, cfg_map, nodes):
        self.RequestHandlerClass.node_map = cfg_map
        self.RequestHandlerClass.nodes = nodes
        while not self.stop:
            http.server.HTTPServer.handle_request(self)
        #http.server.HTTPServer.serve_forever(self)

    def stop_server(self):
        self.stop = True

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('WeatherPoly')
        """
        Instantiates the Interface to Polyglot.
        """
        polyglot.start()
        """
        Starts MQTT and connects to Polyglot.
        """
        LOGGER.info('Calling Controller to create controller node')
        control = Controller(polyglot)
        """
        Creates the Controller Node and passes in the Interface
        """
        control.runForever()
        """
        Sits around and does nothing forever, keeping your program running.
        """
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
        """
        Catch SIGTERM or Control-C and exit cleanly.
        """
