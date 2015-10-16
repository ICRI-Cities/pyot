# PyoT
## The Python-base Framework for IoT Nodes
PyoT provides a convient and robust framework for implementing software/firmware on Intel IoT Nodes. Using a system of breaking down an IoT Node's hardware into a conceptual hierarchy, PyoT enables new node configurations to be added quickly and easily. This allows data from sensors to be collected and pushed to backend data stores automatically from the configuration.

## PyoT's Hierarchy
PyoT views any IoT Node as a tree of peripherals, starting with the root peripherals, or platform. From there, a number of
peripherals are children of the platform, each containing endpoints (discussed below) and possibly more peripherals as children of their own. The platform (or parent peripheral) provides the various interfaces contained within the hardware as software ports, enabling other peripherals to connect to it. For example, the Intel Galileo platform provides a number of GPIO ports, some AIN ports, two UART ports, one SPI and one I2C ports for other peripherals to connect to. The connections are determined at runtime by the configuration file.

Most peripherals also provide various endpoints which can be access. These include the ports mentioned above, as well as any sensors or actuators that are part of that peripheral. Endpoints are also and comm link between the node and a backend. These endpoints give the peripheral actual functionality, with ports, sensors, actuators and comm each having a rigidly defined API for other peripherals to interact through.

Connections and references to the various peripherals and endpoints is achieved with a simple Unix-like file structure. For instance, if there were a peripheral with the name 'p1' with a sensor endpoint 'temperature' that is an immediate child to the platform name 'myPlatform', the object reference to the sensor endpoint would be '/myPlatform/p1:temperature'.

## Abstraction Construction
At startup, PyoT will examine the configuration file and construct the software hierarchy defined. This begins with the platform and recursively through all the peripherals via their `create` method.