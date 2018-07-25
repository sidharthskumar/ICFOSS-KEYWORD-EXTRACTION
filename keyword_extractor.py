import scrap
from Tokenise import tokenise
from time import sleep
from POSTagging import POStagger
import sys
from POSTagging import split_tagged
from Features import feature_extraction
from Extraction import predict
from Extraction import extraction


link=sys.argv[1]
#link = "http://www.mathrubhumi.com/technology/telecom/-idea-cellular-and-vodafone-india-have-cleared-the-rs-7-268-crore-dues-to-the-dot-1.2998843"
ret = scrap.scrapper(link)
print(link)
sleep(1)
while ret:
    wordcount = tokenise.tokenizer()
    sleep(1)
    POStagger.postagger()
    sleep(1)
    split_tagged.splitTagged()
    sleep(1)
    dic = feature_extraction.featureExtractor(wordcount)
    sleep(1)
    predict.predict()
    sleep(1)
    extraction.extraction(dic)
    ret = 0



