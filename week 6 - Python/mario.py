from cs50 import get_int

while True:
    height = get_int("Height: \n")
    if height > 0 and height < 9:
        break

for stair in range(1, height+1):
    print("{0}{1}{2}{1}".format((height - stair) * " ", stair * "#", "  "))
