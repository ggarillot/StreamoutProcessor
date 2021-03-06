'''
    Configuration file for streamout processor. Is read by streamout.py
    python steer/streamout.py config_streamout run1,run2,etc. numberOfFilesToStreamout(optional, script will runs on all files by default)
    export PYTHONPATH=/cvmfs/ganga.cern.ch/Ganga/install/LATEST/python/:${PYTHONPATH}
'''
import sys

# SPS_06_2016
# MRPC Runs
# runList = [732889,732882,732876,732877,732878,732875,732874,732873,732872,732869,732867,732865,732864,732863,732861,732860,732853,732852] # use this list if no runNumber specified when running streamout.py

# MRPC Muons Runs
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
''' ------------------------- Complete SPS_12_2014 runList ------------------------- '''
# runList = [726195, 726196, 726197, 726204, 726205, 726206, 726207, 726208, 726209, 726210, 726211, 726212, 726221, 726222, 726223, 726252, 726253, 726254, 726255, 726256, 726257, 726260, 726261, 726262, 726263, 726264, 726265, 726273, 726278, 726280, 726286, 726287, 726289, 726290, 726301, 726302, 726305, 726306, 726307, 726310, 726328, 726335, 726337, 726338, 726339, 726344, 726345, 726354, 726356, 726357, 726360, 726362, 726368, 726369, 726370, 726371, 726372, 726373, 726374, 726375, 726376, 726377, 726403, 726404, 726405, 726407, 726408, 726409, 726411, 726412, 726413, 726414]
''' ------------------------- Complete SPS_04_2015 runList ------------------------- '''
# runList = [ 728097, 728099, 728100, 728103, 728105, 728107, 728108, 728110, 728111, 728113, 728114, 728116, 728117, 728118, 728120, 728121, 728122, 728123, 728125, 728127, 728129, 728132, 728136, 728137, 728140, 728142, 728143, 728144, 728153, 728154, 728155, 728156, 728172, 728174, 728176, 728179, 728180, 728181, 728183, 728186, 728187, 728190, 728194, 728197, 728198, 728199, 728200, 728201, 728202, 728203, 728204, 728206, 728211, 728214, 728217, 728219, 728223, 728229, 728231, 728235, 728236, 728238, 728239, 728240, 728242, 728243, 728244, 728246, 728247, 728249, 728251, 728258, 728259, 728262, 728265, 728271, 728272, 728276, 728278, 728284, 728287, 728288, 728289, 728290, 728291, 728313, 728314, 728315, 728322, 728329, 728330, 728331, 728332, 728334, 728336, 728338, 728340, 728341, 728342, 728344, 728345, 728346, 728348, 728350, 728351, 728352, 728354, 728357, 728359, 728360, 728363, 728366, 728368, 728369, 728370, 728372, 728373, 728374, 728381, 728383, 728385, 728389, 728393, 728395, 728396, 728398, 728399, 728401, 728403, 728405, 728406, 728408, 728410, 728412, 728415, 728426, 728427, 728428, 728429, 728430, 728431, 728433, 728434, 728435, 728438, 728448, 728449, 728450, 728451, 728452, 728453, 728454, 728455, 728456 ]
''' ------------------------- Complete PS_06_2015 runList ------------------------- '''
# runList = [ 728536, 728537, 728538]
# runList = [ 728542, 728543, 728544, 728545, 728549, 728552, 728553, 728554, 728555, 728556, 728557, 728558, 728561, 728564, 728572, 728579, 728580, 728581, 728582, 728584, 728585, 728587, 728592] #006

# runList = [ 728595, 728603, 728607, 728608, 728610, 728611, 728614, 728615, 728618, 728623, 728625, 728626, 728627, 728628, 728630, 728631, 728632, 728633, 728634, 728635, 728636, 728637, 728638] #069

# runList = [ 728639, 728640, 728641, 728642, 728643, 728644, 728645, 728646, 728650, 728652, 728653, 728654, 728656, 728658, 728659, 728660, 728661, 728662, 728663, 728664, 728665, 728666, 728667] # 030

