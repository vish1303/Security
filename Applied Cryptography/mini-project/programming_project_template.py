"""
Kyle Soska
Carnegie Mellon University

18-733 Spring 2016 Programming Assignment
"""

from z3 import *

import sha256_template
import certificates_template


rol = lambda val, r_bits, max_bits: \
            (val << r_bits%max_bits) & (2**max_bits-1) | \
                ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

ror = lambda val, r_bits, max_bits: \
            ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
                (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))
      
def hash_example(x):
    C1 = 0x5D7E0D1F2E0F1F84
    C2 = 0x388D76AEE8CB1500
    C3 = 0xD2E9EE7E83C4285B

    x *= C1
    x = x % 2**64
    x = ror(x, x & 0xF, 64)
    x = x % 2**64
    x = x ^ C2
    x = x % 2**64
    x = rol(x, x & 0xF, 64)
    x = x % 2**64
    x = x + C3
    x = x % 2**64
    
    return x



def hash_example_collisions(output, old_input):
    C1=0x5D7E0D1F2E0F1F84
    C2=0x388D76AEE8CB1500
    C3=0xD2E9EE7E83C4285B

    inp, i1, i2, i3, i4, i5, i6, outp = BitVecs('inp i1 i2 i3 i4 i5 i6 outp', 64)
    s = Solver()
    s.add(i1==inp*C1)
    s.add(i2==RotateRight (i1, i1 & 0xF))
    s.add(i3==i2 ^ C2)
    s.add(i4==RotateLeft(i3, i3 & 0xF))
    s.add(outp==i4 + C3)
    s.add(outp== output)
    s.add(inp != old_input)

    print(s.check())
    m=s.model()
    print (m)

    return m[inp].as_long()

def smt_example():

    #What is a 32 bit number between 5 and 10?
    x, low, high = BitVecs('x, low, high', 32)
    s = Solver()
    s.add(low == 5)
    s.add(high == 10)
    s.add(x < high)
    s.add(x > low)
    
    print (s.check())
    print (s.model())
 

    #It tells us that x = 6,  what if we wanted a solution where x!=6
    x, low, high = BitVecs('x, low, high', 32)
    s = Solver()
    s.add(low == 5)
    s.add(high == 10)
    s.add(x < high)
    s.add(x > low)
    s.add(x != 6)

    print (s.check())
    print (s.model())
 
    #Now it tells us that x = 8



    #Lets see some other stuff that we can do

    x, y, z, lower_bound = BitVecs('x, y, z, lower_bound', 32)
    s = Solver()

    #We can add multiple constraints into the same line
    s.add(x == y*y - z*z)
    #s.add(y > lower_bound)
    #s.add(z > lower_bound)
    s.add(lower_bound == 10)
    s.add(y != z)
    s.add(x == 9)
    s.add(y == 5)

    print (s.check())
    print (s.model())


    #What if we give it an impossible task?
    x, y, z = BitVecs('x, y, z', 32)
    s = Solver()

    s.add(y == 5)
    s.add(z == 10)
    s.add(x < y)
    s.add(x > z)
    
    print (s.check())
    #Unsat means that we can confirm that there does not exist a solution




    #MYSTERY

    #The size of the bitvector is important
    x = BitVecs('x', 32)
    s = Solver()
    
    s.add(x == 256)
    #print (s.check())
    #print s.model()

    x = BitVecs('x', 8)
    s = Solver()

    s.add(x > 256)
    #print (s.check())
    #print (s.model())


    #Some operations that you might want to be able to perform
    x, y, z = BitVecs('x, y, z', 32)
    s = Solver()

    s.add(x == 123) #Setting value equal to a constant
    s.add(x == 0x234) #Setting value equal to a hexadecimal constant
    s.add(x != 123) #Constraining a varaible to not be a particular value
    s.add(x == y) #Setting a varaible equal to another value

    s.add(x > y)
    s.add(x < y)
    s.add(x >= y)
    s.add(x <= y) #Standard inequalities

    s.add(x == x & y) #Logical bitwise AND
    s.add(x == x ^ y) #Logical bitwise XOR
    s.add(x == x | y) #Logical bitwise OR

    s.add(x == RotateRight(y, 10)) #Rotate the bits of y right by 10 with replacement
    s.add(x == RotateLeft(y, 10)) #Rotate the bits of y left by 10 with replacement
    s.add(x == LShR(y, 10)) #Logical Right Shift by 10
    s.add(x == y >> 10) #Arithmetic Right Shift by 10
    s.add(x == y << 10) #Arithmetic Left Shift by 10

    s.add(x == y + z) #Addition
    s.add(x == y - z) #Subtraction
    s.add(x == y * z) #Multiplication


    s = Solver()
    x, y, z = BitVecs('x, y, z', 32)
    s.add(z == 10)
    s.add(x < y)
    s.add(y > z)
    #s.add(z < x < y)
    print s.check()
    print s.model()


def find_sha_256_collision():
    #Needs implementation
    return

def generate_rogue_CA_Cert():
    #Needs implementation
    return



smt_example()

value = hash_example(123456789012345)
print (value)
collision = hash_example_collisions(value, 123456789012345)

print ("Original Input: " + str(123456789012345))
print ("Collision: " + str(collision))

if hash_example(collision) == hash_example(123456789012345):
   print ("A collision has been found!")

certificates_template.testCertificates()
