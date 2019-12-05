from collections import namedtuple
import copy

# Instruction = namedtuple("Instruction", "op_code params")
Param = namedtuple("Param", "value mode")

class Instruction:
   operations = {
      1: "Addition",
      2: "Multiplication",
      3: "Input",
      4: "Output",
      5: "Jump-if-true",
      6: "Jump-if-false",
      7: "Less-than",   
      8: "Equals",
      99: "Terminate"
   }

   def __init__(self, int_code):
      # convert int code to list of digits
      digits = [int(d) for d in str(int_code)]
      # ensure instruction code is of format ABCDE where:
      # DE - operation code
      # C - mode of 1st param
      # B - mode of 2nd param
      # A - mode of 3rd param
      while len(digits) < 5:
         digits.insert(0, 0)

      self.op_code = digits[-2]*10 + digits[-1]
      self.params_modes = (digits[2], digits[1], digits[0])

      if self.op_code in (1, 2, 7, 8):
         self.params_count = 3
      elif self.op_code in (3, 4):
         self.params_count = 1
      elif self.op_code in (5, 6):
         self.params_count = 2
      else:
         self.params_count = 0

   def set_params(self, params):
      self.params = [Param(i, j) for i, j in zip(params, self.params_modes)]

      

class Computer:
   def __init__(self, memory_table, input_value):
      self.reset_memory(memory_table)
      self.input_value = input_value
      self.jump_to = None

   def reset_memory(self, initial_memory):
      self.table = copy.deepcopy(initial_memory)
      self._pos = 0

   def compute_result(self):
      while True:
         instruction = self.get_next_instruction()
         if instruction.op_code == 99:
            break
         self.execute_instruction(instruction)

         if self.jump_to:
            self._pos = self.jump_to
         else:
            self._pos += 1 + instruction.params_count

      return self.table[0]
         
   def get_next_instruction(self):
      instruction = Instruction(self.table[self._pos])
      params = tuple((self.table[self._pos + i] for i in range(1, instruction.params_count+1)))
      instruction.set_params(params)
      return instruction

   def get_from_memory(self, param):
      if param.mode == 0:
         return self.table[param.value]
      else:
         return param.value

   def execute_instruction(self, instruction):
      params = instruction.params

      self.jump_to = None
      if instruction.op_code == 1:
         self.table[params[-1].value] = self.get_from_memory(params[0]) + self.get_from_memory(params[1])
      elif instruction.op_code == 2:
         self.table[params[-1].value] = self.get_from_memory(params[0]) * self.get_from_memory(params[1])
      elif instruction.op_code == 3:
         self.table[params[0].value] = self.input_value
      elif instruction.op_code == 4:
         self.table[0] = self.get_from_memory(params[0])
      elif instruction.op_code == 5:
         if self.get_from_memory(params[0]) != 0:
            self.jump_to = self.get_from_memory(params[1])
      elif instruction.op_code == 6:
         if self.get_from_memory(params[0]) == 0:
            self.jump_to = self.get_from_memory(params[1])
      elif instruction.op_code == 7:
         self.table[params[-1].value] = 1 if self.get_from_memory(params[0]) < self.get_from_memory(params[1]) else 0
      elif instruction.op_code == 8:
         self.table[params[-1].value] = 1 if self.get_from_memory(params[0]) == self.get_from_memory(params[1]) else 0



initial_memory = [int(i) for i in input().split(',')]

input_value = 5

computer = Computer(initial_memory, input_value)
result = computer.compute_result()
print("result:", result)


