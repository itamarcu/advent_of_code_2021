
with open('day10.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

BRACKETS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
STARTER_CHARS = list(BRACKETS.keys())
ENDER_CHARS = list(BRACKETS.values())
SYNTAX_SCORE_TABLE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
AUTOCOMPLETE_SCORE_TABLE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

total_syntax_score = 0
completion_scores = []
for line in lines:
    # print(line)
    stack = []
    for c in line:
        if c in STARTER_CHARS:
            stack.append(c)
        else:  # ender char
            expected_ender = BRACKETS[stack[-1]]
            if c == expected_ender:
                stack.pop(-1)
            else:
                # print(f'Expected {expected_ender}, but found {c} instead.')
                total_syntax_score += SYNTAX_SCORE_TABLE[c]
                stack = []
                break
    if stack:
        # find score of completion
        score = 0
        while stack:
            c = stack.pop()
            score *= 5
            score += AUTOCOMPLETE_SCORE_TABLE[BRACKETS[c]]
        completion_scores.append(score)

print(total_syntax_score)  # 469755

completion_scores.sort()
print(completion_scores[(len(completion_scores) - 1) // 2])  # 2762335572