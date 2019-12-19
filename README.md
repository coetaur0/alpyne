# Alpyne - Algebraic Petri Nets with Python

[![Build Status](https://travis-ci.com/coetaur0/alpyne.svg?branch=master)](https://travis-ci.com/coetaur0/alpyne)
[![codecov](https://codecov.io/gh/coetaur0/alpyne/branch/master/graph/badge.svg)](https://codecov.io/gh/coetaur0/alpyne)

**_Alpyne_** is a package designed for the construction and verification of Algebraic Petri Nets with Python.

_Algebraic Petri Nets_ (APNs) are a high order variant of Petri Nets, a class of models typically used
in the verification of concurrent software. The objective of Alpyne is to provide a framework to build
models of concurrent programs with APNs and to automatically check properties on them.

---

## Installation

To install _Alpyne_, simply clone this repository and run the command `pip3 install --upgrade .` at its
root (and preferably inside of a [virtual environment](https://docs.python.org/3/tutorial/venv.html)).
Once this is done, the package can be used like any other Python library.

---

## Usage

### Algebraic Data Types (ADTs)

Algebraic Petri Nets are built on top of the concept of _Algebraic Data Types_ (a.k.a. ADTs -- mathematically
formalised data structures described with the help of _many-sorted algebrae_, _axioms_ and _rewrite rules_ --
see the book by [Sannella and Tarlecki](https://www.springer.com/gp/book/9783642173356) for an in-depth 
discussion on the subject).

Before an Algebraic Petri Net can be built, the sorts of the terms it uses as tokens need to be defined. This
can be done with the `adt` module of this package. Examples of definitions of ADTs can be found in the 
*/alpyne/adts* folder of this repository, where the ADTs of base sorts such as booleans or naturals are defined.

### Algebraic Petri Nets (APNs)

To define and use APNs, the `apn` module of this package can be used. An example of script that builds and
executes an APN to compute the Fibonacci sequence is provided in the */examples* folder of this repository.
