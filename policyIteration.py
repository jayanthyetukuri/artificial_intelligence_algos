import enum

iterations = 20
actions = {0, 1}
discount_factor = 0.8

values = {}
reward = {}
transactionProb = {}
policy = {}

class states(enum.Enum):
    IN = 1
    SUBURB = 2
    OUT = 3


def updateStateValues():
    values[states.IN] = 0
    values[states.SUBURB] = 0
    values[states.OUT] = 0

# assign transaction probabilities


# assign rewards


# define policy

for state in states:
    for nextState in states:
        policy[(state, nextState)] = actions[0]


def obtainQvalues(state):
    for s_next in states:
        optimunValue = transactionProb[(state, policy[(state, nextState)], s_next)] * \
                       (reward[(state, policy[(state, nextState)], s_next)] + (discount_factor * values[s_next]))
    return optimunValue


for i in range(iterations):
    for state in states:
        Qvalues = []
        for action in actions:
            Qvalues.append(obtainQvalues(state, action))
        values[state] = max(Qvalues)
