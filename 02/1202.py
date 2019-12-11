def compute_value(pos, sequence):
   val1_idx = sequence[pos + 1]
   val2_idx = sequence[pos + 2]
   result_idx = sequence[pos + 3]

   if sequence[pos] == 1:
      sequence[result_idx] = sequence[val1_idx] + sequence[val2_idx]
   elif sequence[pos] == 2:
      sequence[result_idx] = sequence[val1_idx] * sequence[val2_idx]



sequence = [int(i) for i in input().split(',')]

sequence[1] = 12
sequence[2] = 2

pos = 0
while True:
   if sequence[pos] == 99:
      break
   
   compute_value(pos, sequence)

   pos += 4

print(*sequence, sep=',')