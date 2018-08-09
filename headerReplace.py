f = open('headers.txt', 'r')

content = f.read()


words = content.split('\t')

newArray = ', '.join('"{0}"'.format(w) for w in words)


print(newArray)

f.close()