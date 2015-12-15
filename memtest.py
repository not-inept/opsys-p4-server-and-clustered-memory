# Mason Cooper (coopem4) & John Drogo (drogoj)
from memory import *

m = Memory()
print m


#Alloc test.
r = m.alloc("asdasd", 128)
assert(r == ("A", 128, 1, 1))
print r
print m

r = m.alloc("adgdsg", 1000)
assert(r == ("B", 1000, 1, 1))
print r
print m

r = m.alloc("sdgs", 10000)
assert(r == ("C", 10000, 3, 1))
print r
print m

r = m.alloc("sdfgsd", 10000000000000000000000000000)
assert(r == (0, 0, 0, 0))
print r
print m



#Delete test.
r = m.deleteFile("adgdsg")
assert(r == ("B", 1))
print r
print m

r = m.alloc("afafagagag", 100000)
assert(r == ("B", 100000, 25, 2))
print r
print m

m.alloc("test", 10)
m.deleteFile("test")
r = m.alloc("test", 20)
print r
print m



#Read test.
r = m.read("test", 0, 1)
print r


r = m.alloc("weird", 10000)
print r

r =  m.read("weird", 4096, 4096)
assert(r == ("E", 4096, 4096, 1))
print r
print m


print m.lookupTable

#r = m.read("adgdsg", 4096, 8192)
r = m.read("afafagagag", 4095, 4097)
assert(r == ("B", 4095, 4097, 2))
print r
print m

r = m.read("afafagagag", 4095, 4098)
print r
assert(r == ("B", 4095, 4098, 3))
print m

r = m.read("afafagagag", 4090, 5000)
assert(r == ("B", 4090, 5000, 3))
print r
print m


#TODO: Check out of bounds errors.
#TODO: CHekc misnamed errors.
#TODO: Reallocation of a files in use.
#TODO: Add errors if asserts are violated.

print "\n\nTests Passed!"
