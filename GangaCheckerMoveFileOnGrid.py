#!/usr/bin/env python
from Ganga.Utility.GridShell import getShell
from Ganga.Core.exceptions import ProtectedAttributeError
import time


def fileExists(f, fName):
    cmd = 'lcg-ls --vo {} lfn:{}'.format(f.credential_requirements.vo, fName)
    # print 'lsCmd: ', cmd
    (exitcode, output, m) = getShell(f.credential_requirements).cmd1(cmd, capture_stderr=True)
    if exitcode == 0:  # File exists
        return True
    elif 'No such file or directory' in output:
        return False
    else:
        f.failureReason += " The file can't be uploaded because of lsCmd output : {}".format(output)
        return True


def makeGridAlias(f, fName):
    cmd = 'lcg-aa --vo {} {} lfn:{}'.format(f.credential_requirements.vo, f.locations, fName)
    # print 'aliasCmd: ', cmd
    (exitcode, output, m) = getShell(f.credential_requirements).cmd1(cmd, capture_stderr=True)
    if exitcode != 0:
        f.failureReason += " The file can't be uploaded because of {}".format(output)
    return exitcode, output


def check(j):
    ''' postProcessor for gangaJob. Used to move file to their proper location on the grid
        They go by default to /grid/calice/generated/date/file-SomeRandomNumber
        Function takes the guid of the file, make an alias (lcg-aa) to its proper location
        on the grid
    '''
    outputFiles = [file for file in j.outputfiles]
    good = True
    for f in outputFiles:
        fName = '/grid/{}/{}{}'.format(f.credential_requirements.vo, f.se_rpath, f.namePattern)
        # print 'fName: ', fName
        if fileExists(f, fName):
            fName += time.strftime("-%Y-%m-%d_%H-%M-%S")
        rc, output = makeGridAlias(f, fName)
        if rc != 0:
            good = False
    return good
