def funu():
    x = {'1':'2'}
    i = 3
    while True:
        #print (x)
        x[i] = i
        i = i + 1
        if 300000000000 in x.keys():
            break
    print(x)
    print(i)

funu()

