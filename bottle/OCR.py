
import statistics






lst = [i for i in range(1, 500)]
# print(lst)
lst.reverse()
import time

a = time.time()
mean = statistics.mean(lst)
median = statistics.median(lst)
print(time.time()-a)
print(max(lst))
print(lst.pop(499))


