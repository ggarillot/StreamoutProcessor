#!/usr/bin/env python
"""
    Configuration module for Streamout Marlin processor
    Generate the xml file with data imported from external config file
export PYTHONPATH=/cvmfs/ganga.cern.ch/Ganga/install/6.3.0/python:${PYTHONPATH}
"""

from __future__ import print_function  # import print function from py3 if running py2.x
from __future__ import absolute_import

import os
import sys
import yapf

import time
import subprocess
import shlex  # split properly command line for Popen
from marlin import Marlin  # if error importing it move streamout.py to same folder
import yaml
try:
    import ganga
except ImportError:
    print("Ganga not found on system, won't run on grid")

# Import default config file
# Not needed here just for dumb editor not to complain about config not existing
import config_streamout as conf

sys.path.append(".")

# # -----------------------------------------------------------------------------
# def xmlValueBuilder(rootHandle, xmlHandleName, value, parameterType=None, option=None, optionValue=None, xmlParList=None):
#     ''' Generate Marlin compliant xml options
#     '''
#     xmlHandle = etree.SubElement(rootHandle, "parameter", name=xmlHandleName)
#     if parameterType is not None:
#         xmlHandle.set("type", parameterType)
#     if option is not None:
#         xmlHandle.set(option, optionValue)
#     xmlHandle.text = value
#     xmlParList[xmlHandleName] = value

# # -----------------------------------------------------------------------------
# def generateXML(inputFiles, outputFile, parList, xmlFile):
# ''' Generate xml file for Marlin ... Too specific for proper reusability even with yaml conf file
# '''
#     # generate XML
#     ## TAG: Execute
#     marlin = etree.Element('marlin')
#     execute = etree.SubElement(marlin, "execute")
#     for proc in conf.processorList:
#         processor = etree.SubElement(execute, "processor", name=proc[0])

#     ## TAG: Global
#     glob = etree.SubElement(marlin, "global")

#     # -- Processor Parameters
#     xmlValueBuilder(glob, "LCIOInputFiles", inputFiles, xmlParList=parList)
#     # --- Max number of evts to process
#     xmlValueBuilder(glob, "MaxRecordNumber", str(conf.maxEvt), xmlParList=parList)
#     # --- Number of evts to skip
#     xmlValueBuilder(glob, "SkipNEvents", str(conf.nSkipEvt), xmlParList=parList)
#     # --- Verbosity
#     xmlValueBuilder(glob, "Verbosity", conf.verbosity, option="options", optionValue="DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT", xmlParList=parList)

#     ## TAG: Processors
#     for proc in conf.processorList:
#         processor = etree.SubElement(marlin, "processor", name=proc[0])
#         processor.set("type", proc[1])

#         # --- Verbosity
#         xmlValueBuilder(processor, "Verbosity", conf.verbosity, parameterType="string", option="options", optionValue="DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT", xmlParList=parList)
#         xmlValueBuilder(processor, "InputCollectionName", conf.inputCollectionName, "string", "lcioInType", conf.inputCollectionType, xmlParList=parList)
#         xmlValueBuilder(processor, "OutputCollectionName", conf.outputCollectionName, "string", "lcioOutType", conf.inputCollectionType, xmlParList=parList)
#         xmlValueBuilder(processor, "LCIOOutputFile", outputFile + ".slcio", "string", xmlParList=parList)
#         xmlValueBuilder(processor, "ROOTOutputFile", outputFile + ".root", "string", xmlParList=parList)
#         xmlValueBuilder(processor, "PlotFolder", conf.plotPath, "string", xmlParList=parList)
#         # --- Byte shift for raw data reading
#         xmlValueBuilder(processor, "RU_SHIFT", str(conf.ruShift), "int", xmlParList=parList)
#         # --- XDAQ Byte shift for raw data reading
#         xmlValueBuilder(processor, "XDAQ_SHIFT", str(conf.xDaqShift), "int", xmlParList=parList)
#         xmlValueBuilder(processor, "CerenkovDifId", str(conf.cerenkovDifId), "int", xmlParList=parList)
#         # --- Drop first Trigger event (bool)
#         xmlValueBuilder(processor, "DropFirstRU", str(conf.dropRu), "bool", xmlParList=parList)
#         # --- Skip full Asic event (bool)
#         xmlValueBuilder(processor, "SkipFullAsic", str(conf.skipFullAsic), "bool", xmlParList=parList)
#         xmlValueBuilder(processor, "Before2016Data", str(conf.before2016Data), "bool", xmlParList=parList)
#         if conf.before2016Data is False:
#             xmlValueBuilder(processor, "TreatEcal", str(conf.treatEcal), "bool", xmlParList=parList)
#             # --- DetectorId for Ecal Data
#             xmlValueBuilder(processor, "EcalDetectorIds", str(conf.EcalDetectorIds), "std::vector<int>", xmlParList=parList)

