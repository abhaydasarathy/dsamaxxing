class Solution:
    def reverse(self, x: int) -> int:
        rev=0
        rem=0
        flag = 0
        if x<0:
            flag = 1
        x=abs(x)
        while x!=0:
            rem = x%10
            x=x//10
            rev=rev*10+rem
        if rev < -(2**31) or rev > (2**31)-1:
            return 0
        if flag==1:    
            return rev * -1
        else:
            return rev
        
        