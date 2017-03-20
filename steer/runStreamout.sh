#!/bin/sh 
runLocal=false

# period="SPS_10_2016"
run=$1
period=$2
cerenkovDifId=3
# XDAQ_SHIFT=20
# cerenkovDifId=1
XDAQ_SHIFT=24
Before2016Data="True"
maxEvt=0



if [ "$#" -lt 2 ]; then
  echo "Wring Arguments, usage : runStreamout.sh runNumber tbPeriod"
  return 111
fi

if [ "$runLocal" = true ]; then
  echo " Running on my Pee Aye Aime Pee"
  export MARLIN_DLL=/eos/user/a/apingaul/CALICE/Software/Streamout/lib/libStreamoutMarlin.dylib
  # dataFolder="/eos/user/a/apingaul/CALICE/Data/$period"
  dataFolder="/Volumes/PagosDisk/CALICE/data/$period"
  sourceilc
else 
  echo " Running on Lx+" 
  # export MARLIN_DLL=/eos/user/a/apingaul/CALICE/Software/sdhcal_analysis/lib/libmymarlin.so
  # source ~/init_ilcsoft.sh
  # dataFolder="/eos/user/a/apingaul/CALICE/Data/$period"
  export MARLIN_DLL=libStreamoutMarlin.so
  dataFolder="/grid/calice/SDHCAL/pingault/TB/CERN/$period"
  source init_ilcsoft.sh
fi



# dataFolder="/eos/user/a/apingaul/CALICE/CALICE/Data/SPS_10_2016/"

echo " .... Running Streamout process, local File : $(ls -al)"

export LFC_HOST=grid-lfc.desy.de

echo "LFC_HOST = '${LFC_HOST}'"

INPUTFOLDER="${dataFolder}/Raw"

# FILELIST=`ls ${INPUTFOLDER} | grep TDHCAL_${run}.slcio`
FILELIST=$(ls | grep "DHCAL_${run}_I0_*.slcio")
if
    [[ $FILELIST == "DHCAL_${run}_I0_*.slcio" ]]
    then
    echo ${FILELIST}
else
    echo "Looking on grid for files, run = '${run}' - inputGridFolder = '${INPUTFOLDER}' "
    echo "lfc-ls ${INPUTFOLDER} | grep ${run}"
    echo "$(lfc-ls ${INPUTFOLDER} | grep ${run})"
    
    # echo "lcg-lr --vo calice lfn:${INPUTFOLDER}/${filename##*/}"
    # lcg-lr --vo calice lfn:${INPUTFOLDER}/${filename##*/}
    FILELIST=$(lfc-ls ${INPUTFOLDER} | grep ${run})
    echo " Found : ${FILELIST}"
    if [ -z "$FILELIST" ]; then
        exit 111
    fi
    for file in ${FILELIST};
      do source carefulDownload.sh ${file} ${INPUTFOLDER}
    done
fi

echo "FILELIST = " ${FILELIST}
echo " --- Found" ${FILELIST} " in " ${INPUTFOLDER}

OUTPUTFOLDER="${dataFolder}/Streamout/"
OUTPUTFILENAME="DHCAL_${run}_SO_Antoine" 


  # <parameter name="LCIOInputFiles"> ${INPUTFOLDER}/${FILELIST}  </parameter>
cat > StreamoutLCIO.xml <<EOF
<marlin>
  <execute>
    <processor name="MyStreamoutProcessor"/>
  </execute>
  <global>
    <parameter name="LCIOInputFiles">
     ${FILELIST} 
     </parameter>
    <parameter name="MaxRecordNumber">${maxEvt}</parameter>
    <parameter name="SkipNEvents">0</parameter>
    <parameter name="Verbosity" options="DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT">DEBUG0</parameter>
  </global>
  <processor name="MyStreamoutProcessor" type="StreamoutProcessor">
    <parameter name="Verbosity" type="string" options="DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT">DEBUG0</parameter>
    <parameter name="InputCollectionName" type="string" lcioInType="LCGenericObject">RU_XDAQ</parameter>
    <parameter name="OutputCollectionName" type="string" lcioOutType="LCGenericObject">DHCALRawHits</parameter>
    <parameter name="LCIOOutputFile" type="string">${OUTPUTFILENAME}.slcio</parameter>
    <parameter name="ROOTOutputFile" type="string">${OUTPUTFILENAME}.root</parameter>
    <parameter name="PlotFolder" type="string">"./"</parameter>
    <parameter name="RU_SHIFT" type="int">23</parameter>
    <parameter name="XDAQ_SHIFT" type="int">${XDAQ_SHIFT}</parameter>
    <parameter name="CerenkovDifId" type="int">${cerenkovDifId}</parameter>
    <parameter name="DropFirstRU" type="bool">False</parameter>
    <parameter name="SkipFullAsic" type="bool">True</parameter>
    <parameter name="Before2016Data" type="bool">${Before2016Data}</parameter>
    <parameter name="TreatEcal" type="bool">False</parameter>
    <!-- <parameter name="EcalDetectorIds" type="std::vector<int>">201,1100</parameter> -->
  </processor>
</marlin>
EOF

Marlin StreamoutLCIO.xml
rm StreamoutLCIO.xml
for file in ${FILELIST}; do
    rm file
done
echo " Marlin Done...List of local files : $(ls -al)"
echo " Uploading Files (slcio) : $(ls -al | grep slcio)"
source carefulUpload.sh ${OUTPUTFILENAME}.slcio ${OUTPUTFOLDER};
echo " Uploading Files (root) : $(ls -al | grep root)"
source carefulUpload.sh ${OUTPUTFILENAME}.root ${OUTPUTFOLDER};
