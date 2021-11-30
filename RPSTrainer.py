"""
RPS Trainer that utilizes standard Counterfactual Regret Minimization
to generate a Nash Equilibrium that represents the GTO probability
distribution for a game of Rock Paper Scissors
"""

import random

def getStrategy(regretSum,strategySum):
    actions = 3
    normalization = 0
    strategy = [0,0,0]

    for i in range(0,actions):
        if regretSum[i] > 0:
            strategy[i] = regretSum[i]
        else:
            strategy[i] = 0

        normalization += strategy[i]

    for i in range(0,actions):
        if normalization > 0:
            strategy[i] = strategy[i] / normalization
        else:
            strategy[i] = 1.0/actions
        strategySum[i] += strategy[i]

    return (strategy,strategySum)

def getAction(strategy):
    r = random.uniform(0,1)
    cutoff1 = strategy[0]
    cutoff2 = strategy[1]
    cutoff3 = strategy[2]
    
    if r >= 0 and r < cutoff1:
        return 0
    elif r >= cutoff1 and r < (cutoff1 + cutoff2):
        return 1
    elif r >= (cutoff1 + cutoff2) and r < (cutoff1 + cutoff2 + cutoff3):
        return 2
    else:
        return 0

def getAvgStrategy(numiter, oppStrategy):
    actions = 3
    strategySum = train(numiter,[0,0,0],oppStrategy)
    avgStrategy = [0,0,0]
    normalization = 0
    for i in range(0,actions):
        normalization+= strategySum[i]
    for i in range(0,actions):
        if normalization>0:
            avgStrategy[i] = strategySum[i] / normalization
        else:
            avgStrategy[i] = 1.0/actions
    return avgStrategy

def train(numiter, regretSum, oppStrategy):
    actionMatrix = [0,0,0]
    strategySum = [0,0,0]
    actions = 3

    for i in range(0,numiter):
        temp = getStrategy(regretSum,strategySum)
        strategy = temp[0]
        strategySum = temp[1]
        #obtain our action from the calculated strategy distribution
        playeraction = getAction(strategy)
        #obtain opponents action from the calculated strategy distribution
        oppaction = getAction(oppStrategy)

        #opponent plays rock
        if oppaction == 0:
            actionMatrix[0] = 0  #regret of 0 for draw with rock
            actionMatrix[1] = -1 #regret of -1 for loss with scissros
            actionMatrix[2] = 1  #regret of +1 for win with paper
        #opponent plays scissors
        elif oppaction == 1:
            actionMatrix[0] = 1  #regret of -1 for win with rock
            actionMatrix[1] = 0  #regret of 0 for draw with scissors
            actionMatrix[2] = -1 #regret of +1 for loss with paper
        #opponent plays paper
        else:
            actionMatrix[0] = -1 #regret of -1 for loss with rock
            actionMatrix[1] = 1  #regret of +1 for win with scissors
            actionMatrix[2] = 0  #regret of 0 for draw with paper

        for i in range(0,actions):
            regretSum[i] += actionMatrix[i] - actionMatrix[playeraction]
            
    return strategySum

def train2Player(iterations,regretSum1,regretSum2,p2Strat):
    #Adapt Train Function for two players
    actions = 3
    actionUtility = [0,0,0]
    strategySum1 = [0,0,0]
    strategySum2 = [0,0,0]
    for i in range(0,iterations):
        #Retrieve Actions
        t1 = getStrategy(regretSum1,strategySum1)
        strategy1 = t1[0]
        strategySum1 = t1[1]
        myaction = getAction(strategy1)
        t2 = getStrategy(regretSum2,p2Strat)
        strategy2 = t2[0]
        strategySum2 = t2[1]
        otherAction = getAction(strategy2)
        
        #Opponent Chooses scissors
        if otherAction == actions - 1:
            #Utility(Rock) = 1
            actionUtility[0] = 1
            #Utility(Paper) = -1
            actionUtility[1] = -1
        #Opponent Chooses Rock
        elif otherAction == 0:
            #Utility(Scissors) = -1
            actionUtility[actions - 1] = -1
            #Utility(Paper) = 1
            actionUtility[1] = 1
        #Opopnent Chooses Paper
        else:
            #Utility(Rock) = -1
            actionUtility[0] = -1
            #Utility(Scissors) = 1
            actionUtility[2] = 1
            
        #Add the regrets from this decision
        for i in range(0,actions):
            regretSum1[i] += actionUtility[i] - actionUtility[myaction]
            regretSum2[i] += -(actionUtility[i] - actionUtility[myaction])
    return (strategySum1, strategySum2)

#Returns a nash equilibrium reached by two opponents through CFRM
def avgStrategyNoHuman(iterations,oppStrat):
    strats = train2Player(iterations,[0,0,0],[0,0,0],oppStrat)
    s1 = sum(strats[0])
    s2 = sum(strats[1])
    for i in range(3):
        if s1 > 0:
            strats[0][i] = strats[0][i]/s1
        if s2 > 0:
            strats[1][i] = strats[1][i]/s2
    return strats
    
randomStrategy = [.6,.2,.2]
print("Opponent Strategy: ",randomStrategy)
print("Exploitative Strategy: ", getAvgStrategy(100000,randomStrategy))
holders = avgStrategyNoHuman(10000,[.6,.2,.2])
print("Opponents equilibrium strategy: ", holders[0])
print("Players equilibrium strategy: ", holders[1])
