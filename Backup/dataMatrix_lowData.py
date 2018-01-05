import os
import glob
import operator
from math import*
 


path = 'Articles3/'
print "Hello"

filterList = ['whose' ,'New' , 'played'  ,'January' , 'February', 'March', 'April', 'May', 'June', 'July' , 'August', 'September' , 'October' , 'November' , 'December','Photos' ,'Whose' , 'had' ,'according','Dow', 'She', 'after' ,'known', 'age' , 'its' , 'have' , 'can' , 'were' ,'are' , 'all' , 'Sat' , 'just' , 'like' , 'he' , 'her' , 'him' , 'from' , 'from' ,'one' , 'will' ,'his' , 'Sans' , 'said' , 'that' , 'who' , 'contributed' ,'cnn', 'cable' , 'Network' , 'Reserved' , 'CNN' ,'Updated' , 'unfold' , 'preference' , 'Set' , 'unfolds' , 'network' , 'News', 'Cable' , 'unfolds.', 'preference:' ,'is' ,'as' ,'with' , 'Find', 'out', 'happening', 'world', 'world', 'ET,', 'Chat', 'Facebook', 'Messenger' , 'Messenger.' , 'world', '2015','unfolds.', 'Rights', 'Reserved.' ,'edition', 'preference:' , 'edition', 'it' , 'a' , 'are', 'an' , 'The' , 'has' , 'the' ,  'on' , 'A' , 'which' , 'under' , 'to' , 'you', 'provided', 'All' , 'this' , 'u' , 'us' , 'of' , 'was' , 'Mr.' , 'y' , 'Find', 'out', 'what', 'happening', 'world', 'world', 'ET,', 'Chat', 'Facebook', 'Messenger' , 'Messenger.' , 'world', '2015','unfolds.' , 'Rights', 'Reserved.' ,'edition', 'preference:' , 'edition', 'it' , 'a' , 'are', 'an' , 'The' , 'has' , 'for' , 'in' , 'the' , 'is' , 'on' , 'A' , 'which' , 'under' , 'to' , 'you', 'provided', 'All' , 'this' , 'u' , 'us' , 'of' , 'and' , 'was' , 'or' , 'y']


wordList = [] #It stores all the words in all articles (even duplicate ones)
consolidatedWordList = [] #It stores only the unique words
wordFreqList = [] #It contains the frequency of each word

articleList = [] #contains all the article names

#similarity Matrices
euclideanSimilarityMatrix = []
tempWordFreqForAllArticles = []
topKWordList = []
topKWordFreqList = []


def convertListToCleanString(inputList):
	inputListStr = str(inputList)
	inputListStr = inputListStr.replace("," , " ")
	inputListStr = inputListStr.replace("[" , " ")
	inputListStr = inputListStr.replace("]" , " ")

	#print ("The list is " + str(inputList) + "\n")
	#print ("String is " + inputListStr + "\n")
	return inputListStr

def sortArticlesInDecreasingOrderOfFreq():
	for i in range(len(tempWordFreqForAllArticles) - 1, 0, -1):
		for j in range(i):
			if tempWordFreqForAllArticles[j] < tempWordFreqForAllArticles[j+1]:
				tempFreq = tempWordFreqForAllArticles[j]
				tempWordFreqForAllArticles[j] = tempWordFreqForAllArticles[j+1]
				tempWordFreqForAllArticles[j+1] = tempFreq

				tempWord = wordList[j]
				wordList[j] = wordList[j+1]
				wordList[j+1] = tempWord


def partition(array, begin, end):
    pivot = begin
    for i in xrange(begin+1, end+1):
        if array[i] <= array[begin]:
            pivot += 1
            array[i], array[pivot] = array[pivot], array[i]
    array[pivot], array[begin] = array[begin], array[pivot]
    return pivot


def quicksort(array, begin=0, end=None):
    if end is None:
        end = len(array) - 1
    if begin >= end:
        return
    pivot = partition(array, begin, end)
    quicksort(array, begin, pivot-1)
    quicksort(array, pivot+1, end)

def topKfeatureSelection(reqNoOccurences):
	for wordId in range(len(wordList)):
		if tempWordFreqForAllArticles[wordId] > reqNoOccurences:
			topKWordList.append(wordList[wordId])
			topKWordFreqList.append(tempWordFreqForAllArticles[wordId])
	
	print ("List: " + str(topKWordList) + "\n")
	print ("Freq: " + str(topKWordFreqList) + "\n")
	print len(topKWordList)


