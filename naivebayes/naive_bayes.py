import argparse

words_count = {}            #Dictionary to store words and corresponding ham and spam occurence count
spam_count = 0
ham_count =0
unique_words = []           #Storing unique words
spam_word_count = 0
ham_word_count = 0
words_probability = {}
spam_prob =0.0
ham_prob = 0.0

#Method to calculate the frequency count of each word in spam and ham     
def train_data( wordSplit):
    global words_count
    global unique_words
    global spam_count
    global ham_count
    global total_word_count
    global ham_word_count
    global spam_word_count
    
    
    pos = 0                     #0 for ham 1 for spam in wordDict
    init_count = [0,0]          #default init for new word
    if wordSplit[1] == 'spam':
        pos =1
        spam_count+=1
    else:
        ham_count+=1
        
    word_count = 0   
    #Iterating over the words and its frequency count and updating the required spam or ham list
    for counter in  range(2, len(wordSplit), 2):
        word = wordSplit[counter]
        val = int(wordSplit[counter+1])
        if word not in unique_words:
            unique_words.append(word)
            words_count[word] = init_count
        words_count[word][pos] = words_count[word][pos] + val
        word_count+=val 
        
    if wordSplit[1] == 'spam':
        spam_word_count+= word_count
    else:
        ham_word_count+=word_count

#Method to calculate the probability of each word in the word dictionary. The alpha value passed is value for smoothing
def calculateProbability(alpha):
    global words_count
    global words_probability
    global spam_word_count
    global ham_word_count
    global unique_words
    
    #Applying laplacian smoothing
    divisor_spam = float(spam_word_count + alpha*len(unique_words))
    divisor_ham = float(ham_word_count + alpha*len(unique_words)) 
    for key in words_count.keys():
        ham_val, spam_val = words_count.get(key)
        ham_prob = float(ham_val+alpha)/divisor_ham
        spam_prob = float(spam_val+alpha)/divisor_spam
        words_probability[key] = [ham_prob,spam_prob]
        
#Method to caluclate the whether the test string is ham or spam        
def test_data(test_split):
    global spam_prob, ham_prob, words_probability
    prob_spam = 1.0
    prob_ham = 1.0
    for counter in range(2, len(test_split),2):
        word = test_split[counter]
        freq = int(test_split[counter+1])
        prob_ham *= freq*words_probability[word][0]         #Calculating ham probability of each word
        prob_spam *= freq*words_probability[word][1]        #Calculating spam probability of each word
    prob_ham *= ham_prob
    prob_spam *= spam_prob
    if prob_spam > prob_ham:
        return 'spam'
    else:
        return 'ham'
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', help='training file in csv format', required=True)
    parser.add_argument('-f2', help='test file in csv format', required=True)
    parser.add_argument('-o', help='output labels for the test dataset', required=True)
    args = vars(parser.parse_args())
    file_train = open(args["f1"], "r")
    for line in file_train:
        wordSplit = line.split()
        train_data(wordSplit)
    file_train.close()
    spam_prob = float(spam_count)/(spam_count+ham_count)    #Calculating Pr(spam)
    ham_prob = float(ham_count)/(spam_count+ham_count)      #Calculating Pr(ham)
    p=5
    calculateProbability(p)                                 #Calculating probability of each spam and ham word
    acc=0
    file_test = open(args["f2"], "r")
    file_out = open(args["o"],"w+")
    for line1 in file_test:
        test_split = line1.split()
        email_id = test_split[0]
        actual = test_split[1]
        pred = test_data(test_split) 
        if pred==actual:
            acc+=1
        file_out.write(email_id +" "+pred+"\n")
