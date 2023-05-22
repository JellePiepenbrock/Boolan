from sage.all import *
import numpy as np
import itertools
import string
import random


def tt_fourier(num, nb):
    """

    Args:
        num: number coding for the Boolean function
        nb: total bits in encoding (padding)

    Returns:

        list of outputs in the {1, -1} set
    """

    ll = []
    for digit in np.binary_repr(num, width=nb):
        if int(digit) == 1:
            ll.append(-1)
        if int(digit) == 0:
            ll.append(1)

    return ll


def tt_fourier_bitcode(bitcode):

    """

    Args:
        bitcode: binary encoding of function (rows of the truth table from 000 tot 111)

    Returns:
        list of outputs in the {1, -1} set

    """

    ll = []
    for digit in bitcode:
        if int(digit) == 1:
            ll.append(-1)
        if int(digit) == 0:
            ll.append(1)

    return ll


def get_fpolynomial(outputs, no_inputs):

    """

    Args:
        outputs: the outputs for each row of the truth table of the boolean function
        no_inputs: number of variables as inputs for the function

    Returns:
        a Sage polynomial object
    """

    alphabet = string.ascii_lowercase
    varnames = alphabet[:no_inputs]

    R = PolynomialRing(QQ, no_inputs, varnames)

    basis = [[-1, 1] for k in range(no_inputs)]
    print(basis)
    strvar = ""

    for e, i in enumerate(itertools.product(*basis)):
        print(i)
        ziplist = [
            x
            for x in itertools.chain.from_iterable(itertools.zip_longest(i, varnames))
            if x
        ]
        ziplist.append(outputs[e])

        kal = ["((1 + {}*{})/2)" for k in range(no_inputs)] + ["{}"]
        kalstring = "*".join(kal).format(*ziplist)

        if strvar != "":
            kalstring = "+" + kalstring

        strvar += kalstring

    return R(strvar)


def get_influence_variable_order(order, ind, num_vars, pol):

    """

    Args:
        order: which terms of the polynomial should be included (order 0 -> constant term)
        ind: which variable (indexed from 0) we are concerned with
        num_vars: total number of variables
        pol: a Sage polynomial object

    Returns:

        the summed influenced of a variable over terms of a certain order
    """

    inf = 0
    varnames = string.ascii_lowercase[:num_vars]
    R = PolynomialRing(QQ, num_vars, varnames)
    main = varnames[ind]
    rest = [k for k in list(varnames) if not k == main]

    combos = list(itertools.product(main, itertools.combinations(rest, r=order)))

    for mainvar, other in combos:
        inf += np.square(
            pol.monomial_coefficient(
                R(("{}" + len(other) * "*{}").format(mainvar, *other))
            )
        )

    return inf


def get_influence_variable(ind, num_vars, pol):

    """

    Args:
        ind: which variable
        num_vars: total number of variables
        pol: a Sage polynomial object

    Returns:

        the summed influence of a variable over the entire function

    """
    inf = 0
    for order in range(0, 1 + num_vars):
        inf += get_influence_variable_order(order, ind, num_vars, pol)

    return inf


def get_total_influence(pol, num_vars):
    """

    Args:
        pol: a Sage polynomial object
        num_vars: number of variables

    Returns:

        The total influence of the Boolean function

    """
    inf = 0

    for var in range(num_vars):
        inf += get_influence_variable(var, num_vars, pol)

    return inf


def get_weight_order(pol, num_vars, order):
    """

    Args:
        pol: a Sage polynomial object
        num_vars: number of variables
        order: the order of weights that is desired (i.e. 0 for constant term weight)

    Returns:

    """
    varnames = string.ascii_lowercase[:num_vars]

    R = PolynomialRing(QQ, num_vars, varnames)
    vars = [k for k in varnames]
    terms = list(itertools.combinations(vars, order))

    if order is not 0:
        sum_w = 0
        for term in terms:
            term_filled = ("{}" + (len(term) - 1) * "*{}").format(*term)
            sum_w += np.square(pol.monomial_coefficient(R(term_filled)))

        return sum_w

    else:
        return np.square(pol.monomial_coefficient(R(1)))


def get_noise_stability(pol, num_vars, noiselevel):

    """
    Get the noise stability of the function at a certain level of noise
    Args:
        pol: a Sage polynomial object
        num_vars: the number of variables
        noiselevel: the level of noise

    Returns:

        [Int] The noise stability of the function

    """

    ns = 0
    for degree in range(num_vars + 1):
        W = get_weight_order(pol, num_vars, degree)
        ns += (1 - (1 - 2 * noiselevel) ** degree) * W

    return 0.5 * ns


def get_variance(pol, num_vars):

    """
    Get the variance of the function. (Weight not on the constant term)

    Args:
        pol: a Sage polynomial object
        num_vars: the number of variables

    Returns:

        Variance

    """
    var = 0
    for degree in range(1, num_vars + 1):
        var += get_weight_order(pol, num_vars, degree)

    return var


def get_function_characteristics(bitcode):

    """
    This function collects the various statistics
    Args:
        bitcode: the bit code of a certain polynomial:

        Example: the AND function should have as bitcode "[0, 0, 0, 1]"


    Returns:

    """

    num_vars = int(np.log2(len(bitcode)))
    features = []
    pol = get_fpolynomial(bitcode, num_vars)

    total_inf = get_total_influence(pol, num_vars)
    features.append(total_inf)
    for i in range(num_vars + 1):
        features.append(get_weight_order(pol, num_vars, i))

    features.append(get_variance(pol, num_vars))
    for nl in [0.1, 0.2, 0.3, 0.4]:
        features.append(get_noise_stability(pol, num_vars, nl))

    return features


def test_linearity(pol, no_inputs, samples=10):

    linearcount = 0.0
    for i in range(samples):
        x = [random.choice([-1, 1]) for k in range(no_inputs)]
        y = [random.choice([-1, 1]) for k in range(no_inputs)]

        xy = [k * l for k, l in zip(x, y)]
        if pol(*x) * pol(*y) == pol(*xy):
            linearcount += 1

    return linearcount / samples
