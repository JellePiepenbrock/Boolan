# Boolan

Boolan is a Python package to determine characteristics of Boolean functions. It uses the fact that Boolean functions can be expressed as multilinear polynomials over a two valued field {1, -1}. Transforming the Boolean functions into this polynomial (which is close to a Fourier transform), exposes all kinds of information about the behavior of the function, which can be gleaned from the Fourier coefficients of the polynomial.

Boolan uses the Sage computer algebra environment to do its rewriting. In order to install and make use of Boolan, one first has to install Sage. The easiest and most foolproof way to do this, on Ubuntu, is via Conda. To avoid conflicts, one should make a new environment where Sage is installed. 

Add the conda-forge package channel to config
>  conda config --add channels conda-forge