#Get the complete row (word frequency for each column) for given particular article (data)
def getWordCountForEachArticle(data):
	#print data
	curArticleWordList = []
	curwordFreqList = []
	for word in (str(data)).split():
		if word not in filterList:
			curArticleWordList.append(word)
			#print word

	#print("Current Article Word List \n"  + str(curArticleWordList) + "\n")
	for w in consolidatedWordList:
		curwordFreqList.append(curArticleWordList.count(w))
	return curwordFreqList


def euclidean_similarity(article1, article2):
	euclideanDist = sqrt(sum(pow(a-b, 2) for a, b in zip(article1, article2)))
	#convert to similarity
	result = 1/( 1 + euclideanDist)
	print ("Euclidean similarity " + str(result))
	return result

def square_rooted(x):
	return round(sqrt(sum([a*a for a in x])),3)

def cosine_similarity(article1,article2):
	numerator = sum(a*b for a,b in zip(article1,article2))
	denominator = square_rooted(article1)*square_rooted(article2)
	if denominator == 0 :
		result = float('inf')
	else:
		result = round(numerator/float(denominator),3)
	print ("Cosine similarity " + str(result))
	return result

def jaccard_similarity(article1,article2):
	intersection_cardinality = len(set.intersection(*[set(article1), set(article2)]))
	union_cardinality = len(set.union(*[set(article1), set(article2)]))
	result = intersection_cardinality/float(union_cardinality)
	print ("Jaccard similarity " + str(result))
	return result


# MAIN FUNCTION

fileCount = 1
#iterate over all articles
for infile in glob.glob( os.path.join(path, '*.txt') ):
	print str(fileCount) + " current file is: " + infile
	fileCount += 1
	#Store the article names
	articleList.append(infile)
	f = open(infile)  
	for word in f.read().split():
		# filter out unwanted words
		if word not in filterList:
			wordList.append(word)
			tempWordFreqForAllArticles.append(wordList.count(word))
	f.close()

print "Total words in All Files: " + str(len(wordList)) +" \n"
print "================== Feature Selection ==================="
#NOTE: required number of occurences
#topKfeatureSelection(10)

sortArticlesInDecreasingOrderOfFreq()
#quicksort(tempWordFreqForAllArticles)

consolidatedWordFreqList = []
countFreqWords = 0

Output2Str = ""

#Get consolidated list of 100 most frequent unique words
for word in wordList:
	if countFreqWords >= 20:
		break
	#countWords = countWords + 1
	if word not in consolidatedWordList:
		consolidatedWordList.append(word)
		consolidatedWordFreqList.append(wordList.count(word))
		countFreqWords += 1

		Output2Str += str(wordList.count(word)) + "  "


topKWordsStr= convertListToCleanString(consolidatedWordList) 
#print ("Word List " + topKWordsStr)
#Output2 top 100 most frequent words in following file
with open("Output2/wordFreqInAllArticles.txt", 'w') as f: 
	f.write("Words " + topKWordsStr + "\n")
	f.write("'20 Most Frequent Words' " + Output2Str)

#print ("List: " + str(consolidatedWordList) + "\n")
#print ("Freq: " + str(consolidatedWordFreqList) + "\n")

print ("Length of article list: " + str(len(articleList)) + "\n")
print ("Number of Unique words: "  + str(len(consolidatedWordList)) + "\n")

#create a data matrix of size (numberofArticles X noOfUniqueWords)
articleWordMatrix = [[0 for uniqueWord in range(len(consolidatedWordList))] for article in range(len(articleList))] 
print("Size of data matrix   : " + str(len(articleWordMatrix)) + " - " + str(len(articleWordMatrix[0])))


# Write all words in a file
with open("Output2/article_word_freq.txt", 'w') as f: 
	f.write("SN " + "  " + topKWordsStr +"\n")
	consolidatedWordFreqListStr = convertListToCleanString(consolidatedWordFreqList)
	f.write("All " + "  " + consolidatedWordFreqListStr +"\n")

#for each article in articleList:
for articleId in range(len(articleList)):
	#read each article again
	with open (articleList[articleId], "r") as myfile:
		data=myfile.readlines()	

	#get the frequency of each word in the given article
	wordFreqList = getWordCountForEachArticle(data)

	#write the word freq of top K words in a file for each article
	with open("Output2/article_word_freq.txt", 'a') as f:
		wordFreqListStr = convertListToCleanString(wordFreqList)
		f.write(str(articleId) + "  " + wordFreqListStr + "  " + articleList[articleId] + "\n")

	#NOTE:	  articleList - row for the articleWordMatrix 
	#consolidatedWordList - column for the articleWordMatrix
	# 		 wordFreqList - value of each cell of the articleWordMatrix

	#insert each element of word Freq to each column of following matrix in row number - article Id
	for wordId in range(len(wordFreqList)):
		articleWordMatrix[articleId][wordId] = wordFreqList[wordId]
	#print articleId


