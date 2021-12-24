import json


def parse_substring_inclusive(substring: str, start, end):
    return json.loads(substring[start:end + 1])


def add(a: str, b: str) -> str:
    pair = f'[{a},{b}]'
    return reduce(pair)


def magnitude(thing) -> int:
    if type(thing) == int:
        return thing
    else:
        a, b = thing
        return 3 * magnitude(a) + 2 * magnitude(b)


def reduce(input_pair: str) -> str:
    string = input_pair
    keep_trying_to_reduce = True
    while keep_trying_to_reduce:
        keep_trying_to_reduce = False
        # check if any pair is nested inside four pairs - if so, explode
        nesting_level = 0
        for i in range(len(string)):
            if string[i] == '[':
                nesting_level += 1
                if nesting_level >= 5:
                    # explode!
                    # 1. find start and end indices of exploding pair
                    exp_pair_end = string.find(']', i + 1)
                    exp_pair_start = string.rfind('[', i, exp_pair_end)
                    exp_pair = parse_substring_inclusive(string, exp_pair_start, exp_pair_end)
                    first_number, second_number = exp_pair
                    # 2. find indices of first number left of pair and first number right of pair
                    lefter_end = exp_pair_start
                    lefter_start = -1
                    # 2.1.1 find right end of number on the left (could be multiple digits!).  inclusive!
                    while lefter_end >= 0 and not string[lefter_end].isdigit():
                        lefter_end -= 1
                    lefter_exists = lefter_end != -1
                    if lefter_exists:
                        # 2.1.2 find left end of number on the left (could be multiple digits!)
                        lefter_start = lefter_end - 1
                        while lefter_start >= 0 and string[lefter_start].isdigit():
                            lefter_start -= 1
                        lefter_start += 1
                        # 2.1.3. add up the numbers
                        new_lefter = parse_substring_inclusive(string, lefter_start, lefter_end) + first_number
                    else:
                        new_lefter = None
                    # 2.2.1 find left end of number on the right (...)
                    righter_start = exp_pair_end
                    righter_end = -1
                    while righter_start < len(string) and not string[righter_start].isdigit():
                        righter_start += 1
                    righter_exists = righter_start != len(string)
                    if righter_exists:
                        # 2.2.2 find right end of number on the right (could be multiple digits!)
                        righter_end = righter_start + 1
                        while righter_end < len(string) and string[righter_end].isdigit():
                            righter_end += 1
                        righter_end -= 1
                        new_righter = parse_substring_inclusive(string, righter_start, righter_end) + second_number
                    else:
                        new_righter = None
                    # 4. create the result!
                    string = (string[:lefter_start] + str(new_lefter) if lefter_exists else '') + \
                             string[lefter_end + 1:exp_pair_start] + \
                             str(0) + \
                             string[exp_pair_end + 1:righter_start] + \
                             (str(new_righter) + string[righter_end + 1:] if righter_exists else '')
                    keep_trying_to_reduce = True
                    break
            if string[i] == ']':
                nesting_level -= 1
        # try checking for explosions again before checking splits
        if keep_trying_to_reduce:
            continue
        # check if any number is 10+ - if so, split
        for i in range(len(string)):
            if string[i].isdigit():
                num_start = i
                num_end = i + 1
                while string[num_end].isdigit():
                    num_end += 1
                num_end -= 1
                if num_start != num_end:  # i.e. if number is 10+
                    # split!
                    number = parse_substring_inclusive(string, num_start, num_end)
                    new_pair = f'[{number // 2},{(number + 1) // 2}]'
                    string = string[:num_start] + \
                             new_pair + \
                             string[num_end + 1:]
                    keep_trying_to_reduce = True
                    break
    return string


with open('day18.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

current = lines[0]
for line in lines[1:]:
    current = add(current, line)
    # print(current)
print(magnitude(json.loads(current)))


best_magnitude = 0
for line in lines:
    for other_line in lines:
        if line == other_line:
            continue  # assuming no duplicates
        this_magnitude = magnitude(json.loads(add(line, other_line)))
        best_magnitude = max(this_magnitude, best_magnitude)

print(best_magnitude)