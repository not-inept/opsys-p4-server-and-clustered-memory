from memory import *

m = Memory()
print m

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


r = m.delete("B")
assert(r == ("B", 1))
print r
print m

r = m.alloc("afafagagag", 100000)
assert(r == ("B", 100000, 25, 2))
print r
print m


print "\n\nTests Passed!"
