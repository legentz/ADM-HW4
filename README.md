The datasets created was done by the scrapping house annpuncements in Rome from Immobiliare.it 

Using Scraper.py libriary which contains the Beautiful Soup library to parse the hmtl to obtain our datasets on information which consists of announcements, price, locali, baqgni and piano and the description dataset which contains words on used for the  annoucements. 

Clustering on the Information Dataset 
Our dataset was of length 20013 hence we implemented the MiniBatchKmeans algorithm to perform the clustersing and using the Elbow Method choose th]e optimal number of clusters, k. 
In order to achieve the above, we dropped annoucement to base our focus on the other variables in the dataset.
we then converted the dataset into matrix. Since the variables varies, we normalized them using the MinMaxScaler from the sklearn module to get the values in range from 0 and 1. 


The wordcloud was structured using the wordcloud module. The dataset was first preprocessed using the utils.py library as attached to the repository.


