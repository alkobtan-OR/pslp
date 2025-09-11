
def instance(T, S, N):
  N_a = N 
  if N > T*S:
    print('Invalid Number of items')
    return error 

  if N < T*S: 
    N_a = T*S

  P = list(range(1, N+1))  # integers from 0 to N-1
  random.shuffle(P)

  print(f'{T}, {S}')
  print 
  return P 
