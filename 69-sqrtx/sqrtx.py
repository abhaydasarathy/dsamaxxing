class Solution:
    def mySqrt(self, x: int) -> int:
        a=0
        left =0
        right=x
        if x==0:
            return 0
        for i in range(x):
            while(left<=right):
                mid=(left+right)//2
                if mid*mid == x:
                    return mid
                elif mid*mid<x:
                    left = mid + 1
                elif mid*mid > x:
                    right = mid -1
            return right




                
            
            
                
        