# runList = [  728668, 728669, 728670, 728672, 728673, 728674, 728675, 728676, 728677, 728678, 728680, 728681, 728682 ] #104
''' ------------------------- complete SPS_10_2015 runList ------------------------- '''
# runList = [ 730489, 730490, 730491, 730497, 730502, 730504, 730505, 730509, 730511, 730516, 730518, 730522, 730526, 730533, 730540, 730545, 730548, 730552, 730563, 730566, 730567, 730568, 730569, 730578, 730581, 730582, 730583, 730584, 730605, 730607, 730609, 730611, 730615, 730616, 730617, 730618, 730619, 730620, 730621, 730622, 730623, 730625, 730626, 730627, 730630, 730631, 730633, 730634, 730648, 730651, 730655, 730656, 730657, 730658, 730659, 730661, 730668, 730672, 730673, 730676, 730677, 730678, 730705, 730709, 730713, 730716, 730752, 730756, 730790, 730804, 730816, 730819, 730821, 730823, 730824, 730842, 730844, 730846, 730847, 730851, 730858, 730861, 730882, 730884, 730886, 730888, 730903, 730909, 730914, 730915, 730917, 730920, 730923 ]
# 730490
# runList = [ 730490 ] #027
# 730678, 730705, 730709, 730713] OK
# runList = [ 730824, 730842, 730844, 730846, 730847] OK
# runList = [ 730851, 730858, 730861, 730882, 730884, 730886] OK
# runList = [ 730489, 730823, 730888, 730903, 730909] OK
''' ------------------------- complete SPS_06_2016 runList -------------------------'''
# runList = [ 732695, 732724, 732725, 732728, 732729, 732731, 732768, 732769, 732770, 732771, 732772, 732773, 732774, 732775, 732777, 732778, 732779, 732786, 732790, 732791, 732792, 732815, 732817, 732818, 732819, 732820, 732826, 732827, 732829, 732831, 732832, 732835, 732836, 732837, 732838, 732839, 732840, 732841, 732842, 732843, 732844, 732845, 732846, 732847, 732850, 732852, 732853, 732860, 732861, 732863, 732864, 732865, 732869, 732872, 732873, 732874, 732875, 732876, 732877, 732878, 732882, 732883, 732889, 732891, 732904]
''' ------------------------- complete SPS_10_2016 runList ------------------------- '''
# runList = [ 733628, 733637, 733654, 733655, 733656, 733660, 733665, 733675, 733683, 733686, 733688] #lxplus030

# runList = [ 733689, 733693, 733696, 733698, 733699, 733711, 733718, 733720, 733723, 733724, 733728] #lxplus063

# runList = [  733742, 733743, 733748, 733750, 733754, 733756 ] #lxplus012

# SPS 10 2016 state 224
# runList=[ 733724, 733728, 733742, 733743, 733748, 733750, 733754, 733756    , 733711, 733718,733654, 733655,733656, 733660, 733665, 733675, 733680, 733683, 733686, 733689, 733693, 733696]
# SPS 10 2016 state 227
# runList=[733711, 733718]
# SPS 10 2016 state 224 - 2012 Condition
# runList=[733654, 733655]
# SPS 10 2016 state 238
# runList=[733656, 733660, 733665, 733675, 733680, 733683, 733686, 733689, 733693, 733696]
''' ------------------------- SPS_09_2017 ------------------------- '''
# Calo displacement scan ?
# Full List
# runList = [736572, 736571, 736570, 736569, 736568, 736567, 736566, 736565, 736564, 736563, 736562, 736561, 736560, 736559, 736558, 736557, 736556, 736554, 736545, 736544, 736543, 736542, 736541, 736540, 736539, 736538, 736537, 736536, 736535, 736533, 736532, 736531, 736530, 736529]

