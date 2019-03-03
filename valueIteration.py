import enum

iterations = 0
actions = {}
discount_factor = 0

values = {}
reward = {}
transactionProb = {}


class states(enum.Enum):
    IN = 1
    SUBURB = 2
    OUT = 3

class actions(enum.Enum):
    DRIVE = 1
    WAIT = 0

def initialize():
    for state in states:
        values[state] = 0
        for action in actions:
            for nextState in states:
                transactionProb[zip(state, action, nextState)] = 0
                reward[zip(state, action, nextState)] = 0


def defineProblem():
    discount_factor = 0.8

    # transaction probabilities
    transactionProb[zip(states.IN, actions.DRIVE, states.IN)] = 0.9
    transactionProb[zip(states.IN, actions.DRIVE, states.SUBURB)] = 0.1
    transactionProb[zip(states.IN, actions.WAIT, states.IN)] = 0.7
    transactionProb[zip(states.IN, actions.WAIT, states.SUBURB)] = 0.3

    transactionProb[zip(states.SUBURB, actions.DRIVE, states.IN)] = 0.3
    transactionProb[zip(states.SUBURB, actions.DRIVE, states.SUBURB)] = 0.6
    transactionProb[zip(states.SUBURB, actions.DRIVE, states.OUT)] = 0.1
    transactionProb[zip(states.SUBURB, actions.WAIT, states.OUT)] = 0.1

    transactionProb[zip(states.OUT, actions.DRIVE, states.IN)] = 0.6
    transactionProb[zip(states.OUT, actions.DRIVE, states.OUT)] = 0.4
    transactionProb[zip(states.OUT, actions.WAIT, states.OUT)] = 0.1

    # rewards
    reward[zip(states.IN, actions.DRIVE, states.IN)] = 0.9
    reward[zip(states.IN, actions.DRIVE, states.SUBURB)] = 0.1
    reward[zip(states.IN, actions.WAIT, states.IN)] = 0.7
    reward[zip(states.IN, actions.WAIT, states.SUBURB)] = 0.3

    reward[zip(states.SUBURB, actions.DRIVE, states.IN)] = 0.3
    reward[zip(states.SUBURB, actions.DRIVE, states.SUBURB)] = 0.6
    reward[zip(states.SUBURB, actions.DRIVE, states.OUT)] = 0.1
    reward[zip(states.SUBURB, actions.WAIT, states.OUT)] = 0.1

    reward[zip(states.OUT, actions.DRIVE, states.IN)] = 0.6
    reward[zip(states.OUT, actions.DRIVE, states.OUT)] = 0.4
    reward[zip(states.OUT, actions.WAIT, states.OUT)] = 0.1


def updateStateValues():
    values[states.IN] = 0
    values[states.SUBURB] = 0
    values[states.OUT] = 0

# assign transaction probabilities


# assign rewards


def obtainQvalues(state, action):
    for s_next in states:
        optimunValue = transactionProb[(state, action, s_next)] * \
                       (reward[(state, action, s_next)] + (discount_factor * values[s_next]))
    return optimunValue


defineProblem()
for i in range(iterations):
    for state in states:
        Qvalues = []
        for action in actions:
            Qvalues.append(obtainQvalues(state, action))
        values[state] = max(Qvalues)
