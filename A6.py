import threading
import time
import logging

#map function
def map_(thread, intermediate_results):
    for word in thread:
        #lowercase
        word = word.lower()
        #key value pairing
        intermediate_results.append((word, 1))

#reduce function
def reduce_(intermediate_results, result):
    word_counts = {}
    for word, count in intermediate_results:
        if word in word_counts:
            word_counts[word] += count #word already seen so add 1
        else:
            word_counts[word] = count #new word and set count to 1
    #append to results
    result.extend(word_counts.items())
   
def combine_(intermediate_results):
    comb = {}
    for word, count in intermediate_results:
        if word in comb:
            comb[word] += count #word already seen so add 1
        else:
            comb[word] = count #new word and set count to 1
    #append to results
    return comb.items()

#read the data
def readData(fileP, threadN):
    with open(fileP, "r") as file:
        data = file.read().split()
        
    #split the data to correct number of threads
    splitD = [data[i::threadN] for i in range(threadN)]
    return splitD

# Define data processing logic
def process(fileP, numthread):
    
    #read the data with correct number of threads
    data = readData(fileP, numthread)
    #initialize list to store each thread
    sepR = []

    #threads
    threads = [threading.Thread(target=map_, args=(threadN, sepR)) for threadN in data]

    #start threads
    for thread in threads:
        thread.start()

    #join threads
    for thread in threads:
        thread.join()

    #result list
    result = []

    #reduce the threads
    reduce_(sepR, result)
    
    #combine the threads
    combined_results = combine_(result)

    return combined_results

#Main function
def main():
    #read input data
    filePath = input("Enter file path: ")
    
    #define the thread count
    threadCount = input("Enter amount of threads: ")
    num_threads = int(threadCount)
    
    #time for single thread 
    start = time.time()
    singlethreaded = process(filePath, 1)
    singleTime = time.time() - start

    #time for multi thread
    start = time.time()
    multithreaded = process(filePath, num_threads)
    multiTime = time.time() - start

    #display results
    print("Single thread execution time:", singleTime)
    print("Multithread execution time:", multiTime)
    print("Word count (Singlethreaded):")
    for word, count in singlethreaded:
        print(f"{word}: {count}")
    print("Word count (Multithreaded):")
    for word, count in singlethreaded:
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
