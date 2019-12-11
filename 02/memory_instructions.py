from collections import namedtuple
import copy

Instruction = namedtuple("Instruction", "op_code params")

class Computer:
   def __init__(self, memory_table, noun, verb):
      self.reset_memory(memory_table, noun, verb)

   def reset_memory(self, initial_memory, noun, verb):
      self.table = copy.deepcopy(initial_memory)
      self.table[1] = noun
      self.table[2] = verb
      self._pos = 0

   def compute_result(self):
      while True:
         instruction = self._get_next_instruction()
         if instruction.op_code == 99:
            break
         self._execute_instruction(instruction)
      return self.table[0]
         
   def _get_next_instruction(self):
      op_code = self.table[self._pos]
      if op_code == 99:
         instruction = Instruction(op_code=op_code, params=None)
      else:
         instruction = Instruction(op_code=op_code, 
                                   params=(self.table[self._pos+1],
                                           self.table[self._pos+2],
                                           self.table[self._pos+3]))
         self._pos += 4
      return instruction

   def _execute_instruction(self, instruction):
      val1 = self.table[instruction.params[0]]
      val2 = self.table[instruction.params[1]]
      result_idx = instruction.params[2]

      if instruction.op_code == 1:
         self.table[result_idx] = val1 + val2
      elif instruction.op_code == 2:
         self.table[result_idx] = val1 * val2

EXPECTED_RESULT = 19690720
initial_memory = [int(i) for i in input().split(',')]

found = False
for noun in range(100):
   for verb in range(100):
      computer = Computer(initial_memory, noun, verb)
      result = computer.compute_result()
      print("result:", result, "noun:", noun, "verb:", verb)

      if result == EXPECTED_RESULT:
         found = True
         break
   if found:
      break

   

print("result:", result, "noun:", noun, "verb:", verb)
print("100 * noun + verb = ", (100 * noun + verb))
