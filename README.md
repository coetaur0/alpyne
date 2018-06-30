# ALgebraic PYthon NETs
Algebraic Petri Nets in Python

AlPyNet is a package that serves two purposes. First, it allows for the definition of algebraic data types (ADTs) and term 
rewriting systems. The second and main purpose of the library is however to provide a utility to build and use Algebraic Petri
Nets (APNs) in Python.

## Installation

To install AlPyNet, simply clone this repository and run the command `pip3 install --upgrade .`. The package is also available 
on PyPi and can be directly installed with the command `pip3 install alpynet`.

## Usage

### ADTs

To define and use ADTs, the `alpynet.adt` module of this package can be used. Several examples of definitions of ADTs are 
provided with this package in the */alpynet/adts* folder of this repository.

### APNs

To define and use APNs, the `alpynet.apn` module of this package can be used. An example of script that builds and executes an 
APN to compute the Fibonacci sequence is provided in the */examples* folder of this repository.
