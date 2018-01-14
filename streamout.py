#!/usr/bin/env python
"""
    Configuration module for Marlin processor
    export PYTHONPATH=/cvmfs/ganga.cern.ch/Ganga/install/LATEST/python:${PYTHONPATH}
"""

from __future__ import print_function  # import print function from py3 if running py2.x
from __future__ import absolute_import

import os
import sys
import time
import subprocess

from marlin import Marlin
import yaml
try:
    import Ganga
except ImportError:
    print("Ganga not found on system, won't run on grid")

sys.path.append(".")


# -----------------------------------------------------------------------------
    '''



# -----------------------------------------------------------------------------
def elapsedTime(startTime):
    ''' Print time to finish job
    '''
    t_sec = round(time.time() - startTime)
    (t_min, t_sec) = divmod(t_sec, 60)
    (t_hour, t_min) = divmod(t_min, 60)
    print('Time passed: {:.0f} hour {:.0f} min {:.0f} sec'.format(t_hour, t_min, t_sec))


# -----------------------------------------------------------------------------
def checkPeriod(runNumber, runPeriod, configFile):
    ''' Check runNumber is associated to correct runPeriod
        Abort execution if not
    '''
    def periodError(goodPeriod):
        return "[{}] - RunNumber '{}' is from TestBeam '{}', you selected '{}' in configFile '{}'".format(
            os.path.basename(__file__), runNumber, goodPeriod, conf.runPeriod, configFile)

    if runNumber < '726177' and (runPeriod != 'SPS_08_2012' or runPeriod != 'SPS_11_2012'):
        sys.exit(periodError('SPS_08_2012 or SPS_11_2012'))

    if runNumber >= '726177' and runNumber <= '726414' and runPeriod != 'SPS_12_2014':
        sys.exit(periodError('SPS_12_2014'))

    if runNumber >= '727760' and runNumber <= '728456' and runPeriod != 'SPS_04_2015':
        sys.exit(periodError('SPS_04_2015'))

    if runNumber >= '728501' and runNumber <= '728682' and runPeriod != 'PS_06_2015':
        sys.exit(periodError('PS_06_2015'))

    if runNumber >= '730436' and runNumber <= '730926' and runPeriod != 'SPS_10_2015':
        sys.exit(periodError('SPS_10_2015'))

    if runNumber >= '730927' and runNumber <= '732909' and runPeriod != 'SPS_06_2016':
        sys.exit(periodError('SPS_06_2016'))

    if runNumber >= '733626' and runNumber <= '733759' and runPeriod != 'SPS_10_2016':
        sys.exit(periodError('SPS_10_2016'))

    if runNumber >= '736500' and runNumber <= '736575' and runPeriod != 'SPS_09_2017':
        sys.exit(periodError('SPS_09_2017'))


# -----------------------------------------------------------------------------
def scp(runNumber, fName, serverName, serverPath, localPath):
    ''' Download file from serverName:serverPath to localPath
    '''
    print(
        "[{}] - Downloading run '{}' from {}:{}".format(
            os.path.basename(__file__), runNumber, serverName, serverPath
        )
    )
    fName.format(runNumber)
    scpPath = serverName + ":" + serverPath + fName.format(runNumber)
    print(scpPath)
    try:
        subprocess.check_call(['scp', scpPath, localPath])
    except subprocess.CalledProcessError:
        sys.exit("[{}] - Something wrong happened while downloading with scp: return code".format(
            os.path.basename(__file__)))


# -----------------------------------------------------------------------------
def createJob(executable, args=[], name='', comment='', backend='Local', backendCE='', voms=''):
    ''' Create Ganga job. Default backend is Local
    '''
    j = Job()
    j.application = Executable(exe=File(executable), args=args)
    j.name = name
    j.comment = comment

    j.backend = backend
    if backend == 'CREAM':
        j.backend.CE = backendCE
        try:
            gridProxy.voms = voms
        except NameError:  # ganga > 6.3 no longer has the gridProxy credentials system
            print("using new cred system")
            # j.backend.credential_requirements = VomsProxy(vo=voms)
    return j


# -----------------------------------------------------------------------------
def setCliOptions(marlin, xmlSection):
    ''' properly set cliOptions from configfile for marlin.py
    '''
    sectionName = xmlSection.name + "."
    for param, value in vars(xmlSection).items():
        if param != 'name':
            marlin.setCliOption(sectionName + param, value)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def main():
    '''
    '''
    scriptName = os.path.basename(__file__)  # For logging clarity

    runNumber = None
    runListArg = None
    configFile = "configFile"  # Default config file if none is given on cli

    # --- Parse CLI arguments
    if len(sys.argv) > 1:
        # --- Load configuration File
        configFile = sys.argv[1]
        try:
            exec("import {0} as conf".format(configFile))
        except (ImportError, SyntaxError):
            sys.exit("[{}] - Cannot import config file '{}'".format(scriptName, configFile))
        # --- /Load configuration File
        if len(sys.argv) > 2:
            # --- Load runList
            runListArg = sys.argv[2]

    elif conf.runList:  # runNumber configured in configFile
        runList = conf.runList
        print("[{}] : Running with configuration file '{}' on runs '{}'".format(scriptName, configFile, runList))
    else:
        sys.exit("Please give : configFile - runNumber(s)(optional if set up in configFile)")
    # --- /Parse CLI arguments

    # --- Load List of runs
    if runListArg is None:  # if no runs on CLI, load list from configFile
        try:
            runList = conf.runList
        except AttributeError:
            sys.exit("[{}] - No runs specified at command line or in configFile...exiting".format(scriptName))
    else:
        runList = runListArg.split(',')
    # --- /Load List of runs

    # For grid run, define a dictionary of generated configFile and associated inputFiles for each run

    for run in runList:
        # Check if runNumber match given period in configFile
        checkPeriod(str(run), conf.runPeriod, configFile)
        runNumber = int(run)
        #   Create list of files to run on
        if conf.runOnGrid is False:
            print("[{}] - Looking for files to process for run '{}' in '{}'... ".format(scriptName, runNumber, conf.inputPath))
            if os.path.exists(conf.inputPath) is False:
                sys.exit("\n[{}] - Folder '{}' does not exist...exiting".format(scriptName, conf.inputPath))

            inputDataFileList = [f for f in os.listdir(conf.inputPath) if str(runNumber) in f]
            if not inputDataFileList:
                doScp = raw_input("[{}] - No file found...download it from '{}' ? (y/n)".format(scriptName, conf.serverName))
                if doScp == 'y':
                    scp(runNumber, conf.inputFile, conf.serverName, conf.serverDataPath, conf.inputPath)
                else:
                    sys.exit('Exiting')

        if conf.runOnGrid is False:
            outputFile = conf.outputPath + conf.outputFile.format(runNumber)
            marlinLib = conf.processorPath + 'lib/' + conf.marlinLib
            inputDataFileList = [conf.inputPath + f for f in inputDataFileList]
        conf.glob.LCIOInputFiles = ' '.join(inputDataFileList)
        outputFile = conf.outputFile.format(conf.outputPath, runNumber)
        conf.streamoutProc.LCIOOutputFile = outputFile + ".slcio"
        conf.streamoutProc.ROOTOutputFile = outputFile + ".root"

        if conf.runOnGrid is False:
            print("[{}] - output file : {}.slcio".format(scriptName, outputFile))
            print("[{}] - MARLIN_DLL: {}".format(scriptName, marlinLib))

            if os.path.exists("{0}.slcio".format(outputFile)) is True:
                sys.exit("[{}] - OutputFile already present : Delete or move it before running again...exiting".format(
                    scriptName))


        # Printing modification to xml file
        print("\n[{0}] ========================".format(scriptName))
        print("[{0}] --- Dumping modified xml parameters: ".format(scriptName))
        for par, value in vars(conf.glob).items():
            if par != 'name':
                print("[{0}] \t\t{1}:\t{2}".format(scriptName, par, value))
        for par, value in vars(conf.streamoutProc).items():
            if par != 'name':
                print("[{0}] \t\t{1}:\t{2}".format(scriptName, par, value))
        print("[{0}] ========================\n".format(scriptName))

        # Marlin configuration
        marlinCfgFile = conf.marlinCfgFile.format(runNumber)
        marlin = Marlin()
        marlin.setXMLConfig(conf.xmlFile)
        marlin.setLibraries(conf.marlinLib)
        marlin.setILCSoftScript(conf.initILCSoftScript)
        setCliOptions(marlin, conf.glob)  # TODO: Move to Marlin.py
        setCliOptions(marlin, conf.streamoutProc)
        marlin.writeConfigFile(marlinCfgFile)

        # Running locally
        if conf.runOnGrid is False:
            log = open(conf.logFile.format(conf.logPath, runNumber), "w", 1)  # line-buffered
            print("\n[{}] ========================".format(scriptName))
            print('[{}] --- Running Marlin...'.format(scriptName))
            print("[{}] --- Output is logged to '{}'".format(scriptName, log))
            beginTime = time.time()
            if conf.logToFile is True:
                subprocess.call(['python', 'run_marlin.py', marlinCfgFile], stdout=log, stderr=log)
            else:
                subprocess.call(['python', 'run_marlin.py', marlinCfgFile])

            print('[{}] - Running Marlin...OK - '.format(scriptName), end='')
            try:
                elapsedTime(beginTime)
            except ValueError:
                print("Can't print time...")
            print("[{}] ========================\n".format(scriptName))

            # print ('[{}] - Removing xmlFile...'.format(scriptName), end='')
            # subprocess.Popen(["rm", xmlFile])

        # Add gridInfo to Marlin configuration file + make Dic
        else:
            with open(marlinCfgFile, 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
            gridSection = {}
            cfg['Grid'] = gridSection
            gridSection['downloader'] = conf.gridDownloader
            gridSection['uploader'] = conf.gridUploader
            gridSection['LCG_CATALOG_TYPE'] = conf.LCG_CATALOG_TYPE
            gridSection['LFC_HOST'] = conf.LFC_HOST
            gridSection['inputFiles'] = conf.gridInputFiles
            with open(marlinCfgFile, 'w') as ymlfile:
                ymlfile.write(yaml.dump(cfg, default_flow_style=False))

            try:
                print("[{}] --- Submiting Job ... ".format(scriptName))
                # Navigate jobtree, if folder doesn't exist create it
                treePath = conf.runPeriod + '/' + scriptName[:-3]  # Remove .py at end of scriptName
                # print("[{}] --- treePath: {}".format(scriptName, treePath))
                # if jobtree.exists(treePath) is False: # Always returns true...
                jobtree.cd('/')  # make sure we are in root folder
                try:
                    jobtree.cd(treePath)
                except TreeError:
                    try:
                        jobtree.mkdir(treePath)
                    except:  # mkdir should write all missing folder if any....apparently not true
                        print("WhatThe?")
                        jobtree.mkdir(conf.runPeriod)
                        jobtree.mkdir(treePath)
                    jobtree.cd(treePath)

                eos_installation = '/afs/cern.ch/project/eos/installation/user/'
                eos_home = '/eos/user/a/apingaul/CALICE/'

                # Update ganga configuration for eos access
                config.Output.MassStorageFile['defaultProtocol'] = 'root://eosuser.cern.ch'
                config.Output.MassStorageFile['uploadOptions']['cp_cmd'] = eos_installation + 'bin/eos.select cp'
                config.Output.MassStorageFile['uploadOptions']['ls_cmd'] = eos_installation + 'bin/eos.select ls'
                config.Output.MassStorageFile['uploadOptions']['mkdir_cmd'] = eos_installation + 'bin/eos.select mkdir'
                config.Output.MassStorageFile['uploadOptions']['path'] = eos_home
                # Print it
                print(config.Output.MassStorageFile['defaultProtocol'])
                print(config.Output.MassStorageFile['uploadOptions']['cp_cmd'])
                print(config.Output.MassStorageFile['uploadOptions']['ls_cmd'])
                print(config.Output.MassStorageFile['uploadOptions']['mkdir_cmd'])
                print(config.Output.MassStorageFile['uploadOptions']['path'])

                inputFiles = []
                for f in conf.gridInputFiles:
                    inputFiles.append(LocalFile(f))
                inputFiles.append(LocalFile(marlinCfgFile))
                # print('inputFiles:\n', inputFiles)

                inputData = []
                for item in [inputDataFileList]:
                    l = []
                    print("\nitem=", item, "\n")
                    for f in item:
                        l.append(MassStorageFile(f))
                    print("\nl=", l, "\n")
                    for f in l:
                        print("\nf=", f, "\n")

                inputData = GangaDataset(treat_as_inputfiles=False, files=[f for f in l])

                print('\n\ninputDataType:\n', type(inputData))
                print('\n\ninputData:\n', inputData)
                for item in inputData:
                    print(type(item))
                    print(item)

                j = createJob(
                    executable='run_marlin.py', args=[marlinCfgFile], name=str(runNumber), backend=conf.backend,
                    backendCE=conf.CE, voms=conf.voms
                )
                # j = createJob(executable='runStreamout.sh', args=[marlinCfgFile], name=str(runNumber), backend=conf.backend, backendCE=conf.CE, voms=conf.voms)
                j.comment = "Streamout " + conf.runPeriod
                j.outputfiles = [
                    MassStorageFile(namePattern="*.*", outputfilenameformat='GridOutput/Streamout/{jid}/{fname}')
                ]
                j.inputfiles = inputFiles
                j.inputdata = inputData

                jobtree.add(j)
                # queues.add(j.submit)
                j.submit()

                print("\n[{}] ... submitting job done.\n".format(scriptName))

            except IncompleteJobSubmissionError:
                sys.exit("[{}] --- Failed to submit job ".format(scriptName))


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
