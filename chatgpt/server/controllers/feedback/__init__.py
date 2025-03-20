# -*- coding: utf-8 -*-

import sys

def main():
    # Read the number of test cases
    t = int(sys.stdin.readline())
    
    # Iterate through the test cases
    for _ in range(t):
        # Read the input values for each test case
        n, k = map(int, sys.stdin.readline().split())
        a = list(map(int, sys.stdin.readline().split()))
        
        # Calculate the result
        result = solve(n, k, a)
        
        # Print the result
        print(result)

def solve(n, k, a):
    """
    This function solves the problem for a single test case.
    
    Args:
        n: The number of elements in the array.
        k: The maximum number of operations allowed.
        a: The array of integers.
    
    Returns:
        The maximum possible value of a[0] after performing at most k operations.
    """
    
    # Iterate through the array from the second element
    for i in range(1, n):
        # Calculate the number of operations that can be performed on the current element
        ops = min(k, a[i])
        
        # Increase the value of the first element by the number of operations
        a[0] += ops
        
        # Decrease the number of remaining operations
        k -= ops
    
    # Return the maximum possible value of the first element
    return a[0]

if __name__ == "__main__":
    main()
