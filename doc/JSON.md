STEPS TO BUILD AND COMPILE THE PROJECT
=======================================

After Installing the prerequisites

Step 1 : We first need to build the sail parser.
        i) Find a directory to clone that repository, and make that directory your current working directory.
       ii) `git clone -b json https://github.com/ThinkOpenly/sail`
      iii) `cd sail`
       iv) `make`

Step 2 : Then, set up the environment for building in the RISC-V Sail repository:
        i) `eval $(opam env)`
       ii) `export PATH=<path-to-sail-repository>:$PATH`

Step 3 : Clone this sail-riscv repository.

Step 4 : Within that clone : `make json`