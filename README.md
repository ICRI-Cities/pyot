# PyoT
## The Python-base Framework for IoT Nodes
PyoT provides a convient and robust framework for implementing software/firmware on Intel IoT Nodes. Using a system of breaking down an IoT Node's hardware into a conceptual hierarchy, PyoT enables new node configurations to be added quickly and easily. This allows data from sensors to be collected and pushed to backend data stores automatically from the configuration.

## PyoT's Hierarchy
PyoT views any IoT Node as a tree of peripherals, starting with the root peripherals, or platform. From there, a number of
peripherals are children of the platform, each containing endpoints (discussed below) and possibly more peripherals as children of their own. The platform (or parent peripheral) provides the various interfaces contained within the hardware as software ports, enabling other peripherals to connect to it. For example, the Intel Galileo platform provides a number of GPIO ports, some AIN ports, two UART ports, one SPI and one I2C ports for other peripherals to connect to. The connections are determined at runtime by the configuration file.

Most peripherals also provide various endpoints which can be access. These include the ports mentioned above, as well as any sensors or actuators that are part of that peripheral. Endpoints also include any comm links between the node and a backend. These endpoints give the peripheral actual functionality, with ports, sensors, actuators and comms each having a rigidly defined API for other peripherals to interact through. Ports have many APIs to best match the protocol their represent (like a single transfer method for SPI, while separate reads and writes for GPIO, etc). Endpoint sensors have just `read` while comms and have `send` (and have `poll` for pulling down actuations). All important functionality for actually reading a sensor is contained in it's `read` method.

Connections and references to the various peripherals and endpoints is achieved with a simple Unix-like file structure. For instance, if there were a peripheral with the name 'p1' with a sensor endpoint 'temperature' that is an immediate child to the platform name 'myPlatform', the object reference to the sensor endpoint would be '/myPlatform/p1:temperature'. This format enables the use of '.' and '..' in code and the configuration file to reference the peripheral and the parent peripheral respectively without having to know the full path. For instance, a common parameter needed by sensors on a child peripheral is the port to which they are connected on the parent. As such, the reference '../.:port_name' can be used to connect to that port without needing to know the parents name or full path (Note that '..:port_name' is not accepted, you must include at least one '/' to reference a peripheral to which you are not a member).

Each peripheral can also create a pins object which will allow the various ports to automatically manage which peripherals are connected to which physical pins (ie, when a port is taken, there must be some way of remembering which pins are assigned to which connected peripheral as ports can allow multiple peripherals to connect to it).

## Abstraction Construction
At startup, PyoT will examine the configuration file and construct the software hierarchy defined. This begins with the platform and recursively through all the peripherals via their `create` method. Once this completes, all the peripheral objects are created. In order to create endpoints for each of these peripherals, the next phase of the abstraction construction is the build phase. In this phase, the `build` method of all peripherals is called. Here, endpoints as added to the peripherals `endpoints` object, via the `add` method on the endpoints object. Then, the `build` method for all the added endpoints is called.

The next phase is the connect phase, in which the `connect` method is called for each peripheral and their endpoints. This phase is intended for peripherals and endpoints gathering any references needed to operate, such as references to their parent's ports to interact with in later methods. Modules use the `find` method to get a reference to the object, and then must call the object's `grant` method to actually use it, which, for example, prevents multiple sensors from using the same port. The `grant` method also takes in various standard configuration settings as a python dictionary, allowing ports to be properly configured for the module requesting them, such as selecting the GPIO direction or UART baudrate.

The final phase is the init phase, in which the `init` method is called for each peripheral and their endpoints. Here, any kind of initialization is preformed, whether its interfacing through the ports established in the connect phase to physical hardware and setting it up, or creating a communications link to a backend.

Each of these methods takes in a dictionary of parameters that are taken from the configuration file. This allows each module in the system to take in whatever special parameters they need in a portable way. For example, a communication endpoint might be the URL and port of its backend in the init phase while a sensor might need a reference to the specific port to connect to in the connect phase.

Once all of these phases completes, the PyoT framework is ready to being reading from sensors and sending data to the backend.

## Usage
In terms of usage, one should run the main.py script. This will automatically start up any python scripts (.py) in the scripts directory with the arguments provided in the .arg file of the same name (for example, name.py will be started with the arguments provided in name.arg if the file exists). The scripts are run in the background and all output from the scripts will be sent to `/dev/kmsg`. main.py should be run at boot, as some scripts might reboot the machine in certain scenarios (for example, the watchdog.py script will reboot the system periodically as well as if internet is lost or the script pyot.py is killed).

