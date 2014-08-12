# This file is a template for converting the JSON file that MTurk will return to you into a .csv which you can import into R, Excel, etc. Here we're operating on the assumption that you're using mmturkey (https://github.com/longouyang/mmturkey) or some comparable process in your JavaScript to communicate results to MTurk.
 
# Note that this script might need further modification, depending on how you recorded your data. If you follow the instructions below in encoding your data in the JavaScript, or use the sample experimental template provided with Submiterator, you can get away with just filling in a few values.

# This code assumes that what was submitted to MTurk was a JavaScript object (dictionary) where each trial was encoded as a separate object (dictionary), like so:

# data = {
#     q1: {
#         ...
#     },
#     q2: {
#         ...
#     },
#     ...,
#     q20: {
#     ...
#     }
# } 

# If you know a but of Python you could easily modify this to take the case where your data is stored in an array, but it's probably easier to just change your JavaScript code to follow this format.

# MTurk will return a JSON with one line per participant, with 'workerid', Answer.q1', 'Answer.q2', etc. in the header line. The goal is to converr this into a .csv file with one line per trial, where each trial is labeled with all relevant information about the participant (workerid, demographic, etc) as well as all of the data recorded in the trial.

# Add to the bySubjectVariables list any information which appears 1x per participant that you want access to in data analysis. One item in this list should always be 'workerid'.
# Values recorded trial-by-trial should not be named in bySubjectVariables, since they will automatically be added to the byTrialVariables list when the individual trial reulsts are parsed. (It's critical here that exactly the same variables are recorded in each trial. Add dummy variables with NAs in your JavaScript if your experiment isn't set up like this.)

filename = "NAME_OF_YOUR_RESULTS_FILE"
bySubjectVariables = ['workerid', 'Answer.language'] 

import re

fl=open(filename, 'r')
lines = fl.readlines()
fl.close()

processedlines = [line.split('\"\t\"') for line in lines]
processed = [[re.sub('[\n\"{}]', '', x) for x in line] for line in processedlines]
header = processed[0]
data = processed[1:]

def find_idx (string):
    vals = [i for i,x in enumerate(header) if x == string]
    if len(vals) == 0:
        return -1
    else:
        return vals[0]

individualTrialNames = [x for x in header if x[:7] == 'Answer.' and x not in bySubjectVariables]
sampletrial = data[0][find_idx(individualTrialNames[0])]
sampletrial_parsed = [x.split(':') for x in sampletrial.split(',')]
byTrialVariables = [x[0] for x in sampletrial_parsed]

d = {}
counter=0
for subjectdata in data:     
    counter += 1   
    subjname = "subject" + str(counter)
    d[subjname] = {}
    trialnum = 0
    for trialname in individualTrialNames:
        trialnum += 1
        trialindex = find_idx(trialname)
        trialdataraw = {}
        keysAndValues = [x.split(":") for x in subjectdata[trialindex].split(",")]
        for keyValuePair in keysAndValues:
            trialdataraw[keyValuePair[0]] = keyValuePair[1]
        for item in bySubjectVariables:
            trialdataraw[item] = subjectdata[find_idx(item)]
        d[subjname][trialnum] = trialdataraw
        
csv=""
for x in bySubjectVariables + byTrialVariables:
    if x[:7] == 'Answer.':
        csv = csv + x[7:] + "," 
    else:   
        csv = csv + x + ","
csv = csv[:-1] + "\n"

for subj in d.keys():
    for trial in d[subj].keys():
        for v in bySubjectVariables + byTrialVariables:
            csv += d[subj][trial][v] + ","
        csv = csv[:-1] + "\n"    

parsed = open(filename + "-parsed.csv", 'w')
parsed.write(csv)
parsed.close()
