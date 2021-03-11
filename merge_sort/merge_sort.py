l1 = ['Cristiano', 'Drogba', 'Kaka', 'Leo', 'Lukaku']
l2 = ['Armani', 'Bebeto', 'Mascherano', 'Rojo']
l3 = []

# Si yo lo tuviera que implementar
pos1 = pos2 = 0
while (pos1 < len(l1)) and (pos2 < len(l2)):
    if (l1[pos1] <= l2[pos2]):
        l3.append(l1[pos1])
        pos1 += 1
    else:
        l3.append(l2[pos2])
        pos2 += 1
if pos1 >= len(l1):
    l3 += l2[pos2:]
else:
    l3 += l1[pos1:]

print(l3)

# La manera fácil
print(sorted(l1+l2))