### Calculate euclidean similarity matrix
euclideanSimilarityMatrix = [[0 for articleId in range(len(articleWordMatrix))] for articleId in range(len(articleWordMatrix))] 
print ("Size of Similarity Matrix: " + str(len(euclideanSimilarityMatrix)) + " - " + str(len(euclideanSimilarityMatrix[0])))

dictEuclid = {}
dictCosine = {}
dictJaccard = {}

for articleId_1 in range(len(articleWordMatrix)):
		#euclideanSimilarityMatrix.append([])		
		for articleId_2 in range(len(articleWordMatrix)):
			if articleId_1 != articleId_2:
				print ("==================================================\n\n")

				print ("Column: " + str(consolidatedWordList) + "\n") 
				print ("Article 1: " + str(articleWordMatrix[articleId_1]) + "\n")
				print ("Article 2: " + str(articleWordMatrix[articleId_2])  + "\n")
				print (" Similarity between : "  + str(articleId_1) + "  " + str(articleId_2))

				euclidSim = euclidean_similarity(articleWordMatrix[articleId_1] , articleWordMatrix[articleId_2])
				euclidSim = float("{0:.5f}".format(euclidSim))
				dictEuclid[euclidSim] = str(articleId_1) + " " + str(articleId_2)

				cosineSim = cosine_similarity(articleWordMatrix[articleId_1] , articleWordMatrix[articleId_2])
				cosineSim = float("{0:.5f}".format(cosineSim))
				dictCosine[cosineSim] = str(articleId_1) + " " + str(articleId_2)

				jaccardSim = jaccard_similarity(articleWordMatrix[articleId_1] , articleWordMatrix[articleId_2])
				jaccardSim = float("{0:.5f}".format(jaccardSim))
				dictJaccard[jaccardSim] = str(articleId_1) + " " + str(articleId_2)

				print ("\n\n==================================================\n")

#print dictEuclid

euclidOutput2Str = ""
cosineOutput2Str = ""
jaccardOutput2Str = ""


print "\nSorted Euclidean Similarity"
for key in reversed(sorted(dictEuclid)):
	articlePair = dictEuclid[key].split()
	euclidOutput2Str += str(key) + " " + str(articlePair[0]) + " " + str(articlePair[1]) + " \n "
    #print "%s: %s" % (key, dictEuclid[key])

with open("Output2/euclidSimilarity.txt", 'w') as f: 
	f.write(euclidOutput2Str)

print "\nSorted Cosine Similarity"
for key in sorted(dictCosine):
	cosineOutput2Str += str(key) + " " + dictCosine[key] + " \n "
    #print "%s: %s" % (key, dictCosine[key])

with open("Output2/cosineSimilarity.txt", 'w') as f: 
	f.write(cosineOutput2Str)


print "\nSorted Jaccard Similarity"
for key in sorted(dictJaccard):
	jaccardOutput2Str += str(key) + " " + dictJaccard[key] + " \n "
    #print "%s: %s" % (key, dictJaccard[key])

with open("Output2/jaccardSimilarity.txt", 'w') as f: 
	f.write(jaccardOutput2Str)

#write in a file the most correlated and least correlated article pairs

#simF = open("Output2/pairWiseSimilarity.txt", 'w')

print ("================== Eucliean Similarity =========================== \n")
lineArray = []
with open("Output2/euclidSimilarity.txt", 'r') as f:
	lineArray = f.readlines()

mostSimilar = (lineArray[0]).split()
print "Most Similar: " + str(mostSimilar)+ " \n"

with open("Output2/euclidean_most_"+str(mostSimilar[0])+".txt" ,'w') as f:
	for colIndex in range(len(articleWordMatrix[0])):
		Output2Str = str(consolidatedWordList[colIndex])+ " "+ str(articleWordMatrix[int(mostSimilar[1])][colIndex]) +" "+ str(articleWordMatrix[int(mostSimilar[2])][colIndex])+ "\n"
		f.write(Output2Str)

leastSimilar = (lineArray[len(lineArray) - 2]).split()
print "Least Similar: " + str(leastSimilar)+ " \n"

with open("Output2/euclidean_least_"+str(leastSimilar[0])+".txt" ,'w') as f:
	for colIndex in range(len(articleWordMatrix[0])):
		Output2Str = str(consolidatedWordList[colIndex])+ " "+ str(articleWordMatrix[int(leastSimilar[1])][colIndex]) +" "+ str(articleWordMatrix[int(leastSimilar[2])][colIndex])+ "\n"
		f.write(Output2Str)


print ("================== Cosine Similarity =========================== \n")

with open("Output2/cosineSimilarity.txt", 'r') as f:
	lineArray = f.readlines()

