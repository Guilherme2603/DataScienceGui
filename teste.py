tentativas =  int(input())

for i in range(tentativas):
    pa, pb, g1, g2 = map(float, input().split())
    anos = 0
    while pa < pb and anos <= 100:
        pa *= 1 + g1 / 100
        pb *= 1 + g2 / 100
        anos += 1
        pa, pb = int(pa), int(pb)  

    if anos <= 100:
        print(f'{anos} anos.')
    else:
        print('Mais de 1 seculo.')