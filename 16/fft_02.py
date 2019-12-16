def apply_phase(input_signal, phase):
   processed_signal = []
   p_val = sum(input_signal)
   for i in range(len(input_signal)):
      processed_signal.append(p_val)
      p_val -= input_signal[i]

   processed_signal = [int(str(i)[-1]) for i in processed_signal]
   return processed_signal 


input_signal = input()
input_signal = [int(i) for i in str(input_signal)]

phase = [0, 1, 0, -1]

offset = 0
for i in range(7):
   offset += input_signal[i] * 10**(6-i)

read_offset = offset % len(input_signal)
idx_offset = offset - read_offset
multiple = idx_offset // len(input_signal)
times = 10_000 - multiple

print("Offset:", offset)
print("Input signal length:", len(input_signal))
print("Idx offset:", idx_offset)
print("Read offset:", read_offset)
print("Multiple:", multiple)
print("Extending input signal", times, "times")

input_signal *= times
input_signal = input_signal[read_offset:]

print("Extened input signal length:", len(input_signal))

for i in range(100):
   input_signal = apply_phase(input_signal, phase)
   print(i+1)

# print(input_signal)
output = 0
for i in range(8):
   output += input_signal[i] * 10**(7-i)
   print(output)

print("Output message:", output)