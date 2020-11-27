num = []
num2 = []


for i in range(1, 11):
    n = input('Digite o {}º número(apenas números inteiros)! \n'.format(i))
    num.append(n)
    num2.append(n)

print()
print('Primeiro Vetor')
for i in range(len(num)):
    print(num[i])

print()
print('Segundo Vetor')
for i in range(len(num2)-1, -1, -1):
    print(num2[i],i)