# AND function calculation between an odd number of XOR masked data shares
# for every i this algorithm calculates:
# Ci = [XOR(k!=i: Ak) AND XOR(j!=i: Bj)] XOR (Ai AND Bi)

# The generic parameters enable arbitrary wide words to be AND-ed which consist of arbitrary odd
# number masked shares. The algorithm does not work with an even number of shares due to its math
# properties!

def masked_AND_rolled_out(am, bm):
    #any non-zero offset creates non-completeness, can even be random
    offset = 1
    #calculate AND between masked values
    cm = [am[i] & bm[i] for i in range(r)]
    #calculating correction terms
    for i in range(r):
        summa = 0
        #calculating no parities between all but 1 Ak and Bj bits which could cause unmasking
        for j in range(r):
            if i==j:
                continue
            summa ^= am[i] & bm[j]
        #addig correction term to the particular output share
        #which is the "AND" between the parities
        cm[i-offset] ^= summa
    return cm

# BEGIN TESTING

a = 0x76857f6f
b = 0x5432f1f2
print("A:      ", hex(a))
print("B:      ", hex(b))
print("AND:    ", hex(a & b))

# preparing odd pieces of random numbers for masking
# the algorithm doesn't work with an even number of shares!

r = 7 #6 #uncomment to test even number of shares

ra =[0x67978544,
     0xa6f328ab,
     0x68979586,
     0xa76ef4bc,
     0xc9876d3e, # comment to test even number of shares
     0xa7656b36] 

rb =[0x6abdc744,
     0x895728ab,
     0xfe45c8d6,
     0xc9876d3e,
     0xe346a867, # comment to test even number of shares
     0x86f675ed] 

# the sum of the masks has to be zero at first...*1
rasum = 0
for ma in ra:
    rasum ^= ma
ra.append(rasum)
rbsum = 0
for mb in rb:
    rbsum ^= mb
rb.append(rbsum)

# *1...so that adding a and b to any arbitrary random number yields valid shares
am = ra
am[2] ^= a #index is arbitrary
bm = rb
bm[r-2] ^= b #index is arbitrary

# test vectors for VHDL code
#for s in am:
#    print(hex(s))# test vectors for VHDL code
#for s in bm:
#    print(hex(s))

# double checking the sum of shares
a = 0
b = 0
for i in range(r):
    a ^= am[i]
    b ^= bm[i]
print("A sum:  ", hex(a))
print("B sum:  ", hex(b))

# AND calculation between masked shares
cm = masked_AND_rolled_out(am, bm)

# test vectors for VHDL code
#for s in cm:
#    print(hex(s))

#summing up the result shares
c = 0
for k in range(len(cm)):
    c ^= cm[k]
print("Result: ", hex(c))
print("Correct: ", c == a&b)