![Boolan](Boolan_logo.png)

----------------
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Boolan is a Python package to determine characteristics of Boolean functions. It uses the fact that Boolean functions can be expressed as multilinear polynomials over a two valued field {1, -1}. Transforming the Boolean functions into this polynomial (which is close to a Fourier transform), exposes all kinds of information about the behavior of the function, which can be gleaned from the Fourier coefficients of the polynomial.

## Install
Boolan uses the Sage computer algebra environment to do its rewriting. In order to install and make use of Boolan, one first has to install Sage. The easiest and most foolproof way to do this, on Ubuntu, is via Conda. To avoid conflicts, one should make a new environment where Sage is installed. If you don't have Conda, you can get it [here](https://www.anaconda.com/distribution/).

Add the conda-forge package channel to config
> conda config --add channels conda-forge

Make sure everything is up to date 
> conda update --all

Install Sage in its own Conda enviroment
> conda create -n sage sage

## Features
Boolean functions can be written as polynomials, with -1 coding for True and 1 for False (read that again; the ordering is not a mistake!). The two-input AND function can be expressed like this:
<p align="center">
  <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{1}{2}&space;&plus;&space;\frac{1}{2}x_1&space;&plus;&space;\frac{1}{2}x_2&space;-&space;\frac{1}{2}x_1x_2" target="_blank"><img src="https://latex.codecogs.com/png.latex?\frac{1}{2}&space;&plus;&space;\frac{1}{2}x_1&space;&plus;&space;\frac{1}{2}x_2&space;-&space;\frac{1}{2}x_1x_2" title="\frac{1}{2} + \frac{1}{2}x_1 + \frac{1}{2}x_2 - \frac{1}{2}x_1x_2" /></a>
</p>

The influence of a certain variable on the ouput is another quantity that could be of interest. It is defined as the sum of the squares of all the coefficients of the terms that contain the variable. The total influence of a function is then the sum of the influences of all the input variables of the function.
<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=Influence_i&space;&=&space;\sum_{\{S&space;|&space;i&space;\in&space;S&space;\}}&space;\hat{f}&space;(S)^2" target="_blank"><img src="https://latex.codecogs.com/png.latex?Influence_i&space;&=&space;\sum_{\{S&space;|&space;i&space;\in&space;S&space;\}}&space;\hat{f}&space;(S)^2" title="Influence_i &= \sum_{\{S | i \in S \}} \hat{f} (S)^2" /></a>
  </p>


<a href="https://www.codecogs.com/eqnedit.php?latex=NS_\delta&space;=&space;\frac{1}{2}&space;\sum_{k=0}^N&space;(1&space;-&space;(1&space;-&space;2\delta)^k)&space;W^k[f]" target="_blank"><img src="https://latex.codecogs.com/png.latex?NS_\delta&space;=&space;\frac{1}{2}&space;\sum_{k=0}^N&space;(1&space;-&space;(1&space;-&space;2\delta)^k)&space;W^k[f]" title="NS_\delta = \frac{1}{2} \sum_{k=0}^N (1 - (1 - 2\delta)^k) W^k[f]" /></a>

## Example
The two-input AND function can be analysed in the following way

```python
from boolan.boolan import get_stats

AND = [-1, 1, 1, 1]
features = get_stats(AND)
```

This piece of code will give you the following characteristics of the function:

- Total Influence
- Weights on each order of monomial (3 values in the case of AND)
- Variance
- Noise Sensitivity at noise levels [0.1, 0.2, 0.3, 0.4]
