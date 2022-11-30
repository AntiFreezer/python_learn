a = [0] * 30000
inp = input()

cur = 0
jumpindex = []
i = 0
intbrcount = 0

skipjump = False

while i < len(inp):
    if skipjump:
        if inp[i] == '[':
            intbrcount += 1
            i += 1
            continue

        if inp[i] == ']':
            if intbrcount > 0:
                intbrcount -= 1
                i += 1
                continue
            skipjump = False

        i += 1
        continue

    if inp[i] == '[' and a[cur] == 0:
        skipjump = True
        i += 1
        continue

    if len(jumpindex) > 0:
        if inp[i] == ']':
            i = jumpindex.pop()
            continue

    if inp[i] == '[' and a[cur] != 0:
        jumpindex.append(i)
        i += 1
        continue

    if inp[i] == ">":
        cur += 1
        if cur > 29999:
            cur -= 30000
    elif inp[i] == '<':
        cur -= 1
        if cur < 0:
            cur += 30000
    elif inp[i] == '+':
        a[cur] += 1
        if a[cur] > 255:
            a[cur] -= 256
    elif inp[i] == '-':
        a[cur] -= 1
        if a[cur] < 0:
            a[cur] += 256
    elif inp[i] == '.':
        print(a[cur])

    i += 1

