"""mdp
Implement mdp Value Iteration algorithm
input:mdpinput.txt
output:policy.txt
"""
import copy
def maxaction(idx, states, actions, transition_model, gamma, reward, unow):
    """ argmax maxu action for given state to other states
        output:maxutility
    """
    uiti = []
    for action in actions:
        action_u = float(0)
        #plus reward
        action_u += reward[states[idx]][action]
        # every action
        for j in range(len(states)):
            action_u += gamma*unow[j]*transition_model[action][idx][j]
        uiti.append((action_u, action))
    return max(uiti)

def value_iteration(mdp, epsilon):
    """ implement VL algorithm
        inputs:
        mdp, an mdp with states S(list), action(list of array),
        transition model: action-(state1,state2)
        reward (dic of dic) state-action-u
        discount(float)
        epsilon float
        output:
        Converged uitility
    """
    s_vi, actions, transition_model, reward, gamma = mdp[0], mdp[1], mdp[2], mdp[3], mdp[4]
    u_vi, u_prime, delta = [float(0)]*len(s_vi), [float(0)]*len(s_vi), float('inf')
    while delta > epsilon*(1 - gamma)/gamma:
        u_vi, delta = copy.deepcopy(u_prime), float(0)
        lastaction = ['']*len(s_vi)
        for iss in range(len(s_vi)):
            u_prime[iss], lastaction[iss] = maxaction(iss, s_vi, actions, transition_model, gamma, reward, u_vi)
            if abs(u_prime[iss] - u_vi[iss]) > delta:
                delta = abs(u_prime[iss] - u_vi[iss])
    return u_vi, lastaction

def reward_initialize(reward, line_w):
    """ initialize reward as a dicitonay
    """
    line_s = line_w.strip().split(',')
    state, action, rsa = line_s[0].strip(), line_s[1].strip(), line_s[2].strip()
    if state not in reward.keys():
        reward[state] = {}
        reward[state][action] = float(rsa)
    else:
        reward[state][action] = float(rsa)

def actions_initialize(acts, actions, line_w):
    """ initialize action as a list
    """
    line_s = line_w.strip().split(',')
    for action in line_s:
        actions[action.strip()] = []
        acts.append(action.strip())

def states_initialize(states, line_w):
    """ initialize states as a list
    """
    line_s = line_w.strip().split(',')
    for state in line_s:
        states.append(state.strip())

def actions_update(action, actions, line_w):
    """ update action dictionary
    """
    line_s = line_w.strip().split(',')
    col = []
    for val in line_s:
        col.append(float(val.strip()))
    actions[action].append(col)

if __name__ == '__main__':
    INPUT_PATH = 'mdpinput.txt'
    STATES = []
    ACT = []
    ACTIONS = {}
    REWARD = {}
    GAMMA = float(0)
    EPSILON = float(0)
    with open(INPUT_PATH, 'r') as f:
        COUNT = 0
        NUMLINE = 0
        for line in f:
            if line[0] == '%':
                COUNT += 1
                continue
            if COUNT == 1:
                states_initialize(STATES, line)
            if COUNT == 2:
                actions_initialize(ACT, ACTIONS, line)
            if COUNT >= 5 and COUNT <= 4 + len(ACT):
                NUMSTATES = len(STATES)
                actions_update(ACT[NUMLINE/NUMSTATES], ACTIONS, line)
                NUMLINE += 1
            if COUNT == 5 + len(ACT):
                reward_initialize(REWARD, line)
            if COUNT == 6 + len(ACT):
                GAMMA = float(line.strip())
            if COUNT == 7 + len(ACT):
                EPSILON = float(line.strip())

        UTILITY, LASTACTION = value_iteration((STATES, ACT, ACTIONS, REWARD, GAMMA), EPSILON)
        OUTPUT_PATH = 'policy.txt'
        with open(OUTPUT_PATH, 'w+') as f:
            f.write("%"+" Format: State: Action (Value)"+'\n')
            for i in range(len(STATES)):
                f.write(str(STATES[i])+": "+str(LASTACTION[i])+" " \
                	+"("+str(round(UTILITY[i], 2)) +")"+'\n')