mostSimilar = (lineArray[0]).split()
print "Most Similar: " + str(mostSimilar)+ " \n"

with open("Output2/cosine_most_"+str(mostSimilar[0])+".txt" ,'w') as f:
	for colIndex in range(len(articleWordMatrix[0])):
		Output2Str = str(consolidatedWordList[colIndex])+ " "+ str(articleWordMatrix[int(mostSimilar[1])][colIndex]) +" "+ str(articleWordMatrix[int(mostSimilar[2])][colIndex])+ "\n"
		f.write(Output2Str)

leastSimilar = (lineArray[len(lineArray) - 2]).split()
print "Least Similar: " + str(leastSimilar)+ " \n"

with open("Output2/cosine_least_"+str(leastSimilar[0])+".txt" ,'w') as f:
	for colIndex in range(len(articleWordMatrix[0])):
		Output2Str = str(consolidatedWordList[colIndex])+ " "+ str(articleWordMatrix[int(leastSimilar[1])][colIndex]) +" "+ str(articleWordMatrix[int(leastSimilar[2])][colIndex])+ "\n"
		f.write(Output2Str)


print ("================== Jaccard Similarity =========================== \n")
with open("Output2/jaccardSimilarity.txt", 'r') as f:
	lineArray = f.readlines()

mostSimilar = (lineArray[0]).split()
print "Most Similar: " + str(mostSimilar)+ " \n"

with open("Output2/jaccard_most_"+str(mostSimilar[0])+".txt" ,'w') as f:
	for colIndex in range(len(articleWordMatrix[0])):
		Output2Str = str(consolidatedWordList[colIndex])+ " "+ str(articleWordMatrix[int(mostSimilar[1])][colIndex]) +" "+ str(articleWordMatrix[int(mostSimilar[2])][colIndex])+ "\n"
		f.write(Output2Str)

leastSimilar = (lineArray[len(lineArray) - 2]).split()
print "Least Similar: " + str(leastSimilar)+ " \n"

with open("Output2/jaccard_least_"+str(leastSimilar[0])+".txt" ,'w') as f:
	for colIndex in range(len(articleWordMatrix[0])):
		Output2Str = str(consolidatedWordList[colIndex])+ " "+ str(articleWordMatrix[int(leastSimilar[1])][colIndex]) +" "+ str(articleWordMatrix[int(leastSimilar[2])][colIndex])+ "\n"
		f.write(Output2Str)

#leastSimilar = (linesArray[len(linesArray) - 1]).split()
#print "Least Similar: " + str(leastSimilar) + "\n"



	# values = (str(line)).split()
	# if len(values) > 0:
	# 	article1 = articleWordMatrix[int(values[1])]
	# 	article2 = articleWordMatrix[int(values[2])]
	# 	print str(article1)
		#print "Line : " + str(values[0]) + " " + str(values[1]) +" " + str(values[2]) +" \n" 




# def similarityBasedOnEuclideanDistance():
# 	#print(" Size of data matrix is " + str(len(articleWordMatrix)) + " - " + str(len(articleWordMatrix[0])))

# 	#create a similarity matrix with size (articleId X articleId)
# 	euclideanSimilarityMatrix = [[0 for articleId in range(len(articleWordMatrix))] for articleId in range(len(articleWordMatrix))] 
# 	print ("Size of Similarity Matrix: " + str(len(euclideanSimilarityMatrix)) + " - " + str(len(euclideanSimilarityMatrix[0])))

# 	#Calculate the euclidean distance for a pair of rows (articleId)
# 	#Then save the final result to the similarity matrix as an element for the given pair of rows

# 	#NOTE: similarity value is only stored in [0][1] but not in [1][0] and so on

# 	for articleId_1 in range(len(articleWordMatrix)):
# 		#euclideanSimilarityMatrix.append([])
		
# 		for articleId_2 in range(len(articleWordMatrix)):
# 			euclideanDistance = 0
# 			for wordId in range(len(articleWordMatrix[0])):
# 				euclideanDistance += math.pow((articleWordMatrix[articleId_1][wordId] - articleWordMatrix[articleId_2][wordId]),2) 
			
# 			#if articleId_1 == articleId_2:
# 			print ("Here " + str(articleId_1)+ " - " + str(articleId_2) +" " + str(euclideanDistance))
			
# 			euclideanDistance  = math.sqrt(euclideanDistance)
# 			euclideanSimilarityMatrix[articleId_1][articleId_2] = euclideanDistance
			

# 	for row in range(len(euclideanSimilarityMatrix)):
# 		for column in range(len(euclideanSimilarityMatrix)):
# 			print (str(row) + " - " + str(column) + " " + str(euclideanSimilarityMatrix[row][column]))
# 	return

