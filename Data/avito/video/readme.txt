
This scripts are for parsing avito site

Common workflow:

1) Scrap data from the site:
search_download.py

This should generate the parsed items list:
search.csv

2) If you don't have the gpulist.csv file
or you want to renew it then download the 
gpu1.html
gpu2.html
...
files from 
https://www.videocardbenchmark.net

links to the lists are:
High End
High Mid Range
Low Mid Range
Low End

Than launch the gpu list parser:
parse_gpulist.py

This should generate parsed gpu list:
gpulist.csv

3) Try to find any of the items 
obtained in step 1 in the parsed 
gpulist.csv

To do so execute:
merge_search.py

This will generate the results:
recognized.csv

and
unknown.csv

4) Try to recognize items from the unknown.csv list
by obtaining more information

Then merge new data with the recognized.csv list

To do so run
merge_unknown.py

Results: 
recognized.csv updated
unknown.csv with new data (full description and so on)



