from collections import namedtuple
from enum import IntEnum
from itertools import permutations
from itertools import cycle 
import copy
import sys


class Param:
   def __init__(self, value, mode):
      self.value = value
      self.mode = mode

   def get_value(self, memory_table, relative_base):
      if self.mode == 0:
         return memory_table[self.value]
      elif self.mode == 1:
         return self.value
      elif self.mode == 2:
         return memory_table[self.value + relative_base]

   def get_address(self, relative_base):
      if self.mode == 2:
         return self.value + relative_base
      else:
         return self.value

   def __str__(self):
      return f'Param value: {self.value}, mode: {self.mode}'

class Operation(IntEnum):
   ADD = 1
   MULT = 2
   INPUT = 3
   OUTPUT = 4
   JUMP_IF_TRUE = 5
   JUMP_IF_FALSE = 6
   LESS_THAN = 7
   EQUALS = 8
   RELATIVE_BASE = 9
   
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
      Operation.RELATIVE_BASE: "SetRelativeBase",
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
                            Operation.OUTPUT,
                            Operation.RELATIVE_BASE):
         self.params_count = 1
      elif self.op_code in (Operation.JUMP_IF_TRUE, 
                            Operation.JUMP_IF_FALSE):
         self.params_count = 2
      else:
         self.params_count = 0

   def set_params(self, params):
      self.params = [Param(i, j) for i, j in zip(params, self.params_modes)]

   def __str__(self):
      return f'Instruction {self.op_code} ({Instruction.operations[self.op_code]})'

      
class State(IntEnum):
   RUNNING = 1
   WAITING_FOR_INPUT = 2
   FINISHED = 3

class Computer:
   def __init__(self, memory_table):
      self.reset_memory(memory_table)
      self.input_values = []
      self.jump_to = None
      self.state = State.RUNNING
      self.relative_base = 0
      self.output = []

   def set_input(self, input_value):
      self.input_values.append(input_value)
      self.state = State.RUNNING

   def reset_instruction_pointer(self):
      self._pos = 0

   def reset_memory(self, initial_memory):
      self.table = copy.deepcopy(initial_memory)
      self.table.extend([0]*1000)
      self._pos = 0

   def get_output(self):
      out = self.output
      self.output = []
      return out

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
            return self.get_output(), self.state

         if self.jump_to is not None:
            self._pos = self.jump_to
         else:
            self._pos += 1 + self.next_instruction.params_count
            
      return self.get_output(), self.state
         
   def get_next_instruction(self):
      instruction = Instruction(self.table[self._pos])
      params = tuple((self.table[self._pos + i] for i in range(1, instruction.params_count+1)))
      instruction.set_params(params)
      return instruction

   def get_param_value(self, param):
      if param.mode == 0:
         return self.table[param.value]
      elif param.mode == 1:
         return param.value
      elif param.mode == 2:
         return self.table[param.value + self.relative_base]

   def get_param_address(self, param):
      if param.mode == 2:
         return param.value + self.relative_base
      else:
         return param.value

   def execute_instruction(self, instruction):
      params = instruction.params

      get_val = lambda param: param.get_value(self.table, self.relative_base) 
      get_addr = lambda param: param.get_address(self.relative_base) 

      self.jump_to = None


      if instruction.op_code == Operation.ADD:
         self.table[get_addr(params[-1])] = get_val(params[0]) + get_val(params[1])

      elif instruction.op_code == Operation.MULT:
         self.table[get_addr(params[-1])] = get_val(params[0]) * get_val(params[1])

      elif instruction.op_code == Operation.INPUT:

         if self.input_values:
            self.table[get_addr(params[0])] = self.input_values.pop(0)
         else:
            self.state = State.WAITING_FOR_INPUT
            return 

      elif instruction.op_code == Operation.OUTPUT:
         self.output.append(get_val(params[0]))

      elif instruction.op_code == Operation.JUMP_IF_TRUE:
         if get_val(params[0]) != 0:
            self.jump_to = get_val(params[1])

      elif instruction.op_code == Operation.JUMP_IF_FALSE:
         if get_val(params[0]) == 0:
            self.jump_to = get_val(params[1])

      elif instruction.op_code == Operation.LESS_THAN:
         self.table[get_addr(params[-1])] = 1 if get_val(params[0]) < get_val(params[1]) else 0

      elif instruction.op_code == Operation.EQUALS:
         self.table[get_addr(params[-1])] = 1 if get_val(params[0]) == get_val(params[1]) else 0

      elif instruction.op_code == Operation.RELATIVE_BASE:
         self.relative_base += get_val(params[0])
