from collections import namedtuple
from enum import IntEnum
from itertools import permutations
from itertools import cycle 
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

      
class State(IntEnum):
   RUNNING = 1
   WAITING_FOR_INPUT = 2
   FINISHED = 3

class Computer:
   def __init__(self, memory_table, input_value):
      self.reset_memory(memory_table)
      self.input_values = [input_value]
      self.jump_to = None
      self.state = State.RUNNING

   def set_input(self, input_value):
      self.input_values.append(input_value)
      self.state = State.RUNNING

   def reset_memory(self, initial_memory):
      self.table = copy.deepcopy(initial_memory)
      self._pos = 0

   def compute_result(self):
      while True:
         if (self.state == State.RUNNING):
            self.next_instruction = self.get_next_instruction()
            if self.next_instruction.op_code == 99:
               self.state = State.FINISHED
               break
         
         self.execute_instruction(self.next_instruction)
         if self.state == State.WAITING_FOR_INPUT:
            # return intermediate result and wait for the next input
            return self.table[0], self.state

         if self.jump_to:
            self._pos = self.jump_to
         else:
            self._pos += 1 + self.next_instruction.params_count

      return self.table[0], self.state
         
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
         if self.input_values:
            self.table[params[0].value] = self.input_values.pop(0)
         else:
            print("input value required")
            self.state = State.WAITING_FOR_INPUT
            return 
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

# Get all permutations of phases 
phase_settings = permutations([5, 6, 7, 8, 9])
# phase_settings = permutations([0, 1, 2, 3, 4])
results = []
for phase in phase_settings:
   print(phase)

   amplifiers = [Computer(copy.deepcopy(initial_memory), i) for i in phase]

   result = 0
   for i, amp in enumerate(cycle(amplifiers)):
      amp.set_input(result)
      print(i, amp.input_values)
      result, state = amp.compute_result()
      print(result, state)
      if (i+1)%5 == 0 and state == state.FINISHED:
         # The last amplifier in the loop finished computations
         results.append(result)
         print("Result:", result)
         break


print("Max result:", max(results))