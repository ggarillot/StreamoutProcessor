'''
    Configuration file for streamout processor. Is read by streamout.py
    python steer/streamout.py config_streamout 732875,732882
'''

#MRPC Runs
# runList = [732889,732882,732876,732877,732878,732875,732874,732873,732872,732869,732867,732865,732864,732863,732861,732860,732853,732852] # use this list if no runNumber specified when running streamout.py

#MRPC Muons Runs
# runList = ['''732865''', 732864, 732863, 732861, 732860, 732853, '''732852'''] # use this list if no runNumber specified when running streamout.py


# runPeriod = "SPS_06_2016"
runPeriod = "SPS_Dec2014"

# dataPath = "/Users/antoine/CALICE/DataAnalysis/data"
dataPath = "/Volumes/PagosDisk/CALICE/data/%s" % runPeriod
inputPath = "%s/Raw" % dataPath
outputPath = "%s/Streamout" % dataPath
plotPath = "%s/Plots" % dataPath
logPath = "%s/Logs" % dataPath

logFile = "%s/streamLog_%s" # % (logPath, runNumber)

inputFile = "%s/DHCAL_%d_I0_%d.slcio" # % (intputPath, runNumber, streamoutFileNumber)
outputFile = "%s/DHCAL_%d_SOTEST" # extension slcio/root added in xml # % (outputPath,runNumber)




processorPath = "/Users/antoine/CALICE/Software/Streamout"
xmlFile = "%s/StreamoutProcessor.xml" % processorPath # XML file to be generated # % processorPath
marlinLib = "%s/lib/libStreamoutMarlin.dylib" % processorPath # Marlin library for processor # % processorPath


processorList = [["MyStreamoutProcessor", "StreamoutProcessor"]] # List of [name,type]
verbosity = "DEBUG0"

inputCollectionType = "LCGenericObject"
inputCollectionName = "RU_XDAQ"
outputCollectionType = "RawCalorimeterHit"
outputCollectionName = "DHCALRawHits"



exportROOT = True # Write to root file (Not implemented yet)

maxEvt = 2 # Max Number of event to process
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
