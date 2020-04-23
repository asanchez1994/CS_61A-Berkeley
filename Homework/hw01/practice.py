def hailstone(n):

     print(n)
     count = 1
     if n == 1:
         return count
     if n % 2 == 0:
         count = hailstone(n // 2) + 1
     else:
         count = hailstone(n * 3 + 1) + 1
     return count 
     
print(hailstone(21))
