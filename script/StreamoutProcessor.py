#!/usr/bin/env python

import os
import sys

class Params :
	def __init__(self) :
		self.outputFileName = 'analysis.slcio'
		self.maxRecordNumber = 0
		self.skipNEvents = 0
		self.RU_SHIFT = 23  # Not used?
		self.DropFirstRU = 'false'  # Drop first Trigger
		self.SkipFullAsic = 'true'  # Skip asic with all 64 channels lit up

		self.CerenkovDifId = 3  # Since May2015
		self.CerenkovOutDifId = 3
		self.CerenkovOutAsicId = 1
		self.CerenkovOutTimeDelay = 6

		self.Before2016Data = 'true'  # Bool for Ecal data detection (change in data format in 2016) Overridden in the following lines
		self.TreatEcal = 'false'
		self.XDAQ_SHIFT = 24


def launch(a , files) :

	fileList = ''
	for name in files :
		fileList += name + ' '

	pid = os.getpid()

	xmlFileName = str(pid) + '.xml'
	tempOutputFile = str(pid) + '.slcio'


	xml = '''<marlin>
  <execute>
    <processor name="MyStreamoutProcessor"/>
  </execute>

  <global>
    <parameter name="LCIOInputFiles">''' + fileList + '''</parameter>
    <parameter name="MaxRecordNumber" value="''' + str(a.maxRecordNumber) + '''"/>
    <parameter name="SkipNEvents" value="''' + str(a.skipNEvents) + '''" />
    <parameter name="Verbosity" options="DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT"> MESSAGE </parameter>
  </global>

  <processor name="MyStreamoutProcessor" type="StreamoutProcessor">
    <parameter name="Verbosity" type="string" options="DEBUG0-4,MESSAGE0-4,WARNING0-4,ERROR0-4,SILENT">MESSAGE</parameter>

    <parameter name="InputCollectionName" type="string" lcioInType="LCGenericObject">RU_XDAQ</parameter>
    <parameter name="OutputCollectionName" type="string" lcioOutType="LCGenericObject">DHCALRawHits</parameter>

    <parameter name="LCIOOutputFile" type="string">''' + tempOutputFile + '''</parameter>
    <parameter name="RU_SHIFT" type="int">''' + str(a.RU_SHIFT) + '''</parameter>
    <parameter name="DropFirstRU" type="bool">''' + a.DropFirstRU + '''</parameter>
    <parameter name="XDAQ_SHIFT" type="int">''' + str(a.XDAQ_SHIFT) + '''</parameter>
    <parameter name="CerenkovDifId" type="int">''' + str(a.CerenkovDifId) + '''</parameter>
    <parameter name="CerenkovOutDifId" type="int">''' + str(a.CerenkovOutDifId) + '''</parameter>
    <parameter name="CerenkovOutAsicId" type="int">''' + str(a.CerenkovOutAsicId) + '''</parameter>
    <parameter name="CerenkovOutTimeDelay" type="int">''' + str(a.CerenkovOutTimeDelay) + '''</parameter>
    <parameter name="SkipFullAsic" type="bool">''' + a.SkipFullAsic + '''</parameter>
    <parameter name="Before2016Data" type="bool">''' + a.Before2016Data + '''</parameter>
    <parameter name="TreatEcal" type="bool">''' + a.TreatEcal + '''</parameter>
    <parameter name="EcalDetectorIds" type="IntVec">201 1100</parameter>
  </processor>

</marlin>'''

	xmlFile = open(xmlFileName , 'w')
	xmlFile.write(xml)
	xmlFile.close()

	os.system('Marlin ' + xmlFileName)
	os.system('rm ' + xmlFileName)
	os.system('mv ' + tempOutputFile + ' ' + a.outputFileName)
