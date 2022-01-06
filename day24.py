# investigation!
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -14
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 2
# mul y x
# add z y

# W =
# X = (Z%26+15 != Inp)
# Y =
# Z = (Z or Z/26) * (25*X + 1) + (Inp+11) * X

# one by one:

# input 1 (Inp1)
# X = (Z%26+12 != Inp)  # always true, so always 1
# Z = (Z or Z/26) * (25*X + 1) + (Inp+4) * X
# meaning: Z = 0 * (...) + Inp + 4
# Z = Inp1 + 4

# input 2
# again, X=1 always
# Z = (Inp1 + 4) * 26 + (Inp2 + 11)

# input 3
# again, X=1 always
# Z = (Inp1 + 4) * 26 * 26 + (Inp2 + 11) * 26 + (Inp3 + 7)
# Z = (Inp1 + 4)e2 + (Inp2 + 11)e1 + (Inp3 + 7)e0

# input 4
# X = (Z%26-14 != Inp4)
# X = (Inp3 != Inp4 + 7)  # (inputs can only be 1-9)
# X = (inputs 3 and 4 aren't either [8,1] or [9,2] in this order)
# Z = ((Inp1 + 4)e1 + (Inp2 + 11)e0) * (25*X + 1) + (Inp4+2) * X
# if inputs 3 and 4 aren't these two options:
# Z = (Inp1 + 4)e2 + (Inp2 + 11)e1 + (Inp4 + 2)e0
# if they WERE one of those:
# Z = (Inp1 + 4)e1 + (Inp2 + 11)e0
# THEORY:  we can't allow them not to be the two options, because it means Z will be too big by the end
# for now let's assume they are one of the two options

# input 5
# again, impossible X equation
# Z = (Inp1 + 4)e2 + (Inp2 + 11)e1 + (Inp5 + 11)

# input 6
# X = (Z%26-10 != Inp6)
# X = (Inp5 + 1 != Inp6)
# X = false if inputs 5&6 are one of: [1,2], [2,3], ..., [8,9]
# continuing with previous assumption:
# X = 0
# Z = (Inp1 + 4)e1 + (Inp2 + 11)e0

# input 7
# Z = (Inp1 + 4)e2 + (Inp2 + 11)e1 + (Inp7 + 9)e0

# input 8
# ... etc Inp8 + 12

# -7
# requirement here is:
# inputs 8&9 have:  inp8+5=inp9  so [4,9]

with open('day24.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

# the following weird code will work because I remember the structure of the input codes
FOURTEEN = 14
stack_thing = []  # keeps (index, thing_added_to_digit)
solution = [0] * 14
for i in range(FOURTEEN):
    section_start = i * 18
    div_by_26 = int(lines[section_start + 4].split(' ')[2])
    thing_added_in_comparison = int(lines[section_start + 5].split(' ')[2])
    thing_added_to_digit = int(lines[section_start + 15].split(' ')[2])
    if div_by_26 == 1:
        assert (thing_added_in_comparison >= 9)
        # add to the stack thing
        stack_thing.append((i, thing_added_to_digit))
    else:
        assert (thing_added_in_comparison < 9)
        # remove top stack thing, compare
        top_i, top_value = stack_thing.pop()
        combined = top_value + thing_added_in_comparison
        if combined >= 0:
            # left + combined = right
            # right = 9, left = 9-combined
            solution[i] = 9
            solution[top_i] = 9 - combined
        elif combined < 0:
            # left - combined = right
            # left = 9, right = 9-combined
            solution[i] = 9 + combined
            solution[top_i] = 9

print(''.join(str(d) for d in solution))  # 92928914999991

stack_thing = []
solution = [0] * 14
for i in range(FOURTEEN):
    section_start = i * 18
    div_by_26 = int(lines[section_start + 4].split(' ')[2])
    thing_added_in_comparison = int(lines[section_start + 5].split(' ')[2])
    thing_added_to_digit = int(lines[section_start + 15].split(' ')[2])
    if div_by_26 == 1:
        # add to the stack thing
        stack_thing.append((i, thing_added_to_digit))
    else:
        # remove top stack thing, compare
        top_i, top_value = stack_thing.pop()
        combined = top_value + thing_added_in_comparison
        if combined <= 0:
            # left + combined = right
            # right = 1, left = 1-combined
            solution[i] = 1
            solution[top_i] = 1 - combined
        elif combined > 0:
            # left - combined = right
            # left = 9, right = 9-combined
            solution[i] = 1 + combined
            solution[top_i] = 1

print(''.join(str(d) for d in solution))  # 91811211611981
