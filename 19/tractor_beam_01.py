import int_comp as ic

def print_board(board):
   for row in board:
      print(''.join(row))
   print()


board_size = 50
board = [['.' for x in range(board_size)] for y in range(board_size)]

program = [int(i) for i in input().split(',')]

comp = ic.Computer(program)
output, state = comp.compute_result()

for i in range(board_size):
   for j in range(board_size):
      comp.set_input(i)
      comp.set_input(j)
      result, state = comp.compute_result()
      if result[0] == 1:
         board[i][j] = '#'
      print(i,j,result, state)

      comp.reset_memory(program, 2000000)


print_board(board)

hash_count = 0
for row in board:
   hash_count += row.count('#')

print('# count:', hash_count)