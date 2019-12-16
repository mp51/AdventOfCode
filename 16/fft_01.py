def apply_phase(input_signal, phase):
   processed_signal = []
   for i in range(len(input_signal)):
      p_val = 0
      phase_idx = 0
      for j, val in enumerate(input_signal):
         if (j+1) % (i+1) == 0:
            phase_idx += 1
            if phase_idx == len(phase):
               phase_idx = 0

         p_val += val * phase[phase_idx]
      processed_signal.append(p_val)

   processed_signal = [int(str(i)[-1]) for i in processed_signal]
   return processed_signal 



input_signal = input()
input_signal = [int(i) for i in str(input_signal)]

phase = [0, 1, 0, -1]

for i in range(100):
   input_signal = apply_phase(input_signal, phase)
   print(i+1, input_signal)

