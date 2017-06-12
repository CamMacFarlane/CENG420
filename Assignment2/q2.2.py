import random
import string

stringOfLetters = string.ascii_uppercase
num_items = 10
profit_min = 10
profit_max = 100
weight_min = 1
weight_max = 50
capacity = 25

items_l = [stringOfLetters[i] for i in range(num_items)]
weights_l = [random.randint(weight_min,weight_max) for i in range(num_items)]
profits_l = [random.randint(profit_min,profit_max) for i in range(num_items)]


for i in range(num_items):
    print("Item ", items_l[i] , "weight ", weights_l[i], "profit", profits_l[i])

def greedy(items, weights, profits, capacity):
    knapsack = list()
    totalWeight = 0
    totalProfit = 0
    num_items = len(items)
    ratio = [profits[i]/weights[i] for i in range(num_items)]

    while(len(items) > 0):
        candidate = ratio.index(max(ratio))
        
        if((totalWeight + weights[candidate]) < capacity):
            knapsack.append(items[candidate])
            totalWeight = totalWeight + weights[candidate]
            totalProfit =+ profits[candidate]
                
        items.pop(candidate)
        weights.pop(candidate)
        profits.pop(candidate)
        ratio.pop(candidate)

    print("Output from Greedy: ")
    print(knapsack, "Total weight: ", totalWeight, "/", capacity, "Total Profit", totalProfit )

greedy(items_l,weights_l,profits_l,capacity)