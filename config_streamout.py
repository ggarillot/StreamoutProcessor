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

# runList=[726180]
# runList=[733756]
# runList=[728243]

# SPS 10 2016
# runList = [733598, 733615, 733626, # 733628 DONE,
#  733631, 733632, # 733633 FAILED,
#  733636, 733637, 733641, 733642, 733643, 733644, 733645, 733646, 733647, 733650, 733653, 733654, 733655, 733656, 733658, 733659, 733660, # 733665 FAILED open or read 
#  733675, 733678, 733679, # 733680 FAILED 
#  733683, 733686, 733688, # 733689 FAILED 
#  733692, 733693, 733696, 733698, 733699, 733700, 733701, 733702, 733705, 733707, 733708, 733710, 733711, # 733718 FAILED 
#  733719, 733720, 733722, 733723, , 733725, 733728, 733738, 733740, 733741, , , , , , 733757, 733758, 733759]


# SPS 10 2016 state 224
# runList=[ 733724, 733728, 733742, 733743, 733748, 733750, 733754, 733756    , 733711, 733718,733654, 733655,733656, 733660, 733665, 733675, 733680, 733683, 733686, 733689, 733693, 733696]
# SPS 10 2016 state 227
# runList=[733711, 733718]
# SPS 10 2016 state 224 - 2012 Condition
# runList=[733654, 733655]
# SPS 10 2016 state 238
# runList=[733656, 733660, 733665, 733675, 733680, 733683, 733686, 733689, 733693, 733696]



# SPS_06_2016
runList=[ 732695, 732773, 732777, 732778, 732725, 732728, 732729, 732774, 732867, 732817, 732818, 732820, 732826, 732872, 732875, 732877, 732878, 732865, 732882, 732889]
# runList=[ 732725, 732728, 732774]
# 
# 
# 732665, 732666, 732667, 732668, 732669, 732670, 732671, 732672, 732673, 732674, 732675, 732676, 732677, 732678, 732679, 732680, 732681, 732682, 732683, 732684, 732685, 732686, 732687, 732688, 732689, 732690, 732691, 732692, 732693,732694, 732695, 732695, 732696, 732697, 732698, 732699, 732700, 732701, 732702, 732703, 732704, 732705, 732706, 732707, 732708, 732709, 732710, 732711, 732712, 732713, 732714, 732715, 732715, 732717, 732718, 732719, 732720, 732721, 732722, 732723, 732724, 732725, 732726, 732727, 732728, 732728, 732728, 732728, 732729, 732730, 732731, 732732, 732733, 732734, 732735, 732736, 732737, 732738, 732739, 732740, 732741, 732742, 732743, 732744, 732745, 732746, 732747, 732748, 732749, 732750, 732751, 732752, 732753, 732763, 732764, 732765, 732766, 732767, 732768, 732769, 732769, 732770, 732771, 732772, 732773, 732774, 732775, 732776, 732777, 732777, 732778, 732778, 732778, 732779, 732780, 732781, 732782, 732783, 732784, 732785, 732786, 732787, 732788, 732789, 732790, 732791, 732792, 732793, 732794, 732795, 732796, 732797, 732798, 732799, 732800, 732801, 732802, 732803, 732804, 732805, 732806, 732807, 732808, 732809, 732810, 732811, 732812, 732813, 732814, 732815, 732815, 732816, 732817, 732818, 732818, 732819, 732820, 732821, 732822, 732823, 732824, 732825, 732826, 732827, 732828, 732829, 732830, 732831, 732832, 732833, 732834, 732835, 732836, 732837, 732838, 732839, 732840, 732841, 732842, 732842, 732843, 732843, 732843, 732844, 732845, 732846, 732847, 732848, 732849, 732850, 732851, 732852, 732853, 732854,
 # 732855, 732856, 732857, 732858, 732859, 732860, 732861, 732862, 732863, 732864, 732864, 732865, 732866, 732867, 732868, 732869, 732870, 732871, 732872, 732873, 732874, 732875, 732876, 732877, 732878, 732879, 732879, 732880, 732882, 732882, 732883, 732884, 732885, 732886, 732887, 732888, 732889, 732890, 732891, 732892, 732893, 732894, 732895, 732896, 732897, 732898, 732899, 732900, 732901, 732902, 732903, 732904, 732905, 732906, 732907, 732908, 732909 ]


