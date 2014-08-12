Submiterator 2.0, August 12, 2014

Dan Lassiter
Department of Linguistics, Stanford University
http://web.stanford.edu/~danlass/
Email: 'dan' followed by 'lassiter', then the at sign, and finally 'stanford.edu'.

Summary:

Submiterator is a Python script intended to streamline the process of posting external HITs to Amazon Mechanical Turk (MTurk) for Mac and other Unix users. (No Windows support, sorry!) Basically the problem is this: you have an experiment written in beautiful HTML/JavaScript/CSS, which collects data on a participant's local machine as the experiment progresses. You've posted it on a public website, and you'd like to use MTurk to recruit participants and possibly also to aggregate their data. Amazon has the capability to create an "External HIT" which will display your website inside a frame in the user's MTurk interface. But, incredibly, Amazon does not have a web interface for the apparently simple task of posting external HITs: you have to write and modify a bunch of inscrutable bash scripts to make it happen. Submiterator relieves you of this burden, making the process much simpler and more efficient.

Using this kind of External HIT for your experiment has a number of benefits. It's much more flexible than the limited surveys you can create using Amazon's web interface, and it's more reliable and comfortable for Turkers than using a code-based system, where they go to an external website and then return to Amazon with a code when they are finished. (Apparently Turkers don't like this, maybe because it's annoying and error-prone.) You don't need to maintain a server beyond whatever you're using for your personal or academic website.  

Submiterator needs to be supplemented by a tool which does something with the data that you've collected in a JavaScript object during the experiment. You _could_ post the results back to a server. But there's a much easier way: you can have the user's machine submit their data to MTurk along with the other information that they pass with the 'HIT completed' signal. Submiterator comes with a template which shows how to do this in a simple way using Long Ouyang's JavaScript tool mmturkey. It also comes with a sample for converting into a .csv the aggregate results that Amazon sends back to you (when you run the 'getResults.sh' file).

Please contact with questions, comments, requests for additional functionality, etc. at the email address above.

To use Submiterator:

	1) Make sure you have Amazon's Command Line Tools installed (http://aws.amazon.com/developertools/694), have a Mechanical Turk requester account (http://www.requester.mturk.com), and are signed up for Amazon Web Services. It's crucial to modify your the mturk.properties file in the /bin/ folder of your installation to include your AWS-assigned access key and secret key. If you don't know these, go to http://s3.amazonaws.com/mturk/tools/pages/aws-access-identifiers/aws-identifier.html to get them.

	2) Make sure you have a working website implementing your experiment. Note that your website will display correctly in the MTurk window ONLY IF it can display securely. I've coded Submiterator so that, if the URL you provide does not begin with 'https', it will abort. You could modify this, but then you'll have to look into hacks for getting browsers to display mixed secure and non-secure content (see http://stackoverflow.com/questions/19801682/why-does-the-mturk-sandbox-only-display-my-hits-in-internet-explorer). 

	3) You'll need a method for passing the data collected on the Turker's local machine to MTurk (or some other way to get the data from them to you). As mentioned above, I recommend Long Ouyang's helpful tool mmturkey (https://github.com/longouyang/mmturkey). This is what is used in the accompanying experimental template.

	3) Make a folder containing a copy of Submiterator and the 'readme.txt' file that you'll tailor for this experiment. Important: once you've chosen a location for this script, don't move it or rename any folders along this path.

	4) Fill in the values specific to your experiment below and follow the other instructions to post your experiment as a HIT. Use the Sandbox to test it before going live (instructions below).

DETAILS:

