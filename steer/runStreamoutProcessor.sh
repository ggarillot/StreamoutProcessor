#!/bin/bash

export MARLIN_DLL=`pwd`/lib/libStreamoutMarlin.dylib
dataPath="/Users/antoine/CALICE/DataAnalysis/data" 
fileNumber=0

[[ $# -lt 1 ]] &&  echo -e "par1 = runNumber; par2=fileNumber(${fileNumber} by default); par3=outputFile(DHCAL_runNumber_SO.slcio by default); par4 = dataPath(${dataPath} by default)\n" && return

runNumber=$1
outputFile="${dataPath}/DHCAL_${runNumber}_SO"

[[ $# -gt 3 ]] &&  dataPath=$4
[[ $# -gt 2 ]] &&  outputFile=${dataPath}/$3
[[ $# -gt 1 ]] &&  fileNumber=$2

inputFile="${dataPath}/DHCAL_${runNumber}_I0_${fileNumber}.slcio"
echo "inputFile: ${inputFile}"
echo "outputFile: ${outputFile}.slcio"

cat > LCIO.xml <<EOF
<marlin>
 <execute>
  <processor name="StreamoutProcessor"/>
 </execute>
 <global>
  <parameter name="LCIOInputFiles">
    ${inputFile}
  </parameter>
  <!-- limit the number of processed records (run+evt): -->
  <!--parameter name="MaxRecordNumber" value="1000"/-->
  <!--parameter name="SkipNEvents" value="18000" /-->
  <parameter name="SupressCheck" value="false" />
  <!--parameter name="GearXMLFile"> gear_ldc.xml </parameter-->
  <!--parameter name="Verbosity" options="DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT"> MESSAGE  </parameter-->
  <!--parameter name="RandomSeed" value="1234567890" /-->
 </global>
 <processor name="StreamoutProcessor" type="StreamoutProcessor">
    <parameter name="InputCollectionName" type="string" lcioInType="LCGenericObject"> RU_XDAQ </parameter>
    <parameter name="OutputCollectionName" type="string" lcioInType="RawCalorimetHit"> DHCALRawHits </parameter>
    <parameter name="CerenkovDifId" type="int"> 3 </parameter>
    <parameter name="LCIOOutputFile" type="string" > ${outputFile}.slcio </parameter>
 </processor>
</marlin>
EOF

Marlin LCIO.xml
