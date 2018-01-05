=======================================================

1. How did I create the datasets ?

********
Step 1: I downloaded the urls for all the articles in the webpage - http://www.cnn.com/US/archive/

Step 2: I stored them in a text file "links.txt" in home folder "helloProject". 
Step 1 and 2 are handled by script file "cnn_spider.py" stored in folder "helloProject/helloProject/Spiders/"

********
Step 3: Then, I created a script "pages_spider.py" to navigate through all urls (stored in links.txt) and download the content body using Scrappy request. Here, I used Scrapy selector.xpath('//p/text()') so that only texts are downloaded instead of entire html file. After that, I only consider alphabetical words with atleast 3 alphabets using a regrex [a-zA-Z]{3,}

The script "pages_spider.py" can be found in folder "helloProject/helloProject/Spiders"
Each downloaded article is stored as article-"article_header".txt in folder "Articles/"

=========================================================

2. How did I create the data matrix ?

Step 1: Read each file from "Articles/*.txt" and do the following:

	1.1 Store article headers in a list "articleList". For future references, the index of this list would be utilized for each article header. 
	1.2 Filter out unimportant words such as:

'its' , 'have' , 'can' , 'were' ,'are' , 'all' , 'Sat' , 'just' , 'like' , 'he' , 'her' , 'him' , 'from' , 'from' ,'one' , 'will' ,'his' , 'Sans' , 'said' , 'that' , 'who' , 'contributed' ,'cnn', 'cable' , 'Network' , 'Reserved' , 'CNN' ,'Updated' , 'unfold' , 'preference' , 'Set' , 'unfolds' , 'network' , 'News', 'Cable' , 'unfolds.', 'preference:' ,'is' ,'as' ,'with' , 'Find', 'out', 'happening', 'world', 'world', 'ET,', 'Chat', 'Facebook', 'Messenger' , 'Messenger.' , 'world', '2015','unfolds.', 'Rights', 'Reserved.' ,'edition', 'preference:' , 'edition', 'it' , 'a' , 'are', 'an' , 'The' , 'has' , 'the' ,  'on' , 'A' , 'which' , 'under' , 'to' , 'you', 'provided', 'All' , 'this' , 'u' , 'us' , 'of' , 'was' , 'Mr.' , 'y' , 'Find', 'out', 'what', 'happening', 'world', 'world', 'ET,', 'Chat', 'Facebook', 'Messenger' , 'Messenger.' , 'world', '2015','unfolds.' , 'Rights', 'Reserved.' ,'edition', 'preference:' , 'edition', 'it' , 'a' , 'are', 'an' , 'The' , 'has' , 'for' , 'in' , 'the' , 'is' , 'on' , 'A' , 'which' , 'under' , 'to' , 'you', 'provided', 'All' , 'this' , 'u' , 'us' , 'of' , 'and' , 'was' , 'or' , 'y']


	1.3 Store all the remaining words (from all the articles) in a list "wordList".  WordList also contains the duplicate words. 
	1.4 Store the frequency of each word in a list "tempWordFreqForAllArticles"

Step 2: Sort both lists "wordList" and "tempWordFreqForAllArticles" in decreasing order of the frequency of word

Step 3: Get top K (for example:  100 ) most frequent words and store the unique words in a list "consolidatedWordList" and 
		their frequencies in a list "consolidatedWordFreqList". Finally, write all 100 "word-frequency" pair in a file 
		"wordFreqInAllArticles.txt"


Step 2: Create a data matrix of size (number of articles) X (K unique most frequent words)

Step 3: For each articleId in range(len(articleList))
			
			3.1 : count the frequency of each word from the consolidatedWordList in the given article and store in a temporary list 
			"wordFreqList"

			3.2: Store the word frequency to the corresponding word (column) for the given article in data matrix i.e
				 articleWordMatrix[articleId][wordId] = wordFreq[wordId]

==================================================================

3. How do I compute the similarity between each pair of articles with Euclidean distance ?








