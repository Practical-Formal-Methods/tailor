<img src="https://numairmansur.github.io/tailor.png" width="230"/><img src="https://upload.wikimedia.org/wikipedia/en/4/4c/LLVM_Logo.svg" alt="llvm logo" width=280 height=180 /><img src="http://i.imgur.com/IDKhq5h.png" alt="crab logo" width=260 height=180 />

<a href="https://travis-ci.org/seahorn/crab-llvm"><img src="https://travis-ci.org/seahorn/crab-llvm.svg?branch=master" title="Ubuntu 16.04 LTS 64bit, g++-5"/></a>

Tailor is a framework to automatically tune **CRAB** abstract interpreter to the code
under analysis and any given resource constraints. 

# Installation
We will first install the **CRAB** abstract interpreter and then the **Tailor** tuning framework on top of it.

## > Installing CRAB

### Requirements 
CRAB is written in C++ and uses heavily the Boost library. The
main requirements are:

- Modern C++ compiler supporting c++11
- Boost >= 1.62
- GMP 
- MPFR (if `-DCRAB_USE_APRON=ON` or `-DCRAB_USE_ELINA=ON`)

In linux, you can install requirements typing the commands:

     sudo apt-get install libboost-all-dev libboost-program-options-dev
     sudo apt-get install libgmp-dev
     sudo apt-get install libmpfr-dev	

To run tests you need to install `lit` and `OutputCheck`. In Linux:

     apt-get install python-pip
     pip install lit
     pip install OutputCheck

### Installation

We will install Crab with Elina. 

     mkdir build && cd build
     cmake -DCMAKE_INSTALL_PREFIX=_DIR_ -DCRAB_USE_LDD=ON -DCRAB_USE_ELINA=ON ../
     cmake --build . --target extra                 
     cmake --build . --target crab && cmake ..
     cmake --build . --target ldd && cmake ..
     cmake --build . --target elina && cmake ..
     cmake --build . --target llvm && cmake ..                
     cmake --build . --target install 

### Checking installation

To run some regression tests:

     cmake --build . --target test-simple

## > Installing Tailor

```
cd ..
virtualenv --python=/usr/bin/python2.7 venv 
source venv/bin/activate
python setup.py install
```

# Don't want to install?
You can also use our CAV artifact which is packaged as a VM image with everything
pre-configured and pre-installed. Download the VM image from [here](https://zenodo.org/record/4719604#.YIaYzC0RpQM).

### How to run the VM?
Download the above OVA file. Start VirtualBox, click on File -> Import Appliance,
select the downloaded OVA file -> continue -> import.
Once imported, select the image "tailorVM" and press Start.
There will be a README.txt file waiting for you in a folder named ARTIFACT on the Desktop.


# Usage
To run TAILOR. Just type:
   
     tailor --program=/path/to/tailor/benchmarks/libcurl_la-vtls_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc 
       
   Where "libcurl_la-vtls_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc" is just an example program in the benchmarks
   folder.
   When you run this command, TAILOR will ask if you are happy with the parameters.
   After pressing "y", TAILOR will then start tuning CRAB for this program and return the best CRAB configuration.
   
   To change the number of iterations used in the optimization loop, use the --iterations flag. For example:
   
      tailor --program=/benchmarks/libcurl_la-vtls_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc --iterations=20
      

   While tuning, TAILOR generates different CRAB configurations. To set a timeout (in seconds) for each configuration, use the --timeout flag. For example:
   
      tailor --program=/benchmarks/libcurl_la-vtls_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc --timeout=5
   
   In the paper, we experimented with 4 optimization algorithms (sa, rs, hc and dars). You can specify the algorithm using the --algo flag. For example: 
   
      tailor --program=/benchmarks/libcurl_la-vtls_DivByZeroCheck_IntOverflowManualCheck_BufferOverflowCheck_UseAfterFreeShadowCheck.bc --algo=rs