#     # pretty string
#     s = etree.tostring(marlin, pretty_print=True)
#     with open(xmlFile, "w") as outFile:
#         outFile.write(s)


# -----------------------------------------------------------------------------
def findNumberOfFiles(folder, findString):
    ''' Return number of files associated with findString in folder
        If no file found print list of files in folder
    '''
    nFile = 0
    command_line = "ls %s" % folder
    args = shlex.split(command_line)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_list = proc.communicate()[0].split('\n')
    for line in stdout_list:
        if findString in line:
            nFile += 1
    if nFile == 0:
        print("\n[{0}] - File Not found, available files: ".format(os.path.basename(__file__)))
        for line in stdout_list:
            print("\t{0}".format(line))
    return nFile


# -----------------------------------------------------------------------------
def listFiles(fileNumber, runNumber, fileName, filePath):
    ''' Return the list of files found associated with runNumber
    '''
    fileList = []
    for iFile in range(0, fileNumber):
        fileList.append(fileName.format(filePath, runNumber, iFile))

#    inFiles = '\n'.join(fileList)
    print(
        '[{0}] - Found {1} raw slcio files for run {2} : \n{3}'.format(
            os.path.basename(__file__), fileNumber, runNumber, fileList
        )
    )
    return fileList


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
        return "[{0}] - RunNumber '{1}' is from TestBeam '{2}', you selected '{3}' in configFile '{4}'".format(
            os.path.basename(__file__), runNumber, goodPeriod, conf.runPeriod, configFile
        )

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
def scp(runNumber, serverName, serverPath, localPath):
    ''' Download file from serverName:serverPath to localPath
    '''
    print(
        "[{0}] - Downloading run '{1}' from {2}:{3}".format(
            os.path.basename(__file__), runNumber, serverName, serverPath
        )
    )
    scpPath = serverName + serverPath
    subprocess.check_call(['scp', scpPath, localPath])  # , env=dict(os.environ))


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
    fileNum = None
    configFile = "config_streamout"  # Default config file if none is given on cli

    # --- Parse CLI arguments
    if len(sys.argv) > 1:
        # --- Load configuration File
        configFile = sys.argv[1]
        try:
            exec ("import {0} as conf".format(configFile))
        except (ImportError, SyntaxError):
            sys.exit("[{0}] - Cannot import config file '{1}'".format(scriptName, configFile))
        # --- /Load configuration File
        if len(sys.argv) > 2:
            # --- Load runList
            runListArg = sys.argv[2]
            if len(sys.argv) > 3:
                # --- Load number of streamoutFile to process
                fileNum = int(sys.argv[3])
    elif conf.runList:  # runNumber configured in configFile
        runList = conf.runList
        print("[{0}] : Running with configuration file '{1}' on runs '{2}'".format(scriptName, configFile, runList))
    else:
        sys.exit(
            "Please give : configFile - runNumber(s)(optional if set up in configFile) - Number of streamout file to process(optional)"
        )

    # --- /Parse CLI arguments

    # --- Load List of runs
    if runListArg is None:  # if no runs on CLI, load list from configFile
        try:
            runList = conf.runList
        except AttributeError:
            sys.exit("[{0}] - No runs specified at command line or in configFile...exiting".format(scriptName))
    else:
        runList = runListArg.split(',')
    # --- /Load List of runs

    # For grid run, define a dictionary of generated configFile and associated inputFiles for each run

    for run in runList:
        # Check if runNumber match given period in configFile
        checkPeriod(str(run), conf.runPeriod, configFile)
        runNumber = int(run)
        #   List number of files to streamout (raw data are split in 2Go files with
        #   format DHCAL_runNumber_I0_fileNumber.slcio )
        #   TODO Remove Hardcoding here
        stringToFind = 'DHCAL_{0}_I0_'.format(runNumber)
        print(
            "[{0}] - Looking for files to streamout for run '{1}' in '{2}'... ".format(
                scriptName, runNumber, conf.inputPath
            ), end=""
        )
        if os.path.exists(conf.inputPath) is False:
            sys.exit("\n[{0}] - Folder '{1}' does not exist...exiting".format(scriptName, conf.inputPath))

        fileNumber = findNumberOfFiles(conf.inputPath, stringToFind)
        if fileNumber == 0:
            doScp = raw_input(
                "[{0}] - No file found...download it from '{1}' ? (y/n)".format(scriptName, conf.serverName)
            )
            if doScp == 'y':
                try:
                    scp(runNumber, conf.serverName, conf.serverPath, conf.inputPath)
                except:
                    raise ("[{0}] - Something wrong happened while downloading with scp".format(scriptName))
            # else :
            # sys.exit('Exiting')
        print('OK')

        # Check if more/less files available than asked by the user
        if fileNum is not None:
            if fileNum != fileNumber:
                ans = raw_input(
                    '\n\t [{}] - *** WARNING! *** Found {} files for run {}, you asked to process {}. Proceed? (y/n)\n'.
                    format(scriptName, fileNumber, runNumber, fileNum)
                )
                if ans == 'y':
                    fileNumber = fileNum
                else:
                    sys.exit('Exiting')

        # List of inputfiles for current run, reused for grid importation
        inputDataFileList = (listFiles(fileNumber, runNumber, conf.inputFile, conf.inputPath))
        conf.glob.LCIOInputFiles = ' '.join(inputDataFileList)
        outputFile = conf.outputFile.format(conf.outputPath, runNumber)
        conf.streamoutProc.LCIOOutputFile = outputFile + ".slcio"
        conf.streamoutProc.ROOTOutputFile = outputFile + ".root"

        print("[{0}] - output file : {1}.slcio".format(scriptName, outputFile))
        print("[{0}] - MARLIN_DLL: {1}".format(scriptName, conf.marlinLib))

        if os.path.exists("{0}.slcio".format(outputFile)) is True:
            sys.exit(
                "[{0}] - OutputFile already present : Delete or move it before running again...exiting".
                format(scriptName)
            )
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
            print("\n[{0}] ========================".format(scriptName))
            print('[{0}] --- Running Marlin...'.format(scriptName))
            print("[{0}] --- Ouput is logged to '{1}'".format(scriptName, log))
            beginTime = time.time()
            if conf.logToFile is True:
                subprocess.call(['python', 'run_marlin.py', marlinCfgFile], stdout=log, stderr=log)
            else:
                subprocess.call(['python', 'run_marlin.py', marlinCfgFile])

            print('[{0}] - Running Marlin...OK - '.format(scriptName), end='')
            try:
                elapsedTime(beginTime)
            except ValueError:
                print("Can't print time...")
            print("[{0}] ========================\n".format(scriptName))

            # print ('[{0}] - Removing xmlFile...'.format(scriptName), end='')
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

###
            try:
                print("[{0}] --- Submiting Job ... ".format(scriptName))
                # Navigate jobtree, if folder doesn't exist create it
                treePath = conf.runPeriod + '/' + scriptName[:-3]  # Remove .py at end of scriptName
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
                print('inputFiles:\n', inputFiles)

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

                # Save job as txtFile locally
                # export(jobs(j.id), 'my_job.txt')

                jobtree.add(j)
                # queues.add(j.submit)
                j.submit()
                print("\n[{0}] ... submitting job done.\n".format(scriptName))

            except:
                print("[{0}] --- Failed to submit job ".format(scriptName))
                raise


###

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