Each line in your 'settings.txt' file is either a comment (beginning with "#") or a key-value pair, where keys and values are separated by "::". Go through this file and set the values to what you want for your experiment. (Don't modify any of the keys!) Submiterator will ignore lines that don't contain a "::", since they don't have a relevant key-value pair. If you want to add a comment to this file for your own use, mark it out with a "#".

Once you've set all of the experimental parameters described below, find the folder with these files in it and then type

> python submiterator.py
> sh postHIT.sh

If everything's been done correctly you'll get a message confirming that your HIT has been posted and giving you an address to see it. [This requires Java, so you may be required to set your JAVA_HOME environment variable: “export JAVA_HOME=…”.] If you're using the Sandbox, go ahead and do your own HIT so you can check the output. 

Once your experiment is running, monitor it using 
	https://requestersandbox.mturk.com/mturk/manageHITs
or
	https://requester.mturk.com/mturk/manageHITs
depending on whether it's sandbox or a live HIT.

Once you have some results in, you can download them as a .csv using the web interface, or else type

> sh getResults.sh

to download them as a JSON file. [This is the type of file that the 'parseJSON.py' file included with Submiterator can be modified to work with.]

When you're ready to approve work, you can do this on the website. If you have a lot of results and want to approve them all at once, you can do this by running

> sh approveAllResults.sh

Individual descriptions of the parameters you'll need to set:

	1. experimentURL: The URL where you've posted your experiment. This should begin with 'https:'.
	2. local configuration variables
		a. locationofCLT: The full absolute path to your installation of Amazon's Command Line Tools. Should not begin with '~/'. To find this path, use your terminal to navigate to the CLT installation and type 'pwd'.
		b. nameofexperimentfiles: this will be used locally to name some files that Submiterator creates and manipulates. I recommend making this name informative, so that you can easily identify which files attach to which experiment.
	3. Experimental parameters & participant filtering
		a. liveHIT: if 'yes' then, when you run the 'postHIT.sh' script, you will post a real HIT to MTurk for the world to see (assuming you have enough money in your account, etc.). If 'no', you'll post a Sandbox HIT, for testing and debugging. The default is 'no'. 
		b. numberofparticipants: how many participants do you want? You can always add more using the web interface, or expire your HIT early if you decide you don't want as many as you originally thought.
		c. reward: in dollars. E.g., if you want to pay 40 cents, enter '.40'.
		d. USonly?: if 'yes', only Turkers with a US IP address will be able to do your HIT.
		e. minPercentPreviousHITsApproved: a number between 0 and 100, or "none" if you don't want to place any restrictions here. Only workers who have had at least that percentage of previous HITs they've submitted subsequently approved by the assigner will be able to do your HIT. I think 85-95 is a frequently used threshold. This is a trade-off: too high and no one will be able to do your HIT; too low and you'll get bots and other low quality data.
	4. Advertising and display: control how Turkers will find and see your experiment.
		a. title: the title of the HIT, which is the first thing potential participants will see when deciding whether to consider doing the HIT.
		b. description: a brief 1-2 sentence description of the HIT. Make it catchy!
		c. keywords: 3-5 keywords, such as 'survey, experiment, ...'. Including interesting and descriptive keywords will make it more likely that people will find and take your experiment.
		d. frameheight: The height of the embedded frame that your subjects will see your experiment inside, in pixels. 500-700 is frequently a good value for me. When setting this, think about the smallest screen size you can expect your workers to have. Play with this parameter by posting several times to the sandbox with different settings and seeing which works for your specific experiment for a given screen size. 
		e. assignmentduration: in minutes. Make sure it's not such a short time that your participants will have difficult completing the task. E.g., if you think it will take 10 minutes on average you might enter '30'.
		f. hitlifetime: in hours. Your HIT will expire when this timer runs out or when you have all of the participants you've asked for, whichever comes first.
		g. autoapprovaldelay: in hours. If you haven't made any accept/reject decisions by this amount of time after posting all work will be automatically accepted. 

Your workers will want to have their work approved as soon as possible after they've completed the HIT. Once you've looked at the data, you should go on the requester site and choose which HITs to approve and reject. You can reject people if they're obviously screwing around, e.g. if they give the same answer to every question, but if everyone seems to have made a good-faith effort you can just approve everything by clicking "All" under "Approve" on leftmost column, and then making sure to submit this at the bottom of the page. 

Questions or comments on Submiterator and associated documentation? Email me (address at top of this file).











