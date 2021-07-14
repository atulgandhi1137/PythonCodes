
n = int(input())

for i in range(1,n+1):
    for j in range(0, n-i):
        print(end = '_')
    for k in range(i):
        print(end = "*")
    print()