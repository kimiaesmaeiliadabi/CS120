from asyncio import base_tasks
import math
import time
import random

"""
See below for mergeSort and singletonBucketSort functions, and for the BC helper function.
"""


def merge(arr1, arr2):
    sortedArr = []

    i = 0
    j = 0
    while i < len(arr1) or j < len(arr2):
        if i >= len(arr1):
            sortedArr.append(arr2[j])
            j += 1
        elif j >= len(arr2):
            sortedArr.append(arr1[i])
            i += 1
        elif arr1[i][0] <= arr2[j][0]:
            sortedArr.append(arr1[i])
            i += 1
        else:
            sortedArr.append(arr2[j])
            j += 1

    return sortedArr

def mergeSort(arr):
    if len(arr) < 2:
        return arr

    midpt = int(math.ceil(len(arr)/2))

    half1 = mergeSort(arr[0:midpt])
    half2 = mergeSort(arr[midpt:])

    return merge(half1, half2)

def singletonBucketSort(univsize, arr):
    universe = []
    for i in range(univsize):
        universe.append([])

    for elt in arr:
        universe[elt[0]].append(elt)

    sortedArr = []
    for lst in universe:
        for elt in lst:
            sortedArr.append(elt)

    return sortedArr

def BC(n, b, k):
    if b < 2:
        raise ValueError()
    digits = []
    for i in range(k):
        digits.append(n % b)
        n = n // b
    if n > 0:
        raise ValueError()
    return digits

def radixSort(univsize, base, arr):
    """
    LSD Radix Sort using:
      - BC(n, b, k): returns the length-k base-b digit array (LSB first) for n
      - singletonBucketSort(univsize, arr): stable bucket sort on arr of pairs (key, value)
        with keys in [0, univsize-1].

    Inputs:
      univsize (U): size of the key universe (keys are in [0, U-1])
      base (b):     radix base (>= 2)
      arr:          list of pairs (K, V)
    Output:
      new list sorted by the numeric keys K (stable).
    """
    n = len(arr)
    if n <= 1 or univsize <= 1:
        # already sorted (all keys are 0 if U<=1)
        return arr[:]
    if base < 2:
        raise ValueError("base must be >= 2")

    # number of passes: k = ceil(log_b U)
    # (math.log(U, base) == log_b U; if U==1 then k=0, but we returned above)
    k = int(math.ceil(math.log(univsize, base)))

    # Precompute the length-k base-b digits for each key (LSB first) and
    # keep them attached to the record so we don't recompute.
    # Each 'record' is [digits, (K, V)] so that we can carry digits across passes.
    records = []
    for (K, V) in arr:
        digits = BC(K, base, k)   # length-k, LSD at index 0
        records.append([digits, (K, V)])

    # For each digit position j (LSB to MSB):
    for j in range(k):
        # Build the input for a stable bucket sort on the j-th digit.
        # singletonBucketSort expects a list of (key, value) with keys in [0, base-1].
        bucket_input = [(rec[0][j], rec) for rec in records]
        sorted_pairs = singletonBucketSort(base, bucket_input)

        # Unwrap back to the 'records' order for the next pass (stability preserved).
        records = [rec for (_, rec) in sorted_pairs]

    # Return the final order of (K, V) pairs.
    return [rec[1] for rec in records]
