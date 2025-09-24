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

