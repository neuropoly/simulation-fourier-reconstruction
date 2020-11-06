# simulation-fourier-reconstruction
Code to investigate what might cause the different Fourier-related artifacts that we encounter during our experiments.

Currently, the code located in `code/FFT_scripts.m` is a Matlab file in which an image (`code/brain_MRI.jpg`) is loaded and Fourier transformed. Modifications are then applied to its Fourier transform. These modifications depend on the script that is run (e.g Ghosting, aliasing...). The image is then inverse Fourier transformed and displayed to observe the effect of the modifications in the Fourier domain. To run a script, simply click on it and run `ctrl`+`enter`. 

It has been tested in MatLab 2020b.
