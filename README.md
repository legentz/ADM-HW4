## The datasets created was done by the scrapping house announcements in Rome from Immobiliare.it 

## Using Scraper.py libriary
The Scraper.py attached was used to parse the hmtl to obtain our datasets on information which consists of announcements, price, locali, baqgni and piano and the description dataset which contains words on used for the  annoucements. This contained the Beautiful Soup library

## Clustering on the Information Dataset 
Our dataset was of length 20013 hence we implemented the MiniBatchKmeans algorithm to perform the clustersing and using the Elbow Method choose th]e optimal number of clusters, k. 
In order to achieve the above, we dropped annoucement to base our focus on the other variables in the dataset.
we then converted the dataset into matrix. Since the variables varies, we normalized them using the MinMaxScaler from the sklearn module to get the values in range from 0 and 1. 
Before achieving the above, we cleaned up the dataset since we came to a realization that piano contained the string types. We therefore 
replaced the ground floor, T with 0
the half floor, R we replace it with 0.5
the loft, A as 11
the basement, S with -1
and 11+ as 12.
We also cleaned out locali and bagni to removed the + signs.

## The wordcloud 
This was structured using the wordcloud module. The dataset was first preprocessed using the utils.py library as attached to the repository.


