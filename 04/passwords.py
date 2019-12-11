_range = (165432, 707912)

passwords = [[int(digit) for digit in str(number)] for number in range(_range[0], _range[1])]
print("Passwords count:", len(passwords))

def is_not_descending(password):
   for i in range(len(password) - 1):
      if password[i] > password[i+1]:
         return False
   return True

filtered1 = list(filter(is_not_descending, passwords))
print("Not descending passwords count:", len(filtered1))

def same_two_adjacent_digits(password):
   for i in range(len(password) - 1):
      if password[i] == password[i+1]:
         return True
   return False

def has_exact_two_same_adjacent_digits(password):
   adjacent_equal_digits = []
   temp = 1
   for i in range(len(password) - 1):
      if password[i] == password[i+1]:
         temp += 1
      else:
         adjacent_equal_digits.append(temp)
         temp = 1

   adjacent_equal_digits.append(temp)

   return 2 in adjacent_equal_digits

# Part 1
# filtered2 = list(filter(same_two_adjacent_digits, filtered1))

# Part 2
filtered2 = list(filter(has_exact_two_same_adjacent_digits, filtered1))
print("Final filtered passwords count:", len(filtered2))