# ADM-HW4
[#4 Homework](https://github.com/CriMenghini/ADM-2018/tree/master/Homework_4) of [ADM](http://aris.me/index.php/data-mining-ds-2018) within the MSc in [Data Science](http://datascience.i3s.uniroma1.it/it) @ La Sapienza University

## Flow
1. Scraping the website through BautifulSoup (generator)
2. Scraper on a server
3. Merge results and build the two TSV datasets 
4. K-Mean clustering through sklearn linked module (No ++)
5. Elbow method to study the best no. of clusters 
6. Get top-3 for each of them 
7. Compare the overall results 
8. Compare the top-3 of each dataset
9. [...]

1. Proceed with the definition of two hash functions (one takes into account the 
2. ~~HashTable has to be defined as a python class (dictionary style)~~
3. *Iterate in parallel (multiprocessing as we do not need any memory sharing)
4. Find 10M duplicates
5. Check collisions probabilities 

* shared memory hashtable required!

## Datasets
20k items were scraped from the website 
[information-dataset.tsv](https://drive.google.com/file/d/1Byqz5YcD5-FESIq0Yi7HDlTqlxkCVbC6/view?usp=sharing)
[description-dataset-with-header.tsv](https://drive.google.com/file/d/1gb0pZrwiPuo_AIrHX58qSKi20JS3ss6q/view?usp=sharing)

Datasets have to be extracted using [pbzip2](https://launchpad.net/pbzip2/+download) or [bzip](http://www.bzip.org/). 