# CERENKOV DEBUGGING
# runList=[726411] # SPS_12_2014
# runList=[728338] # SPS_04_2015 electrons
# runList=[728645] # SPS_06_2015
# runList=[730655, 730668, 730677, 730709, 730713] # SPS_10_2015
# runList =[733728] # SPS_10_2016


####################
### Grid Section
####################
runOnGrid = True
# runOnGrid = False
backend = 'Local'
# backend = 'LSF'
# backend = 'LSF'
voms = 'calice'
#CE = 'lyogrid07.in2p3.fr:8443/cream-pbs-calice'
#CE = 'lpnhe-cream.in2p3.fr:8443/cream-pbs-calice'
CE = 'grid-cr0.desy.de:8443/cream-pbs-desy'
carefulLoaderDir = "/eos/user/a/apingaul/CALICE/script/"

gridDownloader = '/home/ilc/pingault/script/carefulDownload.sh'
gridUploader = '/home/ilc/pingault/script/carefulUpload.sh'
LCG_CATALOG_TYPE = 'lfc'
LFC_HOST = 'grid-lfc.desy.de'

eos_home = '/eos/user/a/apingaul/CALICE/'
#gridDataPath = eos_home + 'data/' + runPeriod 
gridIlcSoftPath = "/cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/"
gridProcessorPath = eos_home + "Software/Streamout/"

gridInputFiles = []
 # xmlFile and marlinLibrary are added after
              # gridProcessorPath + 'run_marlin.py',
              # gridProcessorPath + 'marlin.py',
              # gridProcessorPath + 'StreamoutProcessor.xml'
              # gridUploader,
              # gridDownloader
              # ] 
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
# runPeriod = "SPS_12_2014"
# runPeriod = "SPS_04_2015"
# runPeriod = "PS_06_2015"
# runPeriod = "SPS_10_2015"
runPeriod = "SPS_06_2016"
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

print "runOnGrid: {0}".format(runOnGrid)
print "dataPath: {0}".format(dataPath)

inputPath = "%s/Raw" % dataPath
outputPath = "%s/Streamout" % dataPath
plotPath = "%s/Plots" % dataPath
logPath = "%s/Logs" % dataPath

logFile = "{0}/streamLog_{1}" # % (logPath, runNumber)
inputFile = "{0}/DHCAL_{1}_I0_{2}.slcio" # % (inputPath, runNumber, streamoutFileNumber)
outputFile = "{0}/DHCAL_{1}_SO_Antoine" # extension slcio/root added in script # % (outputPath,runNumber)
# outputFile = "{0}/DHCAL_{1}_SO_CerDebug" # extension slcio/root added in script # % (outputPath,runNumber)

processorPath = "/Users/antoine/cernbox/CALICE/Software/Streamout"
if runOnGrid is True:
    processorPath = gridProcessorPath
xmlFile = "{0}/StreamoutProcessor.xml".format(processorPath) # Path to XML file
# marlinLib = "{0}/lib/libStreamoutMarlin.dylib".format(processorPath) # Marlin library for processor
marlinLib = "{0}/lib/libStreamoutMarlin.so".format(processorPath) # Marlin library for processor
if runOnGrid is True:
    gridInputFiles.append(xmlFile)
    gridInputFiles.append(marlinLib)
    gridInputFiles.append(gridProcessorPath + 'marlin.py')
    # gridInputFiles.append(marlinCfgFile)


####################
### Scp section for autoDownload before running
####################
# If file not available, use serverName to scp it from.
# serverName = 'lyoac29'
serverName = 'lyoac30'
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
glob.MaxRecordNumber = 0 # Max Number of event to process
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
    # streamoutProc.EcalDetectorIds = "201 1100"

else:
    print "[config_streamout] - runPeriod '%s' is wrong or undefined in configuration file" % runPeriod
