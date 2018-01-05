import os
import glob
from math import*
 


path = 'Articles/'
print "Hello"

filterList = ["u'", "',", '\t' , '\r' , '\n', '[' , ']' , '"' , 'are', 'an' , 'The' , 'has' , 'for' , 'in' , 'the' , 'is' , 'on' , 'A' , 'which' , 'under' , 'to' , 'you', 'provided', 'All' , 'this' , 'u' , 'us' , 'of' , 'and' , 'was' , 'Mr.' , 'or' , 'y']


wordList = [] #It stores all the words in all articles (even duplicate ones)
consolidatedWordList = [] #It stores only the unique words
wordFreqList = [] #It contains the frequency of each word

articleList = [] #contains all the article names

#similarity Matrices
euclideanSimilarityMatrix = []


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

# MAIN FUNCTION

tempWordFreqForAllArticles = []
#iterate over all articles
for infile in glob.glob( os.path.join(path, '*.txt') ):
    print "current file is: " + infile
   #Store the article names
    articleList.append(infile)
    f = open(infile)  
    for word in f.read().split():
    	# filter out unwanted words
    	if word not in filterList:
    		wordList.append(word)
    		#countWords = countWords + 1
    		if word not in consolidatedWordList:
    			consolidatedWordList.append(word)
    f.close()


print ("Length of article list: " + str(len(articleList)))
print ("Number of Unique words: "  + str(len(consolidatedWordList)))

#create a data matrix of size (numberofArticles X noOfUniqueWords)
articleWordMatrix = [[0 for uniqueWord in range(len(consolidatedWordList))] for article in range(len(articleList))] 
print("Size of data matrix   : " + str(len(articleWordMatrix)) + " - " + str(len(articleWordMatrix[0])))

#for each article in articleList:
for articleId in range(len(articleList)):
	#read each article again
	with open (articleList[articleId], "r") as myfile:
		data=myfile.readlines()	

	#get the frequency of each word in the given article
	wordFreqList = getWordCountForEachArticle(data)

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

for articleId_1 in range(len(articleWordMatrix) - 170):
		#euclideanSimilarityMatrix.append([])		
		for articleId_2 in range(len(articleWordMatrix) - 170):
			if articleId_1 != articleId_2:
				print ("==================================================\n\n")
				print (" Similarity between : "  + str(articleId_1) + "  " + str(articleId_2))
				
				euclidean_similarity(articleWordMatrix[articleId_1] , articleWordMatrix[articleId_2])
				cosine_similarity(articleWordMatrix[articleId_1] , articleWordMatrix[articleId_2])
				jaccard_similarity(articleWordMatrix[articleId_1] , articleWordMatrix[articleId_2])

				print ("\n\n==================================================\n\n")



    #print("List \n" + str(consolidatedWordList) + "\n")
    # print("Freq \n" + str(wordFreq) + "\n")

    		#wordFreq.append(f.read().count(word))
    		#print(word)
    		#print f.read().count(word)
    # with open(infile,'r') as f:
    # 	for line in f:
    # 		wordList = line.split()

    #     	for word in wordList:
    #         	wordFreq.append(wordList.count(word))
    #         	print (word +" - " + str(wordFreq) + "\n")