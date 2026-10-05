class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        count = nums.count(0)
        if count !=0:
            for i in nums:
                if i==0:
                    nums.remove(i)
                    nums.append(0)
        return nums
        