# Complete list withtout bad runs
# runList = [
#     736576, 736575, 736574, 736573, 736572, 736571, 736570, 736569, 736567, 736566, 736565, 736564, 736563, 736562,
#     736560, 736559, 736558, 736545, 736543, 736542, 736540, 736538, 736537, 736536, 736535, 736534, 736532, 736531,
#     736530, 736528, 736525, 736523, 736522, 736521, 736520, 736519, 736517, 736516, 736515, 736514, 736513, 736512,
#     736511, 736509, 736508, 736507, 736506, 736505, 736503, 736501, 736500
# ]

# runList = [
#     736571, 736570, 736569, 736566, 736565, 736564, 736563, 736562, 736560, 736559, 736558, 736545, 736543, 736542,
#     736540, 736538, 736537, 736536, 736532, 736531, 736528, 736525, 736523, 736522, 736520, 736519, 736517, 736516,
#     736515, 736514, 736513, 736512, 736511, 736509, 736503, 736501, 736500
# ]

# runList= [736543, 736566, 736572]
runList= [736572]

# runList = [736521, 736530, 736534, 736535, 736567, 736572, 736573, 736574, 736575, 736576]
''' ------------------------- CERENKOV DEBUGGING -------------------------'''
# runList=[726411] # SPS_12_2014
# runList=[728338] # SPS_04_2015 electrons
# runList=[728645] # SPS_06_2015
# runList=[730655, 730668, 730677, 730709, 730713] # SPS_10_2015
# runList =[733728] # SPS_10_2016

# All data are assumed to be in a perPeriod subfolder
# runPeriod = 'SPS_12_2014'
# runPeriod = 'SPS_04_2015'
# runPeriod = 'PS_06_2015'
# runPeriod = 'SPS_10_2015'
# runPeriod = 'SPS_06_2016'
# runPeriod = 'SPS_10_2016'
runPeriod = 'SPS_09_2017'

####################
# Grid Section
####################
# runOnGrid = True
runOnGrid = False
# backend = 'Local'
backend = 'CREAM'
# backend = 'LSF'
voms = 'calice'
# CE = 'lyogrid07.in2p3.fr:8443/cream-pbs-calice'
# CE = 'lpnhe-cream.in2p3.fr:8443/cream-pbs-calice'
CE = 'grid-cr0.desy.de:8443/cream-pbs-desy'
SE = 'lyogrid06.in2p3.fr'

carefulLoaderDir = '/eos/user/a/apingaul/CALICE/script/'
gridDownloader = carefulLoaderDir + 'carefulDownload.sh'
gridUploader = carefulLoaderDir + 'carefulUpload.sh'
lcg_catalog_type = 'lfc'
lfc_host = 'grid-lfc.desy.de'

eos_home = '/eos/user/a/apingaul/CALICE/'
processorPath = eos_home + "Software/Streamout/"
gridProcessorPath = eos_home + "Software/Streamout/"

####################
# Global variables
####################
logToFile = False
ilcSoftVersion = 'v01-19-05'
gridIlcSoftVersion = 'v01-19-05'
ilcSoftPath = '/opt/ilcsoft/'
gridIlcSoftPath = '/cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/'
processorType = 'Streamout'

# General Path to find/store data: the following assumes that all data is in a subfolder of dataPath
# Overwritten by gridDataPath if runOnGrid is True
dataPath = eos_home + 'Data/' + runPeriod
gridDataPath = 'SDHCAL/pingault/TB/CERN/' + runPeriod  # Ganga automatically prepend /grid/calice/ before the path

if runOnGrid is True:
    dataPath = gridDataPath
    processorPath = gridProcessorPath
    ilcSoftPath = gridIlcSoftPath
    ilcSoftVersion = gridIlcSoftVersion

initILCSoftScript = ilcSoftPath + ilcSoftVersion + "/init_ilcsoft.sh"
marlinCfgFile = 'marlinCfg_{}.yml'  # .format(runNumber) cfgFile name written by script to properly run marlin with all variables set
marlinCfgPath = processorPath

