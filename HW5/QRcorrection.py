"""
QR Code Generator
"""

import comp140_module5 as qrcode
import comp140_module5_z256 as z256

def divide_terms(coefficient1, power1, coefficient2, power2):
    """
    Computes the quotient of two terms.

    The degree of the first term, power1, must be greater than or
    equal to the degree of the second term, power2.

    Inputs:
        - coefficient1: a Z_256 number representing the coefficient of the first polynomial term
        - power1: an integer representing the power of the first term.
        - coefficient2: a Z_256 number representing the coefficient of the second polynomial term
        - power2: an integer representing the power of the second term.

    Returns: an instance of a Polynomial that is the resulting
    term.
    """
    # From recipe: (a*x^b) / (c*x^d) = (a/c) * x^(b-d)
    new_coeff = z256.div(coefficient1, coefficient2)
    new_pow = power1 - power2

    # Represent our answer as a Polynomial
    divided = Polynomial()
    divided = divided.add_term(new_coeff, new_pow)
    return divided

class Polynomial:
    """
    A class used to abstract methods on a polynomial in the finite
    field Z_256 (including numbers from 0 through 255).

    Since 256 is not prime, but is rather of the form p^n = 2^8, this
    representation uses special arithmetic via the z256 module so as to
    preserve multiplicative inverses (division) inside this field.
    """

    def __init__(self, terms=None):
        """
        Creates a new Polynomial object.  If a dictionary of terms is provided,
        they will be the terms of the polynomial,
        otherwise the polynomial will be the 0 polynomial.

        inputs:
            - terms: a dictionary of terms mapping powers to coefficients or None
              (None indicates that all coefficients are 0)
        """
        if terms != None:
            self._terms = dict(terms)
        else:
            self._terms = {}

    def __str__(self):
        """
        Returns: a string representation of the polynomial, containing the
        class name and all of the terms.
        """
        # Create a string of the form "ax^n + bx^n-1 + ... + c" by
        # creating a string representation of each term, and inserting
        # " + " in between each
        term_strings = []

        # Add the highest powers first
        powers = list(self._terms.keys())
        powers.sort(reverse=True)
        for power in powers:
            coefficient = self._terms[power]
            # Don't print out terms with a zero coefficient
            if coefficient != 0:
                # Don't print "x^0"; that just means it's a constant
                if power == 0:
                    term_strings.append("%d" % coefficient)
                else:
                    term_strings.append("%d*x^%d" % (coefficient, power))

        terms_str = " + ".join(term_strings)
        if terms_str == "":
            terms_str = "0"
        return "Polynomial: %s" % terms_str

    def __eq__(self, other_polynomial):
        """
        Check if another polynomial is equvalent

        inputs:
            - other_polynomial: a Polynomial object

        Returns a boolean: True if other_polynomial contains
        the same terms as self, False otherwise.
        """
        # Make sure that other_polynomial is a Polynomial
        if not isinstance(other_polynomial, Polynomial):
            return False

        # Get the terms of the other_polynomial
        terms = other_polynomial.get_terms()

        # Check that all terms in other_polynomial appear in self
        for power, coefficient in terms.items():
            if coefficient != 0:
                if power not in self._terms:
                    return False
                if self._terms[power] != coefficient:
                    return False

        # Check that all terms in self appear in other_polynomial
        for power, coefficient in self._terms.items():
            if coefficient != 0:
                if power not in terms:
                    return False
                if terms[power] != coefficient:
                    return False

        return True

    def __ne__(self, other_polynomial):
        """
        Check if another polynomial is NOT equivalent

        inputs:
            - other_polynomial: a Polynomial object

        Return a boolean: False if other_polynomial contains the same terms
        as self, True otherwise.
        """
        return not self.__eq__(other_polynomial)

    def get_terms(self):
        """
        Returns: a dictionary of terms, mapping powers to coefficients.
        This dictionary is a completely new object and is not a reference
        to any internal structures.
        """
        terms = dict(self._terms)
        return terms

    def get_degree(self):
        """
        Returns: the maximum power over all terms in this polynomial.
        """
        # Since we don't clean zero-coefficient powers out of our dictionary,
        # we need a trickier get_degree function, to take into account that
        # some coefficients could be zero.
        highest_power = 0
        for power in self._terms:
            if (power > highest_power) and (self._terms[power] != 0):
                highest_power = power

        return highest_power


    def get_coefficient(self, power):
        """
        Determines the coefficient of x^(power) in this polynomial.
        If there is no coefficient of x^(power), this method
        returns 0.

        inputs:
            - power: an integer representing a polynomial power

        Returns: a Z_256 number that is the coefficient or 0 if there
                 is no term of the given power
        """
        if power in self._terms:
            return self._terms[power]
        else:
            return 0

    def add_term(self, coefficient, power):
        """
        Add one term to this polynomial.

        inputs:
            - coefficient: a Z_256 number representing the coefficient of the term
            - power: an integer representing the power of the term

        Returns: a new Polynomial that is the sum of adding this polynomial
        to (coefficient) * x^(power) using Z_256 arithmetic to add
        coefficients, if necessary.
        """

        # Create a dictionary 
        dic = self.get_terms()

        # Check if term-to-add is already in the self
        if power in dic:
            # if so add term-to-add's constant term with the constant in Z_256
            dic[power] = z256.add(dic[power], coefficient)
        else:
            # if not then push this into the Z_256
            dic[power] = coefficient

        # return by creating a new polynomial
        return Polynomial(dic)

    def subtract_term(self, coefficient, power):
        """
        Subtract one term from this polynomial.

        inputs:
            - coefficient: a Z_256 number representing the coefficient of the term
            - power: an integer representing the power of the term

        Returns: a new Polynomial that is the difference of this polynomial
        and (coefficient) * x^(power) using Z_256 arithmetic to subtract
        coefficients, if necessary.
        """
        # essential substract a term from given polynomial is the same as
        # adding the opposite of the term
        # the coefficient ought to be the opposite of the orginial term
        return self.add_term(z256.sub(0, coefficient), power)

    def multiply_by_term(self, coefficient, power):
        """
        Multiply this polynomial by one term.

        inputs:
            - coefficient: a Z_256 number representing the coefficient of the term
            - power: an integer representing the power of the term

        Returns: a new Polynomial that is the product of multiplying
        this polynomial by (coefficient) * x^(power).
        """
        
        # Create a disctionary for later construction of Polynomial
        dic = dict() 

        # parse over the self_terms and compute the power and coefficient
        for pro in self._terms:
            # the new power is equal to 
            key = pro + power
            # the new coefficient is equal to
            value = z256.mul(coefficient, self._terms[pro])
            # update the dic
            dic[key] = value

        return Polynomial(dic)

    def add_polynomial(self, other_polynomial):
        """
        Compute the sum of the current polynomial other_polynomial.

        inputs:
            - other_polynomial: a Polynomial object

        Returns: a new Polynomial that is the sum of both polynomials.
        """

        # Create a polynomial for later return
        pol = Polynomial(self._terms)

        # parse over other_polynomial and decompose it into single Polynomials and add one at a time
        for pwr, coe in other_polynomial.get_terms().items():
            # add single polynomial to the pl
            pol = pol.add_term(coe, pwr)

        return pol

    def subtract_polynomial(self, other_polynomial):
        """
        Compute the difference of the current polynomial and other_polynomial.

        inputs:
            - other_polynomial: a Polynomial object

        Returns: a new Polynomial that is the difference of both polynomials.
        """
        
        # Create a polynomial for later return
        ply = Polynomial(self._terms)

        # parse over other_polynomial and decompose it into single Polynomials
        for pwr, coe in other_polynomial.get_terms().items():
            # substract single polynomial from the pl
            ply = ply.subtract_term(coe, pwr)

        return ply

    def multiply_by_polynomial(self, other_polynomial):
        """
        Compute the product of the current polynomial and other_polynomial.

        inputs:
            - other_polynomial: a Polynomial object

        Returns: a new Polynomial that is the product of both polynomials.
        """

        # initialze an empty Polynomial for later return
        ply = Polynomial()

        # parse over one polynomial and decompose it into single polynomial
        for pwr, coe in other_polynomial.get_terms().items():
            # decompose into single polynomial and multiply
            # save the product result into prop
            prop = self.multiply_by_term(coe, pwr)
            # add the prop into ply
            ply = ply.add_polynomial(prop)

        return ply


    def remainder(self, denominator):
        """
        Compute a new Polynomial that is the remainder after dividing this
        polynomial by denominator.

        Note: does *not* return the quotient; only the remainder!

        inputs:
            - denominator: a Polynomial object

        Returns: a new polynomial that is the remainder
        """
        # if the denominator is a constant, the remainder is 0
        if denominator.get_degree() == 0:
            return Polynomial()

        # make a copy of the self polynomial
        rmd = Polynomial(self._terms)

        # as long as the remainder's degree is not lower than that of the denominator
        while rmd.get_degree() >= denominator.get_degree():
            # obtain the highest constant coefficient term for both rm and denominator
            crm = rmd.get_coefficient(rmd.get_degree())
            cde = denominator.get_coefficient(denominator.get_degree())
            # find the product power
            pro = rmd.get_degree() - denominator.get_degree()
            # find the product coeff
            coe = z256.div(crm, cde)
            # form the polynomial with po as power and co as constant
            # multiply npl to denominator to get the resulting product
            npl = denominator.multiply_by_term(coe, pro)
            # update rm to be rm minus the resulting product
            rmd = rmd.subtract_polynomial(npl)
        
        return rmd

