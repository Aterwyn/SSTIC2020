
global stack
#stack = [0]*0x1200

#[ebp-z,  ebp-y, ... ebp-1] ebp
global const
global eax, ebx, ecx, edx, esi, edi

"""
#do this once
f = open("13_bytecode_const.bin","rb")
const = f.read()
f.close()
f = open("99_bytecode_const.bin","wb")
f.write(const[0x5F1F:0x5F1F+0x400])
f.close()
#raise Exception
"""

f = open("99_bytecode_const.bin","rb")
const = f.read()
f.close()


def const_get(offset, getter_type=4):
    global const
    assert getter_type in [4]
    assert offset >= 0 and offset <= len(const)
    val = const[offset]
    val += const[offset+1] << 8
    val += const[offset+2] << 16
    val += const[offset+3] << 24
    return val

def stack_get(offset, getter_type=4):
    #dword ptr [ebp+var_F8] => stack_get(4, 0xF8)
    #returns int(stack[-F5] stack[-F6], stack[-F7], stack[-F8])
    global stack
    val = 0
    assert offset <= len(stack) and offset > 0
    assert getter_type in [1,2,4]

    if getter_type >= 1:
        val = stack[-offset]
    if getter_type >= 2:
        val += stack[-offset+1] << 8
    if getter_type == 4:
        val += stack[-offset+2] << 16
        val += stack[-offset+3] << 24

    return val

def stack_get2(offset, getter_type=4):
    #dword ptr [ebp+var_F8] => stack_get(4, 0xF8)
    #returns int(stack[-F5] stack[-F6], stack[-F7], stack[-F8])
    global stack
    val = 0
    assert offset < len(stack) and offset >= 0
    assert getter_type in [1,2,4]

    if getter_type >= 1:
        val = stack[offset]
    if getter_type >= 2:
        val += stack[offset+1] << 8
    if getter_type == 4:
        val += stack[offset+2] << 16
        val += stack[offset+3] << 24

    return val

def stack_set(offset, val, setter_type=4):
    global stack
    assert offset <= len(stack) and offset > 0
    assert setter_type in [1,2,4]

    if setter_type >= 1:
        stack[-offset] = val & 0xFF
    if setter_type >= 2:
        stack[-offset+1] = (val >> 8) & 0xFF
    if setter_type >= 4:
        stack[-offset+2] = (val >> 16) & 0xFF
        stack[-offset+3] = (val >> 24) & 0xFF

def stack_set2(offset, val, setter_type=4):
    global stack
    assert offset < len(stack) and offset >=0
    assert setter_type in [1,2,4]

    if setter_type >= 1:
        stack[offset] = val & 0xFF
    if setter_type >= 2:
        stack[offset+1] = (val >> 8) & 0xFF
    if setter_type >= 4:
        stack[offset+2] = (val >> 16) & 0xFF
        stack[offset+3] = (val >> 24) & 0xFF

def print_stack(number_of_lines, starting_line=0):
    global stack
    intro_line = " "*8
    intro_line += " ".join(["%02x" % i for i in range(1,17,1)][::-1])
    print(intro_line)
    print("[ebp-X]")


    for i in range(number_of_lines-1,starting_line-1,-1):
        line = ""
        line = "%04x" % (i*16) + "\t"
        if i == 0:
            line += " ".join(["%02x" % i for i in stack[-16*(i+1):]])
        else:
            line += " ".join(["%02x" % i for i in stack[-16*(i+1):-16*i]])
        print(line)


def shl(reg, shift):
    #return (reg << shift) & 0xFFFFFFFF
    #fix
    shft = shift%32
    return (reg << shft) & 0xFFFFFFFF


def shr(reg, shift):
    #return (reg >> shift) & 0xFFFFFFFF
    #fix
    shft = shift%32
    return (reg >> shft) & 0xFFFFFFFF

def rol(reg, rotate):
    #return shl(reg, rotate) + shr(reg, 32-rotate)
    #fix
    rot = rotate%32
    return shl(reg, rot) + shr(reg, 32-rot)
    
