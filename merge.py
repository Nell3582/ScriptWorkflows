
lst = []
with open('1804.txt', 'r') as f:
    for line in f.readlines():
        lst.append(line.replace('\n', '').replace('\r', ''))
str = "@".join(lst).split("@")

with open("data1804.txt", 'w') as f:
    for i in str:
        f.write(i + '\n')