def create_message_polynomial(message, num_correction_bytes):
    """
    Creates the appropriate Polynomial to represent the
    given message. Relies on the number of error correction
    bytes (k). The message polynomial is of the form
    message[i]*x^(n+k-i-1) for each number/byte in the message.

    Inputs:
        - message: a list of integers (each between 0-255) representing data
        - num_correction_bytes: an integer representing the number of
          error correction bytes to use

    Returns: a Polynomial with the appropriate terms to represent the
    message with the specified level of error correction.
    """
    # create an empty polynomial for later return
    ply = Polynomial()

    # parse over the message by index
    for idx in range(len(message)):
        # compute the power
        pwr = num_correction_bytes + len(message) - idx - 1
       
        # form a new polynomial
        nply = Polynomial({pwr:message[idx]})

        # add the new polynomial to the ply
        ply = ply.add_polynomial(nply)

    return ply

def create_generator_polynomial(num_correction_bytes):
    """
    Generates a static generator Polynomial for error
    correction, which is the product of (x-2^i) for all i in the
    set {0, 1, ..., num_correction_bytes - 1}.

    Inputs:
        - num_correction_bytes: desired number of error correction bytes.
                                In the formula, this is represented as k.

    Returns: generator Polynomial for generating Reed-Solomon encoding data.
    """

    # create a 1 polynomial for later return
    ply = Polynomial({0:1})

    # parse over the message by index
    for idx in range(num_correction_bytes):
        # compute the second term
        sdt = Polynomial({0:z256.power(2, idx)})

        # compute the first term
        ftm = Polynomial({1:1})
        
        # form a new polynomial
        nply = ftm.add_polynomial(sdt)

        # multiply the new polynomial to the ply
        ply = ply.multiply_by_polynomial(nply)

    return ply

def reed_solomon_correction(encoded_data, num_correction_bytes):
    """
    Corrects the encoded data using Reed-Solomon error correction

    Inputs:
        - encoded_data: a list of integers (each between 0-255)
                        representing an encoded QR message.
        - num_correction_bytes: desired number of error correction bytes.

    Returns: a polynomial that represents the Reed-Solomon error
    correction code for the input data.
    """
    # get the message polynomial
    msp = create_message_polynomial(encoded_data, num_correction_bytes)

    # get the generator polynomial
    gnp = create_generator_polynomial(num_correction_bytes)

    # return the remainder 
    return msp.remainder(gnp)


# Uncomment the following line when you are ready to generate an
# actual QR code.  To do so, you must enter a short message in the
# "info" text box and hit return (be sure to hit return!).  You then
# must push the "Generate!" button.  This will generate a QR code for
# you to view - try scanning it with your phone!  If you would like to
# save your QR codes, you can use the "Image in a New Window" button
# to create a .png file that you can save by right clicking in your
# browser window.

qrcode.start(reed_solomon_correction)