def ror(reg, rotate):
    #return shr(reg, rotate) + shl(reg, 32-rotate)
    #fix
    rot = rotate%32
    return shr(reg, rot) + shl(reg, 32-rot)

def lea(val):
    return val & 0xFFFFFFFF

def add(a, b):
    return (a+b) & 0xFFFFFFFF

def shld(dst, src, count):
    
    if count == 0:
        return dst

    if (count % 32) != 0:
        val = (dst << (count%32) ) & 0xFFFFFFFF
        val |= (src >> ((32-count) % 32)) & 0xFFFFFFFF
    else:
        val = 0
    
    return val


#non-invertible
def f1(val):
    a = const_get((val & 0xFF)*4)
    b = shl(a, 8)
    c = lea(b + val)
    d = rol(c, 0x0B)
    e = lea(d + 0xB7E15162) & 0xFF
    f = const_get(e*4)
    g = shl(f, 8)
    h = lea(g + d + 0xB7E15162)
    return h

###########################################

def check_state():
    global stack, const
    global eax, ebx, ecx, edx, esi, edi

    print("-"*20)
    print("eax: %08X" % eax)
    print("ecx: %08X" % ecx)
    print("edx: %08X" % edx)
    print("ebx: %08X" % ebx)
    print("esp")
    print("ebp")
    print("esi: %08X" % esi)
    print("edi: %08X" % edi)
    print("-"*20)


const_x64 = 0x9fa34d35
const_x7C = 0x4f8ab6d5
const_x58 = 0xfa92a2c9
const_x78 = 0x2abb5929

const_x80 = 0xd706a831
const_x4C = 0x621ebc2d
const_x40 = 0x072f53d1
const_x5C = 0xb23747cd

const_x74 = 0xaec563f3
const_x30 = 0x92d2fc79
const_x50 = 0xbae9857a
const_x28 = 0xefdd1b42

#init other registers
esi = 0
edi = 0

f = open("encrypted_file.bin","rb")
r_initial = f.read()
f.close()

#r_full = r_initial[:-(len(r_initial)%0x1000)]
r_full = r_initial[:]
#print("%x" % len(r_full))


import _99_gf_mult as gf
import binascii


file_length = len(r_initial)
stack = [0]*file_length

for i in range(file_length):
    stack_set2(i, r_initial[i], 1)

gf.setGF2(64, [64, 11, 2, 1, 0])
#gf_const = 0xefdd1b4292d2fc79
gf_const_inv = 0x247f9823bebea5a8

for i in range(file_length-8, -8, -8):
    if i != 0:
        edi = stack_get2(i-8)
        esi = stack_get2(i-4)
    else:
        esi, edi = 0, 0
    
    edi_new = stack_get2(i)
    esi_new = stack_get2(i+4)

    Y = esi_new ^ f1(edi_new ^ const_x5C)
    X = edi_new ^ f1(Y ^ const_x4C)
    esi_old = Y ^ f1(X ^ const_x80)
    edi_old = X ^ f1(esi_old ^ const_x40)

    Z2 = edi_old
    Z1 = esi_old

    R = (Z2 << 32) | Z1
    #print("output:  %016x" % R)
    Q = gf_const_inv
    #perform multiplication with constant inverse
    P = gf.hdMultGF2(gf.int2Poly(R), gf.int2Poly(Q))
    #print("input:   %016x" % P)

    Z1 = P & 0xFFFFFFFF
    Z2 = P >> 32
    
    X2 = Z2 ^ const_x50
    X1 = Z1 ^ const_x74

    Y = X2 ^ f1(X1 ^ const_x78)
    X = X1 ^ f1(Y ^ const_x58)
    edi_old = Y ^ f1(X ^ const_x7C)
    esi_old = X ^ f1(edi_old ^ const_x64)

    bytes_0_3 = esi_old ^ esi
    bytes_4_7 = edi_old ^ edi

    stack_set2(i+4, bytes_0_3)
    stack_set2(i, bytes_4_7)


w = ""
for i in stack:
    w += "%02x" % i

f = open("output_00.raw","ab")
f.write(binascii.unhexlify(w))
f.close()    