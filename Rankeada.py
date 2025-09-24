from ranking import rank

def organiza(lista):
  n = True
  for i in range(len(lista)-1):
    if lista[i][1]<lista[i+1][1]:
      lista[i], lista[i+1] = lista[i+1], lista[i]
      n = False
  return n

lis = []

for e in rank.items():
  lis.append(e)

while True:
  if organiza(lis):
    break

n =[]
i=0
while True:
  if i >= 10 or i >= len(lis):
    break
  n.append(lis[i])
  i += 1
