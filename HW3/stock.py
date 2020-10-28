"""
Stock market prediction using Markov chains.

For each function, replace the return statement with your code.  Add
whatever helper functions you deem necessary.
"""

import comp140_module3 as stocks
from collections import defaultdict
import random

def customize():
    """
    input: none
    output: a default dictionary
    customize serves as the function that returns the defualt dictionary
    as the default value of the previous markov_chain
    """
    return defaultdict(float)

### Model
def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the markov chain

    returns: a dictionary that represents the Markov chain
    """
    
    ### use a default dict to store the markov chain:{n-order-tuple:{outcomen:pn}}
    res = defaultdict(customize)
    
    ### 
    for index in range(len(data)):
        ### since tuple is unmutable; use a list to store the key
        lst_key = []
        ### determine if possible to form a chain
        if index + order + 1 <= len(data):
            ### if possible parse to form a n-order key first
            for subindex in range(index, index + order):
                lst_key.append(data[subindex])
            ### get the key of value for n-order key: data[index + n]
            val = data[index + order]
            ### add this markov chain into the res
            ### note here I will just note value as frequency instead of prob
            res[tuple(lst_key)][val] += 1
            
    ### now I will convert previous frequencies to probs
    ### first parse each n-order markov subchain
    for key, value in res.items():
        ### as for the value I will first count total frequency
        total_freq = 0
        for outcome, frequency in value.items():
            total_freq += frequency
        ### now I will convert the frequency to probs by freq/total_freq
        for outcome, frequency in value.items():
            res[key][outcome] /= total_freq
    
    return res



### Stochastic choice
def stochastic(dictc):
    """
    Randomly predict the outcome given the probability given for each outcome
    
    inputs:
        - dict: a dictionary representing as {outcomeI : probabilityI}
    returns: one of the outcomeI randomly weightedly chosen
    """
    ### I will use res to store the candidate choices left each time
    res = []
    ### first I will put every choices in dict into res
    for choice in dictc:
        ### here I will check if two has the same probability of being chosen
        ### alr (false) => new prob   (true) => already exist
        alr = False
        for index in range(len(res)):
            ### if two have same probability of being chosen, choose one
            if choice == dictc[res[index]]:
                ran = random.uniform(0, 1)
                alr = True
                ### if ran is [0,0.5) replace existing  number
                if ran < 0.5:
                    res[index] = choice
                break
        ### if the prob not exists i will add new choice
        if not alr:
            res.append(choice)

    ### for all different probabilities of choice
    ### I will first set a thresold as [0,1)
    thresh = random.uniform(0, 1)
    
    ### then I will accumulate proabs for res until the accu is as least
    ### as big as thres
    accu = 0
    index = 0
    while accu < thresh and index < len(res):
        accu += dictc[res[index]]
        index += 1
        
    ### at the end since res only has one element, return the first element
    return res[index-1]

    
### Predict
def predict(model, last, num):
    """
    Predict the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    ### I will copy value num and last into temp variables
    tem_num = num
    tem_last = last.copy()

    ### I will use this list to store the result
    res = []
    ### for each while loop I will proceed one prediction
    while tem_num != 0:
        ### first store the tuple form of tem_last
        tup_last = tuple(tem_last)
        ### use variable to store the prediction outcome
        pre_otc = -1
        ### check if the markov chain is in the model
        if tup_last in model:
            ### if the current state is in the model
            ### access the value
            val = model[tup_last]
            ### return a state based on probability
            pre_otc = stochastic(val)
        else:
            ### if the current tate not in the model
            ### predict from 0 to 3 with equal probability
            ### in other words, all three states have equal chance
            pre_otc = stochastic({0:0.25, 1:0.25, 2:0.25, 3:0.25})
        ### delete the first element of tem_last and append pre_otc to last
        tem_last.pop(0)
        tem_last.append(pre_otc)
        ### add the pre_otc the res
        res.append(pre_otc)
        tem_num -= 1
    
    ### at the end return the res as the prediction
    return res

#print(markov_chain([1,2,3,0,1,2,1],4))

 

### Error
def mse(result, expected):
    """
    Calculate the mean squared error between two data sets.

    The length of the inputs, result and expected, must be the same.

    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    ### initiate a variable res as to store the square differences
    res = 0
    ### parse through every element index of expected and result
    for index in range(len(result)):
        ### get first element
        fst = result[index]
        ### get second element
        snd = expected[index]
        ### compute the different
        diff = fst - snd
        ### square the difference and add it to the result
        res += diff**2
    ### return the mean square erro
    return res / len(result)


### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    ### I will use res present the total mns error
    res = 0
    ### define an try_index to lable the number of trial
    try_index = 0
    while try_index != trials:
        ### at first I will need to train a markov modle using train data
        model = markov_chain(train, order)
        ### next I will make a prediction for future of days store it in pred
        pred = predict(model, test, future)
        ### next I will calculate the mns for this trial
        res += mse(pred, actual)
        ### trial index plus one
        try_index += 1
    
    ### at the end I will return the average mean square error for all trails
    return res / trials


### Application

def run():
    """
    Run application.

    You do not need to modify any code in this function.  You should
    feel free to look it over and understand it, though.
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Get stock data and process it

    # Training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    #   Comment these 2 lines out if you don't want to see the plots
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()

# You might want to comment out the call to run while you are
# developing your code.  Uncomment it when you are ready to run your
# code on the provided data.

#run()
