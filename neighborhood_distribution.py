import math

moore = 0
von_neumann = 0
sqrt2 = math.sqrt(2)
for x in range(0, 100):
    if ((x % sqrt2) < 1):
        moore = moore + 1
        von_neumann = von_neumann + 1
    else:
        von_neumann = von_neumann + 1
print("Moore: ", moore, ", von Neumann: ", von_neumann)
