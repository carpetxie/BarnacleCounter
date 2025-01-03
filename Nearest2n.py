import math
import heapq

powers_of_two = [2] * 11
for i in range(10):
    powers_of_two[i + 1] = powers_of_two[i] * 2


# Given a value val, finds the n such that abs(2^n - val) is minimum

def findClosest(val):
    diff = abs(powers_of_two[0] - val)
    closest2n = 0
    for i in range(10):
        tempDiff = abs(powers_of_two[i + 1] - val)
        if tempDiff <= diff:
            closest2n = i + 1
        else:
            break
        
    return powers_of_two[closest2n - 1]







    
    