from itertools import permutations
import enchant
d = enchant.Dict("en_US")
op = set()
lettr = ["G", "H", "E", "M", "A", "O"]

for n in range(2, len(lettr)+1):
  for word in list(permutations(lettr, n)):
    word = "".join(word)
    if d.check(word):
      op.add(word)
op = list(op)
