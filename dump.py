#!/usr/bin/env python

import subprocess
import os

runPeriod = 'SPS_10_2015'
# runPeriod='SPS_06_2016'
# runPeriod='SPS_10_2016'
# runPeriod='SPS_12_2014'

runList = []

filePath = '/eos/user/a/apingaul/CALICE/Data/%s/Streamout' % runPeriod
namePattern = '%s/DHCAL_%i_SO_Antoine.slcio'

for i, j in runList:
    name = namePattern % (filePath, i)
    print name
    print j
    cmd = os.environ['LCIO'] + "/bin/dumpevent " + str(name) + " " + str(j) + " | head -n 4"
    print cmd
    os.system(cmd)  # ,stdout=subprocess.PIPE)
    # print subprocess.call(['head','-n',str(5)], stdin=p1.stdout)
