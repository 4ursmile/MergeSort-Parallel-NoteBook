""""""
import numpy as np

 #Just a merge in merge sort was combine in MSPL module 
def Merge(*args):
    """ This is just a merge phase in merge sort

    arg: 
        get 1 or 2 list was ordered
    Returns:
        list : list was merge in odered
    """
    res = []
    i = 0
    j = 0
    L,R = args[0] if len(args) == 1 else args
    while(i<len(L) and j<len(R)):
        if (L[i] < R[j]):
            res.append(L[i])
            i+=1
        else:
            res.append(R[j])
            j+=1
    if (i<len(L)):
        res = np.append(res, L[i:])
    if (j<len(R)):
        res = np.append(res, R[j:])
    return res
def MergeSort(A):
    """ This is  merge sort

    arg: 
        get 1 list
    Returns:
        list : list was sorted
    """
    #just a merge sort method
    if (len(A) <=1): 
        return A
    mid = int(len(A)/2)
    L = MergeSort(A[0:mid])
    R = MergeSort(A[mid:])
    return Merge(L,R)

import time
def Mesuare(arr , func):
    tic = time.time()
    arrS = func(arr)
    toc = time.time()
    MS_time = (toc-tic)*1000
    print(f'{func.__name__}, time used {MS_time} ms) \n')
    return MS_time

import random

def QuickSort(arr):
    """ This is quick sort funcion
    """
    if len(arr) <= 1:
        return arr
    
    pivot = random.choice(arr)
    left = []
    right = []
    pivot_list = []
    
    for i in arr:
        if i < pivot:
            left.append(i)
        elif i > pivot:
            right.append(i)
        else:
            pivot_list.append(i)
    
    return QuickSort(left) + pivot_list + QuickSort(right)

"""
Above is another implement of MergeSortParallel 
Run and compare it
"""
import multiprocessing

def MergeSortParallelVer0(A):
    if (len(A) <=1): 
        return A
    mid = int(len(A)/2)
    with multiprocessing.Pool(2) as pool:
        L = pool.apply_async(MergeSort, [A[0:mid]])
        R = pool.apply_async(MergeSort, [A[mid:]])
        L = L.get()
        R = R.get()
    return Merge(L,R)

def MergeSortParallel(A):
    """ This is merged sort parallel

    arg: 
        get 1 list
    Returns:
        list : list was sorted
    """
    n = len(A)
    if n <=1: 
        return A
    n_process = multiprocessing.cpu_count()

    A = np.array_split(A, n_process)
    
    pool = multiprocessing.Pool(n_process)
    A = pool.map(MergeSort, A)
    while len(A)>1:
        odd_part = []
        if len(A) % 2 != 0:
            odd_part = A.pop()
        A = [(A[i],A[i+1]) for i in range(0,len(A),2)]
        if len(odd_part) == 0:
            A = pool.map(Merge, A)
        else:
            A = pool.map(Merge, A) + odd_part
    return A[0]

if __name__ == '__main__':
    arr = np.random.randint(0, 2000000, size=100000)
    MS_time = Mesuare(arr, MergeSort)
    MSP_time = Mesuare(arr, MergeSortParallel)
    MSQP_time =  Mesuare(arr, QuickSort)
    if (MS_time > MSP_time):
        print(f"MergeSort: Parallel version !!! FASTER !!! than normal version {MS_time/MSP_time} times!!!")
    else:
        print(f"MergeSort: Parallel version !!! SLOWER !!! than normal version {MSP_time/MS_time} times!!!")
        