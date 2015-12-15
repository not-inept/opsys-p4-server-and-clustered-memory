from memory import Memory

m = Memory()

r = m.alloc("xyz", 14)
print r
print m

r = m.alloc("abc", 12)
print r
print m




r = m.read("xyz", 4, 5)
print r
print m

r = m.deleteFile("xyz")
print r
print m

r = m.deleteFile("abc")
print r
print m
