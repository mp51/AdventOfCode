from collections import namedtuple
from enum import IntEnum
from itertools import permutations 
import copy
import sys


# Instruction = namedtuple("Instruction", "op_code params")
Param = namedtuple("Param", "value mode")

class Operation(IntEnum):
   ADD = 1
   MULT = 2
   INPUT = 3
   OUTPUT = 4
   JUMP_IF_TRUE = 5
   JUMP_IF_FALSE = 6
   LESS_THAN = 7
   EQUALS = 8
   
   TERMINATE = 99

class Instruction:
   operations = {
      Operation.ADD: "Addition",
      Operation.MULT: "Multiplication",
      Operation.INPUT: "Input",
      Operation.OUTPUT: "Output",
      Operation.JUMP_IF_TRUE: "Jump-if-true",
      Operation.JUMP_IF_FALSE: "Jump-if-false",
      Operation.LESS_THAN: "Less-than",   
      Operation.EQUALS: "Equals",
      Operation.TERMINATE: "Terminate"
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
      self.operation = Operation(self.op_code)
      self.params_modes = (digits[2], digits[1], digits[0])

      if self.op_code in (Operation.ADD, 
                          Operation.MULT, 
                          Operation.LESS_THAN, 
                          Operation.EQUALS):
         self.params_count = 3
      elif self.op_code in (Operation.INPUT, 
                            Operation.OUTPUT):
         self.params_count = 1
      elif self.op_code in (Operation.JUMP_IF_TRUE, 
                            Operation.JUMP_IF_FALSE):
         self.params_count = 2
      else:
         self.params_count = 0

   def set_params(self, params):
      self.params = [Param(i, j) for i, j in zip(params, self.params_modes)]

      

class Computer:
   def __init__(self, memory_table, input_values):
      self.reset_memory(memory_table)
      self.input_values = input_values
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
         self.table[params[0].value] = self.input_values.pop(0)
         print("got input value:",self.table[params[0].value])
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

# Get all permutations of [0, 1, 2, 3, 4] 
phase_settings = permutations([0, 1, 2, 3, 4])
results = []
for phase in phase_settings:
   print(phase)

   result = 0
   for i in phase:
      input_values = [i, result]
      print("Input:", input_values)
      memory = copy.deepcopy(initial_memory)
      computer = Computer(memory, input_values)
      result = computer.compute_result()
      print("result:", result)

   print("result:", result)
   results.append(result)

print("Max result:", max(results))