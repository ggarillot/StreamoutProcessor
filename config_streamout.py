'''
    Configuration file for streamout processor. Is read by streamout.py
    python steer/streamout.py config_streamout run1,run2,etc. numberOfFilesTostreamout(optional, script will runs on all files by default)
'''

#MRPC Runs
# runList = [732889,732882,732876,732877,732878,732875,732874,732873,732872,732869,732867,732865,732864,732863,732861,732860,732853,732852] # use this list if no runNumber specified when running streamout.py

#MRPC Muons Runs
# runList = ['''732865''', 732864, 732863, 732861, 732860, 732853, '''732852'''] # use this list if no runNumber specified when running streamout.py



'''
    Dec2014
    ----------
    State 158 - Lead 8mm - Cerenkov Muons
    80     70     60     50     40     30     20     
    726407 726408 726409 726411 726412 726413 726414
    ----------
    State 150 - Lead 4mm - Cerenkov Muons
    
    
    726371 726370 726369 726368 726362 726360 726357 726356 726354 726345 726344 726339 726338 726337 726335 726328 726310 726307 726306 726305 
'''

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


####################
### Marlin parameters
####################

class xmlOptionSection(object):
    def __init__(self, optionName):
        self.name = optionName

### Global param
###
glob = xmlOptionSection('global')
glob.Verbosity = "DEBUG0"
glob.MaxRecordNumber = 5 # Max Number of event to process
glob.SkipNEvents = 0 # Number of event to skip
glob.LCIOInputFiles = []


### Processor param
###
streamoutProc = xmlOptionSection('MyStreamoutProcessor')
# glob.inputCollectionType = "LCGenericObject"
streamoutProc.InputCollectionName = "RU_XDAQ"
# glob.outputCollectionType = "RawCalorimeterHit"
streamoutProc.OutputCollectionName = "DHCALRawHits"              
# streamoutProc.exportROOT = True # Write to root file (Not implemented yet)

streamoutProc.RU_SHIFT = 23 # Not used?
streamoutProc.DropFirstRU = False # Drop first Trigger
streamoutProc.SkipFullAsic = True # Skip asic with all 64 channels lit up


streamoutProc.CerenkovDifId = 3 # Since May2015
streamoutProc.Before2016Data = True # Bool for Ecal data detection (change in data format in 2016)

if runPeriod.find("2012") != -1:
    streamoutProc.XDAQ_SHIFT = 92 #? 2012

elif runPeriod.find("2014") != -1:
    streamoutProc.XDAQ_SHIFT = 24 # 2014-2015
    streamoutProc.CerenkovDifId = 1 # Dec2014

elif runPeriod.find("2015") != -1:
    streamoutProc.XDAQ_SHIFT = 24 # 2014-2015
    
elif runPeriod.find("2016") != -1:
    streamoutProc.XDAQ_SHIFT = 20 # Since June2016
    streamoutProc.Before2016Data = False # Bool for Ecal data detection
    streamoutProc.TreatEcal = False
    streamoutProc.EcalDetectorIds = "201 1100"

else:
    print "[config_streamout] - runPeriod '%s' is wrong or undefined in configuration file" % runPeriod
