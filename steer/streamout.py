"""
    Configuration module for Streamout Marlin processor
    Generate the xml file with data imported from external config file
"""

from __future__ import print_function # import print function from py3 if running py2.x

import os
import sys
import time
import subprocess
import shlex # split properly command line for Popen
# from lxml import etree

# Import default config file
# Not needed here just for dumb editor not to complain about config not existing
import config_streamout as config
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
        print ("\n[{0}] - File Not found, available files: ".format(os.path.basename(__file__)))
        for line in stdout_list:
            print ("\t{0}".format(line))
    return nFile


# -----------------------------------------------------------------------------
def listFiles(fileNumber, runNumber, fileName, filePath):
    ''' Return the list of files found associated with runNumber
    '''
    fileList = []
    for iFile in range(0, fileNumber):
        fileList.append(fileName % (filePath, runNumber, iFile))

    inFiles = '\n'.join(fileList)
    print ('[{0}] - Found {1} raw slcio files for run {2} : \n{3}'.format(os.path.basename(__file__), fileNumber, runNumber, inFiles))
    return inFiles

# -----------------------------------------------------------------------------
def elapsedTime(startTime):
    ''' Print time to finish job
    '''
    t_sec = round(time.time() - startTime)
    (t_min, t_sec) = divmod(t_sec, 60)
    (t_hour, t_min) = divmod(t_min, 60)
    print('Time passed: {:.0f} hour {:.0f} min {:.0f} sec'.format(t_hour, t_min, t_sec))



'''
'''
# -----------------------------------------------------------------------------
def checkPeriod(runNumber, runPeriod, configFile):
    if runNumber < '726177' and (runPeriod != 'SPS_08_2012' or runPeriod != 'SPS_11_2012'):
        print ("[Streamout.py] - RunNumber '%s' is from TestBeam 'SPS_08_2012' or 'SPS_11_2012', you selected '%s' in configFile '%s'" % (runNumber, config.runPeriod, configFile))
        sys.exit(0)

    if runNumber >= '726177' and runNumber <= '726414' and runPeriod != 'SPS_12_2014':
        print ("[Streamout.py] - RunNumber '%s' is from TestBeam 'SPS_12_2014', you selected '%s' in configFile '%s'" % (runNumber, config.runPeriod, configFile))
        sys.exit(0)

    if runNumber >= '727760' and runNumber <= '728456' and runPeriod != 'SPS_04_2015':
        print ("[Streamout.py] - RunNumber '%s' is from TestBeam 'SPS_04_2015', you selected '%s' in configFile '%s'" % (runNumber, config.runPeriod, configFile))
        sys.exit(0)

    if runNumber >= '728501' and runNumber <= '728682' and runPeriod != 'PS_06_2015':
        print ("[Streamout.py] - RunNumber '%s' is from TestBeam 'PS_06_2015', you selected '%s' in configFile '%s'" % (runNumber, config.runPeriod, configFile))
        sys.exit(0)

    if runNumber >= '730436' and runNumber <= '730926' and runPeriod != 'SPS_10_2015':
        print ("[Streamout.py] - RunNumber '%s' is from TestBeam 'SPS_10_2015', you selected '%s' in configFile '%s'" % (runNumber, config.runPeriod, configFile))
        sys.exit(periodError('SPS_10_2015'))

    if runNumber >= '730927' and runPeriod != 'SPS_06_2016':
        print ("[Streamout.py] - RunNumber '%s' is from TestBeam 'UNKNOWN', you selected '%s' in configFile '%s'" % (runNumber, config.runPeriod, configFile))
        sys.exit(0)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def main():
    '''
    '''
    scriptName = os.path.basename(__file__) # For logging clarity

    runNumber = None
    runListArg = None
    fileNum = None
    configFile = "config_streamout" # Default config file if none is given on cli     


    # --- Parse CLI arguments
    if len(sys.argv) > 1:
        # --- Load configuration File
        configFile = sys.argv[1]
        try:
            exec("import {0} as config".format(configFile))
        except (ImportError, SyntaxError):
            sys.exit("[{0}] - Cannot import config file '{1}'".format(scriptName, configFile))
        # --- /Load configuration File
        if len(sys.argv) > 2:
            # --- Load runList
            runListArg = sys.argv[2]
            if len(sys.argv) > 3:
                # --- Load number of streamoutFile to process
                fileNum = int(sys.argv[3])
    else:
        print ("Please give : configFile - runNumber(s)(optional if set up in configFile) - Number of streamout file to process(optional)")
        return   
    # --- /Parse CLI arguments



    # --- Load List of runs
    if runListArg is None: # if no runs on CLI, load list from configFile
        try:
            runList = config.runList
        except AttributeError:
            sys.exit("[{0}] - No runs specified at command line or in configFile...exiting".format(scriptName))
    else:
        runList = runListArg.split(',')
    # --- /Load List of runs



    for run in runList:
        checkPeriod(run, config.runPeriod, configFile)
        runNumber = int(run)
        #   List number of files to streamout (raw data are split in 2Go files with
        #   format DHCAL_runNumber_I0_fileNumber.slcio )
        print ('\n\n[Streamout.py] - Looking for files to streamout for run \'%d\' in \'%s\'... ' % (runNumber, config.inputPath), end="")
        stringToFind = 'DHCAL_{0}_I0_'.format(runNumber)
        if fileNumber == 0:
            return
        print ('OK')

        # Check if more/less files available than asked by the user
        if fileNum is not None:
            if fileNum != fileNumber:
        inputFiles = listFiles(fileNumber, runNumber)
        outputFile = config.outputFile % (config.outputPath, runNumber) # extension slcio/root added in the xml generator
        print ("[Streamout.py] - output file : %s.slcio" % outputFile)
        print ("[Streamout.py] - MARLIN_DLL: %s" % (config.marlinLib))

        if os.path.exists("%s.slcio" % outputFile) is True:
            print ("[Streamout.py] - OutputFile already present...exiting")
            return
                    


        log = open(config.logFile % (config.logPath, runNumber), "w", 1) # line-buffered
        print("\n[Streamout.py] ========================")
        print ('[Streamout.py] --- Running Marlin...')
        print ('[Streamout.py] --- Ouput is logged to \'%s\'' % log)
        beginTime = time.time()
        subprocess.call(["Marlin", config.xmlFile], env=dict(os.environ, MARLIN_DLL=config.marlinLib, MARLINDEBUG="1"), stdout=log)
        print ('[Streamout.py] - Running Marlin...OK, - ', end='')
        elapsedTime(beginTime)
        print("[Streamout.py] ========================\n")

        print ('[Streamout.py] - Removing xmlFile...', end='')
        subprocess.Popen(["rm", config.xmlFile])
        print ("OK")
                ans = raw_input('\n\t [{}] - *** WARNING! *** Found {} files for run {}, you asked to process {}. Proceed? (y/n)\n'.format(scriptName, fileNumber, runNumber, fileNum))
                if ans == 'y':
                    fileNumber = fileNum
                else:
                    sys.exit('Exiting')




# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if  __name__ == '__main__':
    main()
