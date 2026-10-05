class Solution:
    def isPalindrome(self, s: str) -> bool:
        s1=s.lower()
        s2=''
        for i in s1:
            if i.isalnum()==False:
                continue
            else:
                s2+=i
        return s2==s2[::-1]

        