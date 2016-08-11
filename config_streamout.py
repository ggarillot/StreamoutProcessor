inputFile = "%s/DHCAL_%d_I0_%d.slcio"
outputFile = "%s/DHCAL_%d_SO" # extension slcio/root added in xml

processorPath = "/Users/antoine/CALICE/Software/Streamout"
xmlFile = "/StreamoutProcessor.xml" # XML file to be generated
marlinLib = "/lib/libStreamoutMarlin.dylib" # Marlin library for processor


# dataPath="/Users/antoine/CALICE/DataAnalysis/data"
dataPath = "/Volumes/PagosDisk/CALICE/data/SPS_06_2016/"


processorList = [["MyStreamoutProcessor", "StreamoutProcessor"]] # List of [name,type]
inputCollectionType = "LCGenericObject"
inputCollectionName = "RU_XDAQ"
outputCollectionType = "RawCalorimeterHit"
outputCollectionName = "DHCALRawHits"
verbosity = "MESSAGE"


exportROOT = False # Write to root file (Not implemented yet)

maxEvt = 0 # Max Number of event to process
nSkipEvt = 0 # Number of event to skip

ruShift = 23
# xDaqShift = 92 # 2012
# xDaqShift = 24 # 2014-2015
xDaqShift = 0 # Since June2016
dropRu = False # Drop first Trigger
skipFullAsic = True # Skip asic with all 64 channels lit up

cerenkovDifId = 3 # Dif Id for cerenkov (1 in December, 3 otherwise)

# ''' Configuration file for streamout processor. Is read by streamout.py'''
