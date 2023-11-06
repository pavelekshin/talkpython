def twoSum(nums, target):
    d = {}
    for indx, value in enumerate(nums):
        num = target - value
        if num not in d.keys():
            d[value] = indx
        else:
            print(d.items())
            return [d.get(num),indx]


if __name__ == "__main__":
    print(twoSum([3, 2, 1, 4], 6))
