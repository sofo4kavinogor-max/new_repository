import itertools

# 1. Количество способов подняться по лестнице
def climb_ways(n):
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# 2. Максимальная сумма подотрезка
def max_subarray(nums):
    max_sum = curr_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum

# 3. Размен монет
def min_coins(n):
    coins = [1, 3, 4]
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        for c in coins:
            if i - c >= 0:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return dp[n]

# 4. Расстояние Левенштейна
def levenshtein(s1, s2):
    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    for i in range(len(s1) + 1):
        dp[i][0] = i
    for j in range(len(s2) + 1):
        dp[0][j] = j
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
    return dp[-1][-1]

# Тесты
if __name__ == "__main__":
    print("1. Лестница:", climb_ways(7))
    print("2. Максимальная сумма подотрезка:", max_subarray([-2,1,-3,4,-1,2,1,-7,8]))
    print("3. Минимальное количество монет для суммы:", min_coins(6))
    print("4. Расстояние Левенштейна:", levenshtein("рот", "скат"))
