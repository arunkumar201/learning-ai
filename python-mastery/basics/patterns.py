# 1. Print a right-angled triangle pattern with increasing number of stars in each row
#    Visual:
#    *
#    **
#    ***
#    ****
#    *****
def print_right_angled_triangle(n: int):
    for i in range(1, n):
        for j in range(1, i + 1):
            print("*", end="")
        print()


def print_right_angled_triangle_short(n: int):
    for i in range(1, n):
        print("*" * i)


print("Right-angled triangle pattern:")
print_right_angled_triangle(6)
print("------------Short version ------------")
print_right_angled_triangle_short(6)
print("--------------------------------")


# 2. Print an inverted right-angled triangle pattern
#    Visual:
#    *****
#    ****
#    ***
#    **
#    *
def print_inverted_right_angled_triangle(n: int):
    for i in range(0, n + 1):
        for j in range(0, n - i):
            print("*", end="")
        print()


def print_inverted_right_angled_triangle_short(n: int):
    for i in range(0, n + 1):
        print("*" * (n - i))


print_inverted_right_angled_triangle(5)
print("------------Short version ------------")
print_inverted_right_angled_triangle_short(5)


# 3. Print a pyramid pattern with centered stars
#    Visual:
#        *
#       ***
#      *****
#     *******
#    *********
def print_pyramid(rows: int):
    for i in range(0, rows):
        # Print leading spaces
        for j in range(0, rows - i):
            print(" ", end="")
        # Print stars
        for k in range(0, 2 * i + 1):
            print("*", end="")
        print()


def print_pyramid_short(rows: int):
    for i in range(0, rows):
        print(" " * (rows - i) + "*" * (2 * i + 1))


print("------------Pyramid pattern ------------")
print_pyramid(5)
print("------------Short version ------------")
print_pyramid_short(5)
print("--------------------------------")


# 4. Print a diamond pattern
#    Visual:
#        *
#       ***
#      *****
#     *******
#    *********
#     *******
#      *****
#       ***
#        *
def print_diamond_pattern(n: int) -> None:

    # rows for upper half of diamond
    for i in range(n):
        for j in range(n - i - 1):
            print(" ", end="")
        for k in range(2 * i + 1):
            print("*", end="")
        print()

    # rows for lower half of diamond
    for i in range(n - 2, -1, -1):
        for j in range(n - i - 1):
            print(" ", end="")
        for k in range(2 * i + 1):
            print("*", end="")
        print()


print("------------Diamond pattern ------------")
print_diamond_pattern(5)
