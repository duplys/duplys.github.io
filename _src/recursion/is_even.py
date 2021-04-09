"""Example for recursion."""

def is_even(n, even):
    """Uses recursion to compute whether the given number n is even.

    To determine whether a positive whole number is even or odd, 
    the following can be used:
    * Zero is even
    * One is odd
    * For any other number n, its evenness is the same as n-2
    """
    if n == 0:
        even = True
    elif n == 1:
        even = False
    else:
        even = is_even(n-2, even)

    return even

for i in range(1,20):
    val = None
    print("[*] Is {0} even? {1}".format(i, is_even(i, val)))