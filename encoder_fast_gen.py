#!/usr/bin/env python3

import encode 
import numpy


def gen_matmul(in_name, out_name, A):
    result = ""
    for i in range(0, A.shape[0]):
        tmp = []
        for j in range(0, A.shape[1]):
            if A[i, j] == 1:
                tmp.append(in_name + "(" + str(A.shape[1] - j - 1) + ")")
        if len(tmp) == 0:
            line = "'0'"
        else:
            line = " XOR ".join(tmp)
        line = "    " + out_name + "(" + str(A.shape[0] - i - 1) + ") <= " + line + ";\n"
        result += line
    return result

def gen_backsub(in_name, out_name, T):
    result = ""
    for i in range(0, T.shape[0]):
        tmp = []
        tmp.append(in_name + "(" + str(T.shape[0] - i - 1) + ")")
        for j in range(0, i - 1):
            if T[i, j] == 1:
                tmp.append(out_name + "(" + str(T.shape[1] - j - 1) + ")")
        if len(tmp) == 0:
            print("WTF?")
        else:
            line = " XOR ".join(tmp)
        line = "    " + out_name + "(" + str(T.shape[0] - i - 1) + ") <= " + line + ";\n"
        result += line
    return result

def gen_signal(name, size):
    return "    signal " + name + " : std_logic_vector(" + str(size) + "-1 downto 0);\n"
"""
Hqc = numpy.array([
    [57, -1, -1, -1, 50, -1, 11, -1, 50, -1, 79, -1, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, -1, 28, -1, 0, -1, -1, -1, 55, 7, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [30, -1, -1, -1, 24, 37, -1, -1, 56, 14, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1],
    [62, 53, -1, -1, 53, -1, -1, 3, 35, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1, -1, -1],
    [40, -1, -1, 20, 66, -1, -1, 22, 28, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1, -1],
    [0, -1, -1, -1, 8, -1, 42, -1, 50, -1, -1, 8, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1],
    [69, 79, 79, -1, -1, -1, 56, -1, 52, -1, -1, -1, 0, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1],
    [65, -1, -1, -1, 38, 57, -1, -1, 72, -1, 27, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1],
    [64, -1, -1, -1, 14, 52, -1, -1, 30, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1],
    [-1, 45, -1, 70, 0, -1, -1, -1, 77, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1],
    [2, 56, -1, 57, 35, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0],
    [24, -1, 61, -1, 60, -1, -1, 27, 51, -1, -1, 16, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0]])
"""

Hqc = numpy.array([
    [ 0, -1, -1, -1,  0,  0, -1, -1,  0, -1, -1,  0,  1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [22,  0, -1, -1, 17, -1,  0,  0, 12, -1, -1, -1, -1,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [ 6, -1,  0, -1, 10, -1, -1, -1, 24, -1,  0, -1, -1, -1,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1],
    [ 2, -1, -1,  0, 20, -1, -1, -1, 25,  0, -1, -1, -1, -1, -1,  0,  0, -1, -1, -1, -1, -1, -1, -1],
    [23, -1, -1, -1,  3, -1, -1, -1,  0, -1,  9, 11, -1, -1, -1, -1,  0,  0, -1, -1, -1, -1, -1, -1],
    [24, -1, 23,  1, 17, -1,  3, -1, 10, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0, -1, -1, -1, -1, -1],
    [25, -1, -1, -1,  8, -1, -1, -1,  7, 18, -1, -1,  0, -1, -1, -1, -1, -1,  0,  0, -1, -1, -1, -1],
    [13, 24, -1, -1,  0, -1,  8, -1,  6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0, -1, -1, -1],
    [ 7, 20, -1, 16, 22, 10, -1, -1, 23, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0, -1, -1],
    [11, -1, -1, -1, 19, -1, -1, -1, 13, -1,  3, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0, -1],
    [25, -1,  8, -1, 23, 18, -1, 14,  9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0],
    [ 3, -1, -1, -1, 16, -1, -1,  2, 25,  5, -1, -1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0]])

block_length = 27

block_vector = numpy.zeros(block_length, dtype=Hqc.dtype)
block_vector[0] = 1
H = encode.qc_to_pcm(Hqc, block_vector)
tmp = (H, block_length)
print("returned\n", tmp)
pre = encode.encode_precompute(tmp[0], tmp[1])

in_width = H.shape[1] - H.shape[0]
out_width = H.shape[1]
header = """
-------------------------------------------
--  THIS FILE IS AUTOMATICALLY GENERATED --
--  ALL CHANGES WILL BE OVERWRITTEN      --
-------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use IEEE.math_real.all;

entity encoder is 
    port (clock : in std_logic;
        bits_in : in std_logic_vector(""" + str(in_width) + """-1 downto 0);
        bits_out : out std_logic_vector(""" + str(out_width) + """-1 downto 0)
    );
end entity;

architecture fast of encoder is
"""

footer = "end architecture;"

out_file = open("vhdl/autogen/encoder_fast.vhd", "w")

out_file.write(header)

# all the required signals for encoding

out_file.write(gen_signal("As", pre["A"].shape[0]))
out_file.write(gen_signal("TAs", pre["T"].shape[0]))
out_file.write(gen_signal("ETAs", pre["E"].shape[0]))
out_file.write(gen_signal("Cs", pre["C"].shape[0]))
out_file.write(gen_signal("ETAsCs", pre["C"].shape[0]))
out_file.write(gen_signal("p1", pre["thetainv"].shape[0]))

out_file.write(gen_signal("Bp1", pre["B"].shape[0]))
out_file.write(gen_signal("AsBp1", pre["B"].shape[0]))
out_file.write(gen_signal("p2", pre["T"].shape[0]))

out_file.write("begin\n")
print(out_width)
print(in_width)


footer = "end architecture;\n"


out_file.write(gen_matmul("bits_in", "As", pre["A"]))
out_file.write(gen_backsub("As", "TAs", pre["T"]))
out_file.write(gen_matmul("TAs", "ETAs", -pre["E"] % 2))
out_file.write(gen_matmul("bits_in", "Cs", pre["C"]))
out_file.write("    ETAsCs <= ETAs XOR Cs;\n")
out_file.write(gen_matmul("ETAsCs", "p1", pre["thetainv"]))

out_file.write(gen_matmul("p1", "Bp1", pre["B"]))
out_file.write("    AsBp1 <= As XOR Bp1;\n")
out_file.write(gen_backsub("AsBp1", "p2", - pre["T"] % 2))

out_file.write("    bits_out <= bits_in & p1 & p2;\n")


header = """library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use IEEE.math_real.all;

entity encoder is 
    port (clock : in std_logic;
        bits_in : in std_logic_vector(""" + str(in_width) + """-1 downto 0);
        bits_out : out std_logic_vector(""" + str(out_width) + """-1 downto 0)
    );
end entity;

"""

out_file.write(footer)

out_file.close()
