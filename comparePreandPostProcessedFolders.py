import os
import shutil
post = os.listdir(r'X:\imagery\GEM_SAR_WINDS\2017')

pre = os.listdir(r'X:\imagery\SAR2_2017')

print pre
print post


unprocessed = [x for x in pre if x not in post]
print unprocessed
print len(pre),len(post), len(unprocessed)

file = open ('UnprocessedSARImagery2017.txt','w')

for x in unprocessed:
    file.write(x+'\n')

file.close()

print post