STEPS TO BUILD AND COMPILE THE PROJECT
=======================================

After Installing the prerequisites

1.  We first need to build the sail parser.
    1. Find a directory to clone this repository, and make that directory your current working directory.
    2. `git clone https://github.com/ThinkOpenly/sail`
    3. `cd sail`
    4. `make`

2.  Then, set up the environment for building in the RISC-V Sail repository:
    1. `eval $(opam env)`
    2. `export PATH=<path-to-sail-repository>:$PATH`

3.  Clone this sail-riscv repository.

4.  Within that clone : `make json`