print 'runOnGrid: {}'.format(runOnGrid)
print 'dataPath: {}'.format(dataPath)

inputPath = '{}/Raw/'.format(dataPath)
outputPath = '{}/Streamout/'.format(dataPath)
plotPath = '{}/Plots/'.format(dataPath)
logPath = '{}/Logs/'.format(dataPath)

logFile = '{}/streamLog_{}'  # % (logPath, runNumber)
# inputFile = 'DHCAL_{}_I0_{}.slcio'  # %(runNumber, streamoutFileNumber)
outputFile = 'DHCAL_{}_SO_Antoine'  # extension slcio/root added in script # % runNumber
xmlFile = 'StreamoutProcessor.xml'  # Path to XML file

libExt = 'so'

if sys.platform == 'darwin':
    libExt = 'dylib'
marlinLib = 'libStreamoutMarlin.' + libExt  # Marlin library for processor

gridInputFiles = []
if runOnGrid is True:
    gridInputFiles.append(gridProcessorPath + xmlFile)
    gridInputFiles.append(initILCSoftScript)
    gridInputFiles.append(gridProcessorPath + 'processor.tgz')
    gridInputFiles.append(gridProcessorPath + 'marlin.py')
    gridInputFiles.append(gridProcessorPath + 'run_marlin.py')
    # gridInputFiles.append(marlinCfgFile) # Need to be added in the main script as the name is dynamically generated with the runNumber


####################
# Scp section for autoDownload before running
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
if runPeriod == 'SPS_09_2017':
    serverDataPath = '/data/NAS/H2SEPT2017/'

####################
# Marlin parameters
####################


class xmlOptionSection(object):
    def __init__(self, optionName):
        self.name = optionName


# Global param
###
glob = xmlOptionSection('global')
glob.Verbosity = 'MESSAGE'
glob.MaxRecordNumber = 0  # Max Number of event to process
glob.SkipNEvents = 0      # Number of event to skip
glob.LCIOInputFiles = []

# Processor param
###
marlinProc = xmlOptionSection('MyStreamoutProcessor')
# glob.inputCollectionType = 'LCGenericObject'
marlinProc.InputCollectionName = 'RU_XDAQ'
# glob.outputCollectionType = 'RawCalorimeterHit'
marlinProc.OutputCollectionName = 'DHCALRawHits'
# streamoutProc.exportROOT = True # Write to root file (Not implemented yet)
marlinProc.Verbosity = 'MESSAGE'

marlinProc.RU_SHIFT = 23  # Not used?
marlinProc.DropFirstRU = False  # Drop first Trigger
marlinProc.SkipFullAsic = True  # Skip asic with all 64 channels lit up

marlinProc.CerenkovDifId = 3  # Since May2015
marlinProc.CerenkovOutDifId = 3
marlinProc.CerenkovOutAsicId = 1
marlinProc.CerenkovOutTimeDelay = 6

marlinProc.Before2016Data = True  # Bool for Ecal data detection (change in data format in 2016) Overridden in the following lines

if '2012' in runPeriod:
    marlinProc.XDAQ_SHIFT = 92  # ? 2012

elif '2014' in runPeriod:
    marlinProc.XDAQ_SHIFT = 24  # 2014-2015
    marlinProc.CerenkovDifId = 1  # Dec2014

elif '2015' in runPeriod:
    marlinProc.XDAQ_SHIFT = 24  # 2014-2015

elif '2016' in runPeriod or '2017' in runPeriod:
    marlinProc.XDAQ_SHIFT = 20  # Since June2016
    marlinProc.Before2016Data = False  # Bool for Ecal data detection
    marlinProc.TreatEcal = False
    # streamoutProc.EcalDetectorIds = "201 1100"

else:
    print "[config_streamout] - runPeriod '{}' is wrong or undefined in configuration file".format(runPeriod)

print '[config_streamout] - Finished parsing configFile'
