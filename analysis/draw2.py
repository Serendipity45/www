from collections import Counter

# 示例数组
arr = [1, 2, 3, 4, 5, 1, 2, 3, 1, 2, 1, 1]

# 使用Counter计算每个数字出现的次数
counts = Counter(arr)

# 按照数字顺序对次数进行排序
sorted_counts = sorted(counts.items(), key=lambda x: x[0])

# 提取排序后的次数
sorted_counts_values = [count for _, count in sorted_counts]

# 输出结果
print(sorted_counts_values)