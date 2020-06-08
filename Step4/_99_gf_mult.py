#!/usr/bin/python3
#
# Author: Joao H de A Franco (jhafranco@acm.org)
#
# Description: Binary finite field multiplication in Python 3
#
# Date: 2012-02-16
#
# License: Attribution-NonCommercial-ShareAlike 3.0 Unported
#          (CC BY-NC-SA 3.0)
#===========================================================
from functools import reduce
import time

# constants used in the multGF2 function
mask1 = mask2 = polyred = None
 
def setGF2(degree, irPoly):
    """Define parameters of binary finite field GF(2^m)/g(x)
       - degree: extension degree of binary field
       - irPoly: coefficients of irreducible polynomial g(x)
    """
    global mask1, mask2, polyred
    mask1 = mask2 = 1 << degree
    mask2 -= 1
    if sum(irPoly) <= len(irPoly):
        polyred = reduce(lambda x, y: (x << 1) + y, irPoly[1:])    
    else:
        polyred = poly2Int(irPoly[1:]) 
         
def multGF2(p1, p2):
    """Multiply two polynomials in GF(2^m)/g(x)"""
    p = 0
    while p2:
        if p2 & 1:
            p ^= p1
        p1 <<= 1
        if p1 & mask1:
            p1 ^= polyred
        p2 >>= 1
    return p & mask2
 
#=============================================================================
#                        Auxiliary formatting functions
#=============================================================================
def int2Poly(bInt):
    """Convert a "big" integer into a "high-degree" polynomial"""
    exp = 0
    poly = []
    while bInt:
        if bInt & 1:
            poly.append(exp)
        exp += 1
        bInt >>= 1
    return poly[::-1]
 
def poly2Int(hdPoly):
    """Convert a "high-degree" polynomial into a "big" integer"""
    bigInt = 0
    for exp in hdPoly:
        bigInt += 1 << exp
    return bigInt
 
def i2P(sInt):
    """Convert a "small" integer into a "low-degree" polynomial"""
    return [(sInt >> i) & 1 for i in reversed(range(sInt.bit_length()))]
 
def p2I(ldPoly):
    """Convert a "low-degree" polynomial into a "small" integer"""
    return reduce(lambda x, y: (x << 1) + y, ldPoly)
 
def ldMultGF2(p1, p2):
    """Multiply two "low-degree" polynomials in GF(2^n)/g(x)"""
    return multGF2(p2I(p1), p2I(p2))
 
def hdMultGF2(p1, p2):
    """Multiply two "high-degree" polynomials in GF(2^n)/g(x)"""
    return multGF2(poly2Int(p1), poly2Int(p2))
 
"""
if __name__ == "__main__":

  
    # Define binary field GF(2^571)/x^64 + /x^64 + x^4 + x^3 + x + 1
    #setGF2(64, [64,4,3,1,0])
    setGF2(64, [64,11,2,1,0])

    
    a = 0x380306da784ef0f2
    b = 0xefdd1b4292d2fc79

    res = hdMultGF2(int2Poly(a), int2Poly(b))
    #print("r %x" % res)
    
    #print ((time.clock() - start_clock)*1000, "ms - CPU time")
    #print ((time.time() - start_time)*1000, "ms - total time")
   

#invert b, or compute b^(2^64-2) [n]
a = 0xefdd1b4292d2fc79
k = 2**64-2
#n: set to polynomial x^64 + x^11 + x^2 + x + 1
print("Inverting %x" % a)

#compute a^k [n]
p = 1
while (k>0):
    if (k %2 != 0):
        p = hdMultGF2(int2Poly(p), int2Poly(a))
    
    a = hdMultGF2(int2Poly(a), int2Poly(a))
    k = k//2

print("result: %x" % p)
print("")
print("checking: a * p")
res = hdMultGF2(int2Poly(a), int2Poly(p))
print("res: %x" % res)


print("*"*40)
print("")
a = 0x380306da784ef0f2
constant = 0xefdd1b4292d2fc79
print("a        %08x" % a)
print("constant %08x" % constant)
# Calculate the product of two polynomials in GF(2^64)/x^63 + x^2 + x + 1 * x^5 + x^3
#print(int2Poly(hdMultGF2([63,2,1,0], [5,3])))
res = hdMultGF2(int2Poly(a), int2Poly(constant))
print("result   %08x" % res)

print("\n\nInverting...")
constant_inv = 0x247f9823bebea5a8
print("res      %08x" % res)
print("cst_inv  %08x" % constant_inv)
res2 = hdMultGF2(int2Poly(res), int2Poly(constant_inv))
print("result   %08x" % res2)
"""