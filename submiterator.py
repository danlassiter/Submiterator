settings = open("experiment-settings.txt", 'r')
lines = settings.readlines()
settings.close()
dict={}
for line in lines:
    if not (line == "\n" or line == ""):
        while (line[0] == "\n" or line[0] == "\t" or line[0] == " "):
            line = line[1:]
        if not (line[0:3] == "&&&"):
            x=line.split("::")
            key = x[0]
            possvalues = x[1].split("&&&")
            value = possvalues[0]
            while (key[0] == "\n" or key[0] == "\t" or key[0] == " "):
                key = key[1:]
            while (key[-1] == "\n" or key[-1] == "\t" or key[-1] == " "):
                key = key[:-1]
            while (value[0] == "\n" or value[0] == "\t" or value[0] == " "):
                value = value[1:]
            while (value[-1] == "\n" or value[-1] == "\t" or value[-1] == " "):
                value = value[:-1]
            dict[x[0]] = value

# write the .question file, which tells MTurk where to find your external HIT.
question = open(dict["nameofexperimentfiles"] + ".question", 'w')
question.write("<?xml version='1.0'?><ExternalQuestion xmlns='http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd'><ExternalURL>" + dict["experimentURL"] + "</ExternalURL><FrameHeight>"+ dict["frameheight"] +"</FrameHeight></ExternalQuestion>")
question.close()

#write the .properties file.
properties = open(dict["nameofexperimentfiles"] + ".properties", 'w')
properties.write("title: " + dict["title"] + "\ndescription: " + dict["description"] + "\nkeywords: " + dict["keywords"] + "\nreward: " + dict["reward"] + "\nassignments: " + dict["numberofassignments"] + "\nannotation: ${condition}\nassignmentduration:" + dict["assignmentduration"] + "\nhitlifetime:" + dict["hitlifetime"] + "\nautoapprovaldelay:" + dict["autoapprovaldelay"])
if (dict["USonly?"] == "y" or dict["USonly?"] == "Y" or dict["USonly?"] == "yes" or dict["USonly?"] == "Yes" or dict["USonly?"] == "true" or dict["USonly?"] == "True" or dict["USonly?"] == "T" or dict["USonly?"] == "1"):
    properties.write("\nqualification.1:00000000000000000071\nqualification.comparator.1:EqualTo\nqualification.locale.1:US\nqualification.private.1:false")
if (dict["minPercentPreviousHITsApproved"] != "none"):
    properties.write("\nqualification.2:000000000000000000L0\nqualification.comparator.2:GreaterThanOrEqualTo\nqualification.value.2:" + dict["minPercentPreviousHITsApproved"] + "\nqualification.private.2:false")
properties.close()

#write the .input file. "conditions::" in the file experiment-settings.txt can be followed by any number of condition names, separated by a comma.
input = open(dict["nameofexperimentfiles"] + ".input", 'w')
input.write("condition\n")
num = 1
conditions = dict["conditions"]
conditionlist = conditions.split(",")
for x in conditionlist:
    input.write(str(num) + " " + x + " \n")
    num = num + 1
input.close()

#write the bash script for posting the HITs.
posthits = open(dict["nameofexperimentfiles"] + "-postHIT.sh", 'w')
posthits.write("#!/usr/bin/env sh\npushd " + dict["locationofCLT"] + "/bin\n./loadHITs.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 -label " + dict["hitfolderpath"] + "/" + dict["nameofexperimentfiles"] + " -input " + dict["hitfolderpath"] + "/" + dict["nameofexperimentfiles"] + ".input -question " + dict["hitfolderpath"] + "/" + dict["nameofexperimentfiles"] + ".question -properties " + dict["hitfolderpath"] + "/" + dict["nameofexperimentfiles"] + ".properties -maxhits 1\npopd")
posthits.close()

#write the bash script for getting results from MTurk
getResults = open(dict["nameofexperimentfiles"] + "-getResults.sh", 'w')
getResults.write("#!/usr/bin/env sh\npushd " + dict["locationofCLT"] + "/bin\n./getResults.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 -successfile " + dict["hitfolderpath"] + "/" + dict["nameofexperimentfiles"] + ".success -outputfile " + dict["hitfolderpath"] + "/" + dict["nameofexperimentfiles"] + ".results\npopd")
getResults.close()
