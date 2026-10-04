class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(list(set(nums))) != len(nums) 