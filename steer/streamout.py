from lxml import etree
import shlex # split properly command line for Popen
import os,sys,subprocess

if len(sys.argv) > 2:
    runNumber=int(sys.argv[1] )
    configFile=sys.argv[2]
else:
    print "Please give a run Number and config file"

try:
    exec("import %s  as config" % configFile)
except ImportError:
    raise Exception("cannot import config file '%s'" % configFile)


if len(sys.argv) > 3:
 fileNumber=int(sys.argv[3])
else:
 fileNumber = 1
# else:
#   command_line = "ls -l %s | grep %d_I0_ | wc -l" % (config.dataPath,runNumber)
#   print command_line
#   args = shlex.split(command_line)
#   print args
#   proc = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)
#   child_stdout, child_stderr = proc.communicate("grep %d_I0_")

  
fileList = []
for iFile in range(0,fileNumber):
  fileList.append(config.inputFile % (config.dataPath,runNumber,iFile))

print fileList

# for file in fileList:
inputFiles ='\n'.join(fileList)

print inputFiles

outputFile = config.outputFile % (config.dataPath,runNumber) # extension slcio/root added below

# create XML 
## TAG: Execute 
marlin = etree.Element('marlin')
execute = etree.SubElement(marlin,"execute")
for proc in config.processorList:
  processor = etree.SubElement(execute,"processor", name=proc[0])

## TAG: Global 
glob = etree.SubElement(marlin,"global")
paramLCIO = etree.SubElement(glob,"parameter", name="LCIOInputFiles")
paramLCIO.text = inputFiles
# -- Processor Parameters
# --- Max number of evts to process
paramMaxEvt = etree.SubElement(glob,"parameter", name="MaxRecordNumber")
paramMaxEvt.set("value",str(config.maxEvt))
# --- Number of evts to skip
paramSkipEvt = etree.SubElement(glob,"parameter", name="SkipNEvents")
paramSkipEvt.set("value",str(config.nSkipEvt))
# --- Verbosity
paramVerbosity = etree.SubElement(glob,"parameter", name="Verbosity")
paramVerbosity.set("options","DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT")
paramVerbosity.text = config.verbosity

## TAG: Processors
for proc in config.processorList:
  processor = etree.SubElement(marlin,"processor",name=proc[0])
  processor.set("type",proc[1])

  # --- Verbosity
  paramVerbosity = etree.SubElement(processor,"parameter", name="Verbosity")
  paramVerbosity.set("type","string")
  paramVerbosity.set("options","DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT")
  paramVerbosity.text = config.verbosity
  
  # --- InputCollection
  paramInput = etree.SubElement(processor,"parameter", name="InputCollectionName")
  paramInput.set("type","string")
  paramInput.set("lcioInType",config.inputCollectionType)
  paramInput.set("value",config.inputCollectionName)
  
  # --- OutputCollection
  paramOutput = etree.SubElement(processor,"parameter", name="OutputCollectionName")
  paramOutput.set("type","string")
  paramOutput.set("lcioOutType",config.outputCollectionType)
  paramOutput.set("value",config.outputCollectionName)
  
  # --- LCIO OutputFile
  outFile = etree.SubElement(processor,"parameter", name="LCIOOutputFile")
  outFile.set("type","string")
  outFile.set("value",outputFile + ".slcio")
  
  # --- ROOT OutputFile
  if config.exportROOT:
   outRootFile = etree.SubElement(processor,"parameter", name="ROOTOutputFile")
   outRootFile.set("type","string")
   outRootFile.set("value",outputFile + ".root")
   
  # --- Byte shift for raw data reading
  ruParam = etree.SubElement(processor,"parameter", name="RU_SHIFT")
  ruParam.set("type","int")
  ruParam.set("value",str(config.ruShift))
  
  # --- XDAQ Byte shift for raw data reading-
  xdaqParam = etree.SubElement(processor,"parameter", name="XDAQ_SHIFT")
  xdaqParam.set("type","int")
  xdaqParam.set("value",str(config.xDaqShift))
  
  # --- Cerenkov DIF_Id
  cerenkovIdParam = etree.SubElement(processor,"parameter", name="CerenkovDifId")
  cerenkovIdParam.set("type","int")
  cerenkovIdParam.set("value",str(config.cerenkovDifId))
  
  # --- Drop first Trigger event (bool)
  dropRuParam = etree.SubElement(processor,"parameter", name="DropFirstRU")
  dropRuParam.set("type","bool")
  dropRuParam.set("value",str(config.dropRu))
  
  # --- Skip full Asic event (bool)
  dropRuParam = etree.SubElement(processor,"parameter", name="SkipFullAsic")
  dropRuParam.set("type","bool")
  dropRuParam.set("value",str(config.skipFullAsic))
  
# execute.append(etree.Element('execute'))
# marlin.append(execute)
# # another execute with text
# execute = etree.Element('execute')
# execute.text = 'some text'

# pretty string
s = etree.tostring(marlin, pretty_print=True)
with open (config.processorPath+config.xmlFile,"w") as file:
  file.write(s)

subprocess.Popen(["Marlin",config.processorPath+config.xmlFile], env=dict(os.environ, MARLIN_DLL=config.processorPath+config.marlinLib))
# subprocess.Popen(["rm",config.processorPath+config.xmlFile])
