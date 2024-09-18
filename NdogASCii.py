ascii  = [chr(i) for i in range(ord('0'), ord('9')+1)]
ascii += [chr(i) for i in range(ord('a'), ord('z')+1)]
print(ascii)
with open('c:/dev/ascii.txt', mode='w', encoding='utf_8') as aski:
    for i in ascii:
        for j in ascii:
            print(f'{i}{j}', file = aski)
