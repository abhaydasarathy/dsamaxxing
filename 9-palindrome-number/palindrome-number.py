class Solution:
    def isPalindrome(self, x: int) -> bool:
        original = x
        rev = rem = 0
        while x!=0 and x>0:
            rem = x%10
            x=x//10
            rev = rev *10+rem
        return rev == original


        