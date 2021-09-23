i = 5
j = 2

L = [str(i)+"Geeks\n ", "for ", "Geeks "]

file1 = open('myfile.txt', 'w')
file1.writelines(L)
file1.close()

file1 = open('myfile.txt', 'r')
Lines = file1.readlines()
print(Lines)
count = 0
print(Lines[0])
print(len(Lines[0]))