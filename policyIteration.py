import enum

iterations = 0
actions = {}
discount_factor = 0

values = {}
reward = {}
policy = {}
transactionProb = {}


class states(enum.Enum):
    IN = 1
    SUBURB = 2
    OUT = 3


class actions(enum.Enum):
    DRIVE = 1
    WAIT = 0


# values
for state in states:
    values[state] = 0

    # policy starts with never driving (wait)
    policy[state] = actions.WAIT

for state in states:
    for action in actions:
        for nextState in states:
            transactionProb[(state, action, nextState)] = 0
            reward[(state, action, nextState)] = 0

# problem variables
iterations = 100
discount_factor = 0.8

# transaction probabilities
transactionProb[(states.IN, actions.DRIVE, states.IN)] = 0.9
transactionProb[(states.IN, actions.DRIVE, states.SUBURB)] = 0.1
transactionProb[(states.IN, actions.WAIT, states.IN)] = 0.7
transactionProb[(states.IN, actions.WAIT, states.SUBURB)] = 0.3

transactionProb[(states.SUBURB, actions.DRIVE, states.IN)] = 0.3
transactionProb[(states.SUBURB, actions.DRIVE, states.SUBURB)] = 0.6
transactionProb[(states.SUBURB, actions.DRIVE, states.OUT)] = 0.1
transactionProb[(states.SUBURB, actions.WAIT, states.OUT)] = 1

transactionProb[(states.OUT, actions.DRIVE, states.IN)] = 0.6
transactionProb[(states.OUT, actions.DRIVE, states.OUT)] = 0.4
transactionProb[(states.OUT, actions.WAIT, states.OUT)] = 1

# rewards
reward[(states.IN, actions.DRIVE, states.IN)] = 20
reward[(states.IN, actions.DRIVE, states.SUBURB)] = 0
reward[(states.IN, actions.WAIT, states.IN)] = 30
reward[(states.IN, actions.WAIT, states.SUBURB)] = 10

reward[(states.SUBURB, actions.DRIVE, states.IN)] = 20
reward[(states.SUBURB, actions.DRIVE, states.SUBURB)] = 0
reward[(states.SUBURB, actions.DRIVE, states.OUT)] = 0
reward[(states.SUBURB, actions.WAIT, states.OUT)] = 10

reward[(states.OUT, actions.DRIVE, states.IN)] = 20
reward[(states.OUT, actions.DRIVE, states.OUT)] = 0
reward[(states.OUT, actions.WAIT, states.OUT)] = 10


def updateStateValues():
    values[states.IN] = 0
    values[states.SUBURB] = 0
    values[states.OUT] = 0


def obtainQvalues(state, action):
    optimunValue = 0
    for s_next in states:
        optimunValue += transactionProb[(state, action, s_next)] * \
                       (reward[(state, action, s_next)] + (discount_factor * values[s_next]))
    return optimunValue


for i in range(iterations):
    for state in states:
        # calculate the value for the action obtained from the policy
        values[state] = obtainQvalues(state, policy[state])

        # get better policy for the next iteration
    Qvalues = {}
    for action in actions:
        Qvalues[action] = obtainQvalues(state, policy[state])
    policy[state] = max(Qvalues, key=Qvalues.get)


print ''
print 'Policy: '
print '-------'
for state in states:
    print 'policy(' + str(state) + ') = ', policy[state]

print ''
print ''
print 'Values: '
print '-------'
for state in states:
    print 'value(' + str(state) + ') = ', values[state]

'''
policy: 
-------
policy(states.IN) =  actions.WAIT
policy(states.SUBURB) =  actions.WAIT
policy(states.OUT) =  actions.DRIVE


values: 
-------
value(states.IN) =  97.836166924
value(states.SUBURB) =  79.3663060276
value(states.OUT) =  86.7078825345
'''
