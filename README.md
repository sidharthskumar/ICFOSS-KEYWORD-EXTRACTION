# ICFOSS-KeyWord-Extractor
#### This project was implemented as a part of the summer internship programme at ICFOSS, Thiruvananthapuram, under the guidance of Dr. Rajeev R R.
#### \*\*\*\*UPDATE******* RESEARCH PAPER PUBLISHED IN IEEE EXPLORE LINK- https://ieeexplore.ieee.org/document/8882999/

#### This project is an Automatic Keyword Extractor for Malayalam News Articles Using a CRF Model. 

### Program Modules

##### [keyword_extractor.py](/keyword_extractor.py) will run the entire system from start to end by accepting only the url as input.

1)Web scrapping: scrap.py accepts an url using which it will extract the main paragraphs from the corresponding webpage and write it to scrapped_text.txt inside Tokenize folder. This code has to be modified according to the arrangement of text in the chosen webpage.

2)Pre-processing: the scrapped text contains junk characters and english characters which must be removed. tokenise.py removes all unwanted characters but retains non_breaking prefixes like 'Dr.' 'Mr' etc. The cleaned text is then tokenized into words and stored in tokenized_text.txt inside POSTagging folder.

3)POS Tagging: A TnT Tagger was trained with over 70,000 thousand words annotated with the BIS Tagset to form a POS Tagger. POStagger.py tags the tokenized text which is again cleaned and split using split_tagged.py. The final tagged words are written to tagged_split.txt inside Features folder. postag.py will make use of the web based tagger developed by IITMK for POS tagging.

4)Feature Extraction: The following features are extracted from each word:-
    i)POS tag(POS)
   ii)Term frequency(TF) (word freq/max word freq)
  iii)Depth(DEP) (position of first occurence/total number of words)
   iv)Length(LEN) (word length/max word length)
   v)Presence in Heading(H)
   
  feature_extraction.py extracts the following features from each word in tagged_split.txt and writes the feature vectors to               features.txt. This dataset can be used for training after manual labelling of keywords, or can be fed into the CRF model to be           labelled automatically.
  
5)CRF model: The current CRF model has been trained with over 5000 words from about 50 news articles. predict.py will labell the feature vectors using the trained CRF model. For instructions on using CRF++ refer [CRF++ Taku Kudo](https://taku910.github.io/crfpp/)

6)Post-processing: extraction.py performs the post processing operations necessary to retrieve the keywords according to the labels generated by the CRF model. These keywords are prioritized on the basis of their POS tag and TF and only the top n keywords, where n = 20% of total number of words in the article, are chosen as the final keywords.

### Corpora
[Annotated corpus for training POS Taggger](/POSTagging/TnT/largest.txt)

[Dataset used for training CRF Model(2000 words)](/CRF/train.txt)

### General Instructions
   1)Remember to change all paths and path variables with respect to your local directories.
   
   2)Read the comments for instructions.
   
   3)Take care of the shell scripts used for TnT tagger and CRF++.
   
   4)While using keyword_extractor.py predict.sh and postag.sh must be in the same folder.
   
   5)URL is not recieved from standard input, the url variable has to be replaced for different urls(i got lazy :p )
   
   6)For enquiries contact sidharth.osr@gmail.com

### Web App
   Web App folder contains modifications to the general code of the system in order for the system to be used as a web based application    in a Flask environment.(Modifications under progress)
   
    MIT License


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

This permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

