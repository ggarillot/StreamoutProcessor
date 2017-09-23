#!/usr/bin/env python
import re
import sys

runPeriod = 'SPS_10_2015'
# runPeriod = 'SPS_06_2016'
# runPeriod = 'PS_06_2015'
runList = []

# jobid = sys.argv[2]
# fileName=jobs(jobid).outputdir+'stdout'
# fileName=jobs(jobid).backend.workdir+'/stdout'
logDir = '/eos/user/a/apingaul/CALICE/Data/%s/Logs' % runPeriod

for run in runList:
    fileName = '%s/streamLog_%d' % (logDir, run)
    try:
        file = open(fileName, "r")
        term = 'reconstructed'
        term = 'Hit in Bif'
        # term = 'failed'

        with open('test.txt', 'a') as outFile:
            for line in file:
                if re.search(term, line):
                    # outLine = str(jobs(jobid).id) + ' ' + jobs(jobid).name + ' ' + line
                    outLine = str(run) + ' ' + line
                    print outLine,
                    outFile.write(outLine)
                else:
                    outLine = str(run) + ' *** No final reconstructed event found ***'
    except IOError:
        with open('test.txt', 'a') as outFile:
            outLine = " No logFile for run '%d'\n" % run
            print outLine
            outFile.write(outLine)
