n = int(input())
h = []
re = []
for i in range(n):
    r, g, b = input().split()
    r = int(r)
    g = int(g)
    b = int(b)
    if i == 0:
        re.append([r, g, b])
    h.append([r, g, b])
for i in range(1,n):
    r = min(re[i-1][1], re[i-1][2])+h[i][0]
    g = min(re[i - 1][0], re[i - 1][2]) + h[i][1]
    b = min(re[i - 1][1], re[i - 1][0]) + h[i][2]
    re.append([r,g,b])

print(min(re[n-1][0], re[n-1][1],re[n-1][2]))



