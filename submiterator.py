import os

def trim(l):
    while l[0] in ['\t',' ','\n']:
        l = l[1:]
    while l[-1] in ['\t',' ','\n']:
        l = l[:-1]
    return l

hitfolderpath = os.getcwd()

settings = open("settings.txt", 'r')
lines = settings.readlines()
settings.close()
settings_dict={'conditions':'condition'}
for line in lines:
    if "::" in line: # ignore lines that don't have a key and value
        keyAndValue = trim(line).split("::")
        settings_dict[trim(keyAndValue[0])] = trim(keyAndValue[1].split("###")[0])

# convert hours (used in Submiterator) to seconds (used by AMT)
settings_dict['assignmentduration'] = str(int(settings_dict['assignmentduration']) * 60)
settings_dict['hitlifetime'] = str(int(settings_dict['hitlifetime']) * 3600)
settings_dict['autoapprovaldelay'] = str(int(settings_dict['autoapprovaldelay']) * 3600)

if not os.path.exists(settings_dict["locationofCLT"]) or settings_dict["locationofCLT"][-1] == '/':
    raise Exception("Error: check the 'locationofCLT' specification in your settings file.")

if not settings_dict["experimentURL"][:5] == "https":
    raise Exception("Error: Your HIT will not display properly to workers unless you use a secure connection. Please ensure that your URL begins with 'https'.")

old_properties_file = open(settings_dict["locationofCLT"] + "/bin/mturk.properties", 'r').readlines()
backup = open(settings_dict["locationofCLT"] + "/bin/mturk.properties.backup", 'w')
for line in old_properties_file:
    backup.write(line)
backup.close()
new_properties_file = open(settings_dict["locationofCLT"] + "/bin/mturk.properties", 'w')
if settings_dict["liveHIT"] == "yes":
    for line in old_properties_file:
        if "://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester" in line:
            new_properties_file.write("# service_url=https://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester\n")
        elif "://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester" in line:
             new_properties_file.write("service_url=https://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester\n")
        else:
            new_properties_file.write(line)
else:
    for line in old_properties_file:
        if "://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester" in line:
            new_properties_file.write("service_url=https://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester\n")
        elif "://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester" in line:
            new_properties_file.write("# service_url=https://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester\n")
        else:
            new_properties_file.write(line)
new_properties_file.close()

# write the .question file, which tells MTurk where to find your external HIT.
question = open(settings_dict["nameofexperimentfiles"] + ".question", 'w')
question.write("<?xml version='1.0'?><ExternalQuestion xmlns='http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd'><ExternalURL>" + settings_dict["experimentURL"] + "</ExternalURL><FrameHeight>"+ settings_dict["frameheight"] +"</FrameHeight></ExternalQuestion>")
question.close()

#write the .properties file.
properties = open(settings_dict["nameofexperimentfiles"] + ".properties", 'w')
properties.write("title: " + settings_dict["title"] + "\ndescription: " + settings_dict["description"] + "\nkeywords: " + settings_dict["keywords"] + "\nreward: " + settings_dict["reward"] + "\nassignments: " + settings_dict["numberofparticipants"] + "\nannotation: ${condition}\nassignmentduration:" + settings_dict["assignmentduration"] + "\nhitlifetime:" + settings_dict["hitlifetime"] + "\nautoapprovaldelay:" + settings_dict["autoapprovaldelay"])
if settings_dict["USonly?"] in ["y","Y","yes","Yes","true","True","T","1"]:
    properties.write("\nqualification.1:00000000000000000071\nqualification.comparator.1:EqualTo\nqualification.locale.1:US\nqualification.private.1:false")
if settings_dict["minPercentPreviousHITsApproved"] != "none":
    properties.write("\nqualification.2:000000000000000000L0\nqualification.comparator.2:GreaterThanOrEqualTo\nqualification.value.2:" + settings_dict["minPercentPreviousHITsApproved"] + "\nqualification.private.2:false")
properties.close()

#write the .input file. 
inputfile = open(settings_dict["nameofexperimentfiles"] + ".input", 'w')
inputfile.write("condition\n1 condition")
inputfile.close()

#write the bash script for posting the HITs.
posthits = open("postHIT.sh", 'w')
posthits.write("#!/usr/bin/env sh\npushd " + settings_dict["locationofCLT"] + "/bin\n./loadHITs.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 -label " + hitfolderpath + "/" + settings_dict["nameofexperimentfiles"] + " -input " + hitfolderpath + "/" + settings_dict["nameofexperimentfiles"] + ".input -question " + hitfolderpath + "/" + settings_dict["nameofexperimentfiles"] + ".question -properties " + hitfolderpath + "/" + settings_dict["nameofexperimentfiles"] + ".properties -maxhits 1\npopd")
posthits.close()

#write the bash script for getting results from MTurk
getResults = open("getResults.sh", 'w')
getResults.write("#!/usr/bin/env sh\npushd " + settings_dict["locationofCLT"] + "/bin\n./getResults.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 -successfile " + hitfolderpath + "/" + settings_dict["nameofexperimentfiles"] + ".success -outputfile " + hitfolderpath + "/" + settings_dict["nameofexperimentfiles"] + ".results\npopd")
getResults.close()

# write the bash script to approve all work submitted so far.
approveAll = open('approveAllResults.sh', 'w')
approveAll.write("#!/usr/bin/env sh\npushd " + settings_dict["locationofCLT"] + "/bin\n./approveWork.sh -successfile " + hitfolderpath + "/" + settings_dict["nameofexperimentfiles"] + ".success\npopd")
approveAll.close()