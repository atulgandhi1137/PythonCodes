count = 0
n = 2
j = 0

while count <= 100:
    for k in range(2, n):
        if n%k == 0:
            j += 1
            break

    if j == 0:
        count += 1
        print(n)
    
    j = 0 
    n += 1