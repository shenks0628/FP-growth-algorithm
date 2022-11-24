with open('mushroom.dat') as f:
    for s in f:
        tmp = s.strip()
        data = tmp.replace(' ', ',')
        print(data, file = open('mushroom.csv', 'a'))