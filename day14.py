with open('day14.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

input_chain = lines[0]
rules = {}
for line in lines[2:]:
    pair, new_link = line.split(' -> ')
    rules[pair] = new_link


def simulate_x_steps(starting_chain, step_count):
    chain = starting_chain
    for step in range(step_count):
        next_chain = []
        for i in range(len(chain) - 1):
            next_link = rules[chain[i] + chain[i+1]]
            next_chain.append(chain[i])
            next_chain.append(next_link)
        next_chain.append(chain[-1])
        chain = next_chain
        # print(''.join(chain))
    return chain

def count_after_simulating(ending_chain):
    letter_counts = {}
    for c in ending_chain:
        if c not in letter_counts:
            letter_counts[c] = 0
        letter_counts[c] += 1
    return letter_counts

print('simulating 10 steps')
chain_after_10 = simulate_x_steps(input_chain, 10)
letter_counts_after_10 = count_after_simulating(chain_after_10)
highest_count_after_10 = max(letter_counts_after_10.values())
lowest_count_after_10 = min(letter_counts_after_10.values())
print('part 1:')
print(highest_count_after_10 - lowest_count_after_10)  # 3831


########### PART 2 (solved pretty badly;  we did not realize the trick, so we used a weird partial caching method)

output_counts_after_20_steps_per_rule = {}

print('simulating 20 steps per rule')
for pair in rules.keys():
    count_after_20 = count_after_simulating(simulate_x_steps(pair, 20))
    output_counts_after_20_steps_per_rule[pair] = count_after_20

print('simulating 20 steps from input line')
chain_after_20 = simulate_x_steps(input_chain, 20)

print('sum up counts for each pair in that chain')
letter_counts_after_40 = {}
for i in range(len(chain_after_20) - 1):
    pair = chain_after_20[i] + chain_after_20[i+1]
    counts_after_20_for_this_pair = output_counts_after_20_steps_per_rule[pair].copy()
    if i != 0:
        counts_after_20_for_this_pair[pair[0]] -= 1
    for letter, count in counts_after_20_for_this_pair.items():
        if letter not in letter_counts_after_40:
            letter_counts_after_40[letter] = 0
        letter_counts_after_40[letter] += count

print('almost done')
highest_count_after_40 = max(letter_counts_after_40.values())
lowest_count_after_40 = min(letter_counts_after_40.values())
print('part 2:')
print(highest_count_after_40 - lowest_count_after_40)  # 5725739914282

# example...
# WRONG (overcounting overlaps at edges):
# 2188191654846
# WRONG IN OTHER DIRECTION
# 1234312996237
# CORRECT
# 2188189693529






# BRILLIANT WHITE MAGIC BELOW

from collections import Counter

tpl, _, *rules = open('day14.txt').read().split('\n')
rules = dict(r.split(" -> ") for r in rules)
pairs = Counter(map(str.__add__, tpl, tpl[1:]))
chars = Counter(tpl)

for _ in range(40):
    for (a,b), c in pairs.copy().items():
        x = rules[a+b]
        pairs[a+b] -= c
        pairs[a+x] += c
        pairs[x+b] += c
        chars[x] += c

print('and now, repeating with a correct, super fast, genius solution we found on the internet later:')
print(max(chars.values())-min(chars.values()))