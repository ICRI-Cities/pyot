# PyoT
## The Python-base Framework for IoT Nodes
PyoT provides a convient and robust framework for implementing software/firmware on Intel IoT Nodes.
Using a system of breaking down an IoT Node's hardware into a conceptual hierarchy, PyoT enables new
node configurations to be added quickly and easily. This allows data from sensors to be collected and pushed
to backend data stores automatically from the configuration.
## PyoT's Hierarchy
PyoT views any IoT Node as a tree of peripherals, starting with the root peripherals, or platform. This platform
provides the various interfaces contained within the hardware as software ports, enabling other peripherals to
connect to it. For example, the Intel Galileo platform provides a number of GPIO ports, some AIN ports, two UART ports,
one SPI and one I2C ports for other peripherals to connect to. The connections are determined at runtime by the
configuration file.