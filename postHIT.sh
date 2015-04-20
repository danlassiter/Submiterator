#!/usr/bin/env sh
pushd /Users/dan/aws-mturk-clt-1.3.1/bin
./loadHITs.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 -label /Users/dan/Dropbox/Experiments/Submiterator/tagalog -input /Users/dan/Dropbox/Experiments/Submiterator/tagalog.input -question /Users/dan/Dropbox/Experiments/Submiterator/tagalog.question -properties /Users/dan/Dropbox/Experiments/Submiterator/tagalog.properties -maxhits 1
popd