The most important part of setting up pyot to run smoothly is providing the correct configuration. This file is a JSON file will certain parameters and is a commandline argument of pyot.py. An example of this file is provided in the config directory. Note that is has a few parameters for how long to wait before sampling all sensors to send to the backend as well as how long to wait before sending all these readings to the backend. The list of objects in the sensors list are those sensors that will be sent to all backends, where name is some unique name usually used in IoT platforms to identify a timeseries and path is the full path to the endpoint of the sensor from which to take readings. These backends are specified in the iot list, where the name is some unique name and the path is the full path to the comm endpoint to use to send data. Finally, the platform object contains the entire hierarchy, with a peripheral object. Peripherals have the following parameters: name, a name to use in the path hierarchy (unique among children of a single node, just like directories in most file systems); class, the class to use (from pyotlib.peripherals package) for the peripheral object (note, pyot.py will call `{class}.create(params)`); peripherals, a list of more peripheral object that are the children of the current peripheral object; params, a object containing objects will the names of the endpoints as parameters (or "." to refer to the peripheral itself), each with a params object. A params object contains three parameters, build, connect and init, which refer to objects with whatever parameters (these depend on the class and are class-specific) are needed at each of these stages for the module whose name appears as a parameter for the given param object.

## Full Descriptions

### Configuration File

Configuration files contain a single `root` object.

##### Root Object
`threadRestartRate` - Time in between checks to be sure threads used to read data from sensors and send data to the backend are checked for liveness (and restarted if they've been killed). [seconds]

`sensorSampleRate` - Rate at which the sampling thread will attempt to sample the sensors provided in the sensors list. [seconds]

`iotSendRate` - Rate at which the sending thread will attempt to send the sensor data to the IoT backends. [in seconds]

`timer` - Path to an object to read to get the timestamp for data sent to the backend, note that "default" will use the node's system time. [path]
  
`sensors` - List of `sensor` objects whose readings will be sent to the backends given in the `iot` list. [list]

`iot` - List of `iot` objects that readings from the sensors given in the `sensors` list. [list]

`platform` - A `peripheral` object that serves as the base for the hierarchy. [object]

##### Sensor Object
`name` - A unique name, usually an uuid from the IoT backend. [string]

`path` - Path to the sensor endpoint from which to take readings. [path]

`numSamples` - The number of samples to take for a single reading cycle. The median of these samples is used as the actual value. [number]

`timeBetweenSamples` - The time between taking samples during a reading cycle. [seconds]

  
##### IoT Object
`name` - A unique name. [string]

`path` - Path to the comm endpoint to use to send readings. [path]

##### Peripheral Object
`name` - Name to use for this peripheral in the hierarchy (cannot be shared with any other peripheral sharing the same parent, but can be shared otherwise). [string]

`class` - Python class to use within the pyotlib.peripherals package that implements this peripheral. [class]

`params` - A `paramslist` object, which defines the various parameters for each stage of the abstraction construction for the endpoint defined by the parameter in the `paramlist`. [object]

`peripherals` - List of the children peripherals of this peripheral. [object]

##### ParamsList Object
`*` - A `params` object for any endpoint of the current peripheral (or "." for the current peripheral itself). Optional (`params` in the `peripheral` object may be left an empty object). [object]

##### Params Object
`build` - An object containing all the parameters to pass into the `build` method of the module specified by the parameter of the `paramslist` object to which this object is the child. Module-specific. [object]

`connect` - An object containing all the parameters to pass into the `connect` method of the module specified by the parameter of the `paramslist` object to which this object is the child. Module-specific. [object]

`init` - An object containing all the parameters to pass into the `init` method of the module specified by the parameter of the `paramslist` object to which this object is the child. Module-specific. [object]

### pyotlib Package



### Main Package

These modules are all part of the pyotlib package proper.

##### tree

This module is responsible for managing the hierarchy; most likely users will not need to modify or use this module.

##### channel

This module provides a producer-consumer queue interface between the sensor reading thread (producer) and backend ending thread (consumer). Most likely, users will not need to modify or use this class. However, as it currently uses a Python Queue, users might want to improve this class to use something that can survive reboots; so long as the API for the channel is unchanged.

##### printlib

This module enables printing for and module. Users should use this module over calling Python's print natively.

`Msg(string)` - Prints an informational message given by string.

`Wrn(string)` - Prints a warning message given by string.

`Err(string)` - Prints an error message given by string. Will also print the stacktrace iff `debug` is set.

`Dbg(string)` - Prints a debug message given by string iff `debug` is set.

#### classes Package

These modules are part of the pyotlib.classes package.

##### interface

Contains several important base classes for port protocols.

##### peripheral

Contains several important base classes for creating peripherals.

##### pin

Contains the `Pins` class, which is used for keeping track of the physical pins used by a peripheral or endpoint. There should only be one `Pins` object per peripheral.

`Pins(pinList)` - Creates a new `Pins` object, which manages a list of pins in the given list. Note that pins in the list should be integers.

`Pins.assign(obj, pins)` - Assigns the pins in the `pins` list to the given object, usually an endpoint. This function is needed for calls to `Pins.request` to work correctly, and creates a reference to this `Pins` object as `obj.pins`. `pins` must be a subset of the pin list given to the constructor.

`Pins.request(obj, pins)` - Marks the given pins in the list `pins` as being used. Returns `True` if successful or `False` is some of the requested pins are already in use. If `pins` is left out, all the pins assigned to the given object are requested.

`Pins.getPins(obj)` - Returns a list of all the pins assigned to the given object.