'''
    Configuration file for streamout processor. Is read by streamout.py
    python steer/streamout.py config_streamout run1,run2,etc. numberOfFilesTostreamout(optional, script will runs on all files by default)
'''

#MRPC Runs
# runList = [732889,732882,732876,732877,732878,732875,732874,732873,732872,732869,732867,732865,732864,732863,732861,732860,732853,732852] # use this list if no runNumber specified when running streamout.py

#MRPC Muons Runs
# runList = ['''732865''', 732864, 732863, 732861, 732860, 732853, '''732852'''] # use this list if no runNumber specified when running streamout.py


    726371 726370 726369 726368 726362 726360 726357 726356 726354 726345 726344 726339 726338 726337 726335 726328 726310 726307 726306 726305 
'''

# runPeriod = "SPS_12_2014"
runList=[726201,726238]
####################
### Grid Section
####################
runOnGrid = True
backend = 'Local'
voms = 'calice'
#CE = 'lyogrid07.in2p3.fr:8443/cream-pbs-calice'
#CE = 'lpnhe-cream.in2p3.fr:8443/cream-pbs-calice'
CE = 'grid-cr0.desy.de:8443/cream-pbs-desy'
gridDownloader = '/home/ilc/pingault/script/carefulDownload.sh'
gridUploader = '/home/ilc/pingault/script/carefulUpload.sh'
LCG_CATALOG_TYPE = 'lfc'
LFC_HOST = 'grid-lfc.desy.de'

eos_home = '/eos/user/a/apingaul/CALICE/'
#gridDataPath = eos_home + 'data/' + runPeriod 
gridIlcSoftPath = "/cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/"
gridProcessorPath = eos_home + "Software/Streamout/"

gridInputFiles = [ # xmlFile and marlinLibrary are added after
              gridProcessorPath + 'run_marlin.py',
              gridProcessorPath + 'Marlin.py',
              # gridProcessorPath + 'StreamoutProcessor.xml',
              # gridUploader,
              # gridDownloader
              ] 
               # os.path.relpath(xmlFile, processorPath + '/'),
              # '%s/DifGeom/m3_bonneteau.xml' %path




####################
### Global variables
####################
ilcSoftVersion = "v01-19-01"
# ilcSoftVersion = "v01-17-09"
ilcSoftPath = "/opt/ilcsoft/"
if runOnGrid is True:
    ilcSoftPath = gridIlcSoftPath
initILCSoftScript = ilcSoftPath + ilcSoftVersion + "/init_ilcsoft.sh"
marlinCfgFile = "marlinCfg_{0}.yml" #.format(runNumber) cfgFile name written by script to properly run marlin with all variables set

# All data are assumed to be in a perPeriod subfolder
runPeriod = "SPS_12_2014"
# runPeriod = "SPS_04_2015"
# runPeriod = "PS_06_2015"
# runPeriod = "SPS_10_2015"
# runPeriod = "SPS_06_2016"
# runPeriod = "SPS_10_2016"

# General Path to find/store data: the following assumes that all data is in a subfolder of dataPath
# Overwritten by gridDataPath if runOnGrid is True
# dataPath = "/Users/antoine/CALICE/DataAnalysis/data"
dataPath = "/Volumes/PagosDisk/CALICE/data/%s" % runPeriod # Local
gridDataPath = eos_home + 'Data/' + runPeriod 
# dataPath = "/scracth/SDHCAL/data/%s" % runPeriod # Lyoserv
# dataPath = "/eos/users/a/apingaul/CALICE/Data%s" % runPeriod # Lxplus

if runOnGrid is True:
    dataPath = gridDataPath

inputPath = "%s/Raw" % dataPath
outputPath = "%s/Streamout" % dataPath
plotPath = "%s/Plots" % dataPath
logPath = "%s/Logs" % dataPath

logFile = "{0}/streamLog_{1}" # % (logPath, runNumber)
inputFile = "%s/DHCAL_%d_I0_%d.slcio" # % (inputPath, runNumber, streamoutFileNumber)
outputFile = "%s/DHCAL_%d_SO_TAIS" # extension slcio/root added in script # % (outputPath,runNumber)

processorPath = "/Users/antoine/CALICE/Software/Streamout"
if runOnGrid is True:
    processorPath = gridProcessorPath
xmlFile = "{0}/StreamoutProcessor.xml".format(processorPath) # Path to XML file
# marlinLib = "{0}/lib/libStreamoutMarlin.dylib".format(processorPath) # Marlin library for processor
marlinLib = "{0}/lib/libStreamoutMarlin.so".format(processorPath) # Marlin library for processor
if runOnGrid is True:
    gridInputFiles.append(xmlFile)
    gridInputFiles.append(marlinLib)
    # gridInputFiles.append(marlinCfgFile)


####################
### Scp section for autoDownload before running
####################
# If file not available, use serverName to scp it from.
serverName = 'lyoac29'
# serverName = 'lyoac30'
# serverName = 'lyosdhcal10'
# serverName = 'lyosdhcal12'

serverDataPath = ''
if runPeriod == 'SPS_12_2014':
    serverDataPath = '/data/NAS/December2014/'
if runPeriod == 'SPS_04_2015':
    serverDataPath = '/data/NAS/Avril2015/'
if runPeriod == 'SPS_06_2015':
    serverDataPath = '/data/NAS/May2015/'
if runPeriod == 'SPS_10_2015':
    serverDataPath = '/data/NAS/October2015/'
if runPeriod == 'SPS_06_2016':
    serverDataPath = '/data/NAS/June2016/'
if runPeriod == 'SPS_10_2016':
    serverDataPath = '/data/NAS/Oct2016/'

processorList = [["MyStreamoutProcessor", "StreamoutProcessor"]] # List of [name,type]
verbosity = "DEBUG0"

inputCollectionType = "LCGenericObject"
inputCollectionName = "RU_XDAQ"
outputCollectionType = "RawCalorimeterHit"
outputCollectionName = "DHCALRawHits"



exportROOT = True # Write to root file (Not implemented yet)

maxEvt = 0 # Max Number of event to process
nSkipEvt = 0 # Number of event to skip

ruShift = 23 # Not used?

dropRu = False # Drop first Trigger
skipFullAsic = True # Skip asic with all 64 channels lit up


if runPeriod.find("2012") != -1:
    xDaqShift = 92 #? 2012
    before2016Data = True # Bool for Ecal data detection

elif runPeriod.find("2014") != -1 or runPeriod.find("2015") != -1:
    xDaqShift = 24 # 2014-2015
    cerenkovDifId = 1 # Dec2014
    before2016Data = True # Bool for Ecal data detection

elif runPeriod.find("2016") != -1:
    xDaqShift = 20 # Since June2016
    cerenkovDifId = 3 # Since May2015
    before2016Data = False # Bool for Ecal data detection
    treatEcal = False
    EcalDetectorIds = "201 1100"

else:
    print "[config_streamout] - runPeriod '%s' is wrong or undefined in configuration file" % runPeriod
