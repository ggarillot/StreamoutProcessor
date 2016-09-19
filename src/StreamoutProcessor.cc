


// -- streamoutProcessor
#include "StreamoutProcessor.h"
#include "DIFUnpacker.h"
#include "DIF.h"

// -- lcio header
// #include <EVENT/LCCollection.h>
// #include <EVENT/MCParticle.h>
// #include <EVENT/LCParameters.h>
// #include <UTIL/CellIDDecoder.h>
#include "IMPL/RawCalorimeterHitImpl.h"
#include "IMPL/LCCollectionVec.h"
#include "IMPL/LCEventImpl.h"
#include "IMPL/LCFlagImpl.h"

// ----- include for verbosity dependend logging ---------
#include "marlin/VerbosityLevels.h"


// -- ROOT includes
#include <TCanvas.h>

//-------------------------------------------------------------------------------------------------
//-------------------------------------------------------------------------------------------------
class LMGeneric: public IMPL::LCGenericObjectImpl
{
public:
  /** Constructor
   */
  LMGeneric()
  {
    /* nop */
  }

  /** Get the int vector (reference)
   */
  std::vector<int>& getIntVector()
  {
    return _intVec;
  }
};

//-------------------------------------------------------------------------------------------------
//-------------------------------------------------------------------------------------------------

StreamoutProcessor aStreamoutProcessor ;

StreamoutProcessor::StreamoutProcessor() : Processor("StreamoutProcessor") {

  // modify processor description
  m_processorDescription = "Create a RawCalorimeterHit collection from a LCGenericObject* collection of sdhcal raw dif buffers" ;

  m_inputCollectionName = "RU_XDAQ";
  registerInputCollection( LCIO::LCGENERICOBJECT,
                           "InputCollectionName",
                           "RU_XDAQ Collection Name",
                           m_inputCollectionName,
                           m_outputCollectionName);

  m_outputCollectionName = "DHCALRawHits";
  registerOutputCollection( LCIO::RAWCALORIMETERHIT,
                            "OutputCollectionName" ,
                            "RawCaloHit Collection Name",
                            m_outputCollectionName,
                            m_outputCollectionName);

  m_outputFileName = "StreamoutProcessorOutput.slcio";
  registerProcessorParameter("LCIOOutputFile",
                             "LCIO file",
                             m_outputFileName,
                             m_outputFileName);

  m_cerenkovDifId = 3;
  registerProcessorParameter("CerenkovDifId",
                             "DifID number for the Cerenkov signal",
                             m_cerenkovDifId,
                             m_cerenkovDifId);


  m_ruShift = 23;
  registerProcessorParameter("RU_SHIFT",
                             "Byte shift for raw data reading",
                             m_ruShift,
                             m_ruShift);

  m_xdaqShift = 24;
  registerProcessorParameter("XDAQ_SHIFT",
                             "XDAQ Byte shift for raw data reading",
                             m_xdaqShift,
                             m_xdaqShift);

  m_dropFirstRU = false;
  registerProcessorParameter("DropFirstRU",
                             "Drop first Trigger event (bool)",
                             m_dropFirstRU,
                             m_dropFirstRU);

  m_skipFullAsics = true;
  registerProcessorParameter("SkipFullAsic",
                             "Skip full Asic event (bool)",
                             m_skipFullAsics,
                             m_skipFullAsics);

  m_isBefore2016Data = false;
  registerProcessorParameter("Before2016Data",
                             "Header of raw data was modified in 2016 to account for combined test beam",
                             m_isBefore2016Data,
                             m_isBefore2016Data);

  m_shouldTreatEcal = false;
  registerProcessorParameter("TreatEcal",
                             "Treat Ecal data (bool)",
                             m_shouldTreatEcal,
                             m_shouldTreatEcal);

  std::vector<int> ecalDetectorIds = {201, 1100}; // June 2016 Combined Test Beam
  registerProcessorParameter("EcalDetectorIds",
                             "DetectorId for Ecal Data",
                             m_ecalDetectorIds,
                             ecalDetectorIds);

  registerProcessorParameter( "ROOTOutputFile" ,
                              "File name for the root output",
                              m_rootFileName,
                              std::string("toto.root") );

  registerProcessorParameter( "PlotFolder" ,
                              "Folder Path to save Plot",
                              m_plotFolder,
                              std::string("./") );
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::init()
{
  printParameters() ;

  char cnormal[8] =  {0x1b, '[', '0', ';', '3', '9', 'm', 0};
  char cred[8]     = {0x1b, '[', '1', ';', '3', '1', 'm', 0};
  char cgreen[8]   = {0x1b, '[', '1', ';', '3', '2', 'm', 0};
  char cyellow[8]  = {0x1b, '[', '1', ';', '3', '3', 'm', 0};
  char cblue[8]    = {0x1b, '[', '1', ';', '3', '4', 'm', 0};
  char cmagenta[8] = {0x1b, '[', '1', ';', '3', '5', 'm', 0};
  char cwhite[8]   = {0x1b, '[', '1', ';', '3', '9', 'm', 0};

  normal   = cnormal;
  red      = cred;
  green    = cgreen;
  yellow   = cyellow;
  blue     = cblue;
  magenta  = cmagenta;
  white    = cwhite;

  m_pLCStreamoutWriter = new LCStreamoutWriter(m_outputFileName);

  m_rootFile = new TFile(m_rootFileName.c_str(), "RECREATE");

  m_nRun = 0 ;
  m_nEvt = 0 ;
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::processRunHeader( LCRunHeader* /*run*/)
{
  m_nRun++ ;
  m_nEvt = 0;
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::processEvent( LCEvent * pLCEvent )
{
  if ( NULL == pLCEvent )
  {
    streamlog_out( ERROR ) << " Invalid Ptr to the Event - Aborting" << std::endl;
    return;
  }

  m_eventNbr = pLCEvent->getEventNumber();

  // grab the input collection
  EVENT::LCCollection *pLCCollection = NULL;
  try
  {
    pLCCollection = pLCEvent->getCollection(m_inputCollectionName);
  }
  catch (EVENT::DataNotAvailableException &exception)
  {
    streamlog_out( ERROR ) <<  " - Input collection name not found : " << m_inputCollectionName << std::endl;
    return;
  }

  if (NULL == pLCCollection)
  {
    streamlog_out( ERROR ) <<  " - Collection '" << m_inputCollectionName << "' is empty...exiting" << std::endl;
    return;
  }

  // check collection type
  if (EVENT::LCIO::LCGENERICOBJECT != pLCCollection->getTypeName())
  {
    streamlog_out( ERROR ) <<  " - Wrong collection type : expected '" << EVENT::LCIO::LCGENERICOBJECT << "' found '" << pLCCollection->getTypeName() << "'...exiting" << std::endl;
    return;
  }

  int numElements = pLCCollection->getNumberOfElements();// hit number
  streamlog_out( DEBUG ) << " numElements in colleciton '" << m_inputCollectionName << "' : " << numElements << std::endl;
  // create the output collection
  IMPL::LCCollectionVec *pRawCalorimeterHitCollection = new IMPL::LCCollectionVec(EVENT::LCIO::RAWCALORIMETERHIT);

  // configure it
  IMPL::LCFlagImpl chFlag(0) ;
  EVENT::LCIO bitinfo;
  chFlag.setBit(bitinfo.RCHBIT_LONG);   // raw calorimeter data -> format long
  chFlag.setBit(bitinfo.RCHBIT_BARREL); // barrel
  chFlag.setBit(bitinfo.RCHBIT_ID1);    // cell ID
  chFlag.setBit(bitinfo.RCHBIT_TIME);   // timestamp
  pRawCalorimeterHitCollection->setFlag(chFlag.getFlag());

  // convert the input elements to DIFPtrs
  for ( int e = 0 ; e < pLCCollection->getNumberOfElements() ; e++)
  {
    if (e == 0 && m_dropFirstRU)
      continue;

    LMGeneric *pLCGenericObject = (LMGeneric *)(pLCCollection->getElementAt(e));

    if (NULL == pLCGenericObject)
      continue;

    // grab the generic object contents
    int *pGenericRawBuffer = &(pLCGenericObject->getIntVector()[0]);
    unsigned char *pRawBuffer = (unsigned char *)pGenericRawBuffer;

    /** Check for detectorId (2016 data)   |   2015 data -> No detectorId
      * _iptr[0] = detId                   |  _iptr[0] = timeBuffer
      * _iptr[1] = difId                   |  _iptr[1] = evtCounter
      * _iptr[2] = GTC (evtCounter)        |  _iptr[2] = evtCounter
      * _iptr[3] = timeBuffer              |  _iptr[3] = evtCounter
      * _iptr[4] = ?                       |  _iptr[4] = difId
      * _iptr[5] = TriggerLenght ?         |  _iptr[5] = ?
      * _iptr[6] = 256 * GTC               |  _iptr[6] = TriggerLenght ?
      * _iptr[7] = ?                       |  _iptr[7] = 256 * GTC
      * _iptr[8] = 256 * GTC               |  _iptr[8] = 0
      */


    if (false == m_isBefore2016Data && false == m_shouldTreatEcal)
    {
      uint32_t* _iptr = (uint32_t*) pRawBuffer;

      if (find(m_ecalDetectorIds.begin(), m_ecalDetectorIds.end(), _iptr[0]) != m_ecalDetectorIds.end())
      {
        streamlog_out ( DEBUG0 ) << red << "Skipping ECAL data with detId '" << _iptr[0] << "'" << normal << std::endl;
        continue;
      }
    }

    uint32_t ruSize = pLCGenericObject->getNInt() * sizeof(int32_t);
    uint32_t idStart = DIFUnpacker::getStartOfDIF(pRawBuffer, ruSize, m_xdaqShift);

    if (idStart != m_xdaqShift)
    {
      uint32_t* _iptr = (uint32_t*) pRawBuffer;
      for (const auto & i : m_ecalDetectorIds)
        streamlog_out ( MESSAGE ) << green << "m_ecalDetectorIds: '" << i << "'" << normal << std::endl;

      streamlog_out( WARNING ) << red << " *** WARNING *** Unusual start of dif shift! idStart : " << idStart << "\t xdaqShift: " << m_xdaqShift << "\t detId: " << _iptr[0] << normal << std::endl;
      continue;
    }
    // create the DIF ptr
    unsigned char *pDifRawBuffer = &pRawBuffer[idStart];
    DIFPtr *pDifPtr = new DIFPtr(pDifRawBuffer, ruSize - idStart + 1);
    int difId = pDifPtr->getID();

    streamlog_out( DEBUG0 ) << blue << " DIF: " << difId << " idStart: " << idStart << normal << std::endl;
    int tag = 0;
    if ( difId == m_cerenkovDifId )
    {
      std::vector<unsigned char*> theFrames_;
      std::vector<unsigned char*> theLines_;

      theFrames_.clear();
      theLines_.clear();

      pDifPtr->dumpDIFInfo();
      try
      {
        DIFUnpacker::getFramePtrPrint(theFrames_, theLines_, ruSize - idStart + 1, pDifRawBuffer);
      } catch (std::string e)
      {
        streamlog_out( ERROR ) << "DIF " << pDifPtr->getID() << " " << e << std::endl;
        delete pRawCalorimeterHitCollection;
        return;
      }

      streamlog_out( DEBUG1 ) << blue << " - Hit in Dif " << pDifPtr->getID() << "\t NFrames : " <<  pDifPtr->getNumberOfFrames() << normal << std::endl;
      for (uint32_t i = 0; i < pDifPtr->getNumberOfFrames(); i++)
      {
        streamlog_out( DEBUG1 ) << " - FrameTime : " << pDifPtr->getFrameTimeToTrigger(i) << std::endl;
        for (uint32_t j = 0; j < 64; j++)
        {
          if (pDifPtr->getFrameLevel(i, j, 0))
          {
            streamlog_out( DEBUG1 )  << " - FrameLevel0 - i: " << i << " j: " << j << std::endl;
            tag += 1;
          }
          if (pDifPtr->getFrameLevel(i, j, 1))
          {
            streamlog_out( DEBUG1 )  << " - FrameLevel1 - i: " << i << " j: " << j << std::endl;
            tag += 2;
          }
        }
      }
    }

    if ( 0 != tag)
      streamlog_out( DEBUG1 )  << " - Tag : " << tag << std::endl;


    for (unsigned int f = 0 ; f < pDifPtr->getNumberOfFrames() ; f++)
    {
      // find whether the dif has full asics
      if (m_skipFullAsics)
      {
        unsigned int touchedChannels = 0;

        for (unsigned int ch = 0 ; ch < 64 ; ch++)
        {
          if (!(pDifPtr->getFrameLevel(f, ch, 0) || pDifPtr->getFrameLevel(f, ch, 1)))
            continue;

          touchedChannels++;
        }

        if (64 == touchedChannels)
          continue;
      }

      // create the raw calorimeter hits
      for (unsigned int ch = 0 ; ch < 64 ; ch++)
      {
        // skip empty pads
        if (!(pDifPtr->getFrameLevel(f, ch, 0) || pDifPtr->getFrameLevel(f, ch, 1)))
          continue;

        unsigned long int id0 = 0;
        unsigned long int id1 = 0;
        unsigned long barrelEndcapModule = 0;
        // time stamp of this event from Run Begining
        unsigned long int timeStamp = (unsigned long int)(pDifPtr->getFrameTimeToTrigger(f));
        std::bitset<6> channel(ch);
        std::bitset<3> amplitudeBitSet;



        /**
         * Fill hitMap asic vs Channel for each dif
         */

        Int_t difId = (unsigned long int)(((unsigned short)pDifPtr->getID()) & 0xFF);
        Int_t asicId = (unsigned long int) (unsigned short) pDifPtr->getFrameAsicHeader(f);
        Int_t chanId = (unsigned long int)(channel.to_ulong());

        const auto & mapFind = m_mapHitPerDif.find(difId);
        if (mapFind == m_mapHitPerDif.end()) {
          std::string histoName;
          std::stringstream oss; // osstringstream crash Marlin at some point...
          oss << "hitMapChanAsic_Dif" << difId;
          m_mapHitPerDif.insert(m_mapHitPerDif.end(), std::pair<int, TH2D*>(difId, new TH2D(oss.str().c_str(), oss.str().c_str(), 48, 0, 48, 64, 0, 64)));
          m_mapHitPerDif.at(difId)->GetXaxis()->SetTitle("Asic");
          m_mapHitPerDif.at(difId)->GetYaxis()->SetTitle("Channel");
        }
        
        // streamlog_out( MESSAGE ) << yellow << "Filling trackPos for Dif '" << difId << "'..." << normal << std::endl;
        m_mapHitPerDif.at(difId)->Fill(asicId, chanId);
        // m_hitPerDifAsic->Fill(difId * asicId, chanId);
        // streamlog_out( MESSAGE ) << blue << "Booking trackPos for Dif '" << difId << "'...OK" << normal << std::endl;

        /* ================================= =================================*/

        // 8 firsts bits: DIF Id
        id0 = (unsigned long int)(((unsigned short)pDifPtr->getID()) & 0xFF);

        // 8 next bits:   Asic Id
        id0 += (unsigned long int)(((unsigned short)pDifPtr->getFrameAsicHeader(f) << 8) & 0xFF00);

        //6 next bits:   Asic's Channel
        id0 += (unsigned long int)((channel.to_ulong() << 16) & 0x3F0000);

        //(40 barrel + 24 endcap) modules to be coded here 0 for testbeam (over 6 bits)
        id0 += (unsigned long int)((barrelEndcapModule << 22) & 0xFC00000);

        // cell id 1
        id1 = (unsigned long int)(pDifPtr->getFrameBCID(f));

        amplitudeBitSet[0] = pDifPtr->getFrameLevel(f, ch, 0);
        amplitudeBitSet[1] = pDifPtr->getFrameLevel(f, ch, 1);
        amplitudeBitSet[2] = true; // always synchronized ?

        IMPL::RawCalorimeterHitImpl *pRawCalorimeterHit = new IMPL::RawCalorimeterHitImpl();

        pRawCalorimeterHit->setCellID0(id0);
        pRawCalorimeterHit->setCellID1(id1);
        pRawCalorimeterHit->setAmplitude(amplitudeBitSet.to_ulong());
        pRawCalorimeterHit->setTimeStamp(timeStamp);

        pRawCalorimeterHitCollection->addElement(pRawCalorimeterHit);
      }
    }

    EVENT::IntVec trigger(8);

    trigger[0] = pDifPtr->getDTC(); // DifTriggerCount
    trigger[1] = pDifPtr->getGTC(); // GeneralTriggerCount
    trigger[2] = pDifPtr->getBCID();
    trigger[3] = pDifPtr->getAbsoluteBCID() & 0xFFFFFF;
    trigger[4] = (pDifPtr->getAbsoluteBCID() / (0xFFFFFF + 1)) & 0xFFFFFF;
    trigger[5] = pDifPtr->getTASU1();
    trigger[6] = pDifPtr->getTASU2();
    trigger[7] = pDifPtr->getTDIF();

    std::stringstream parameterKey;
    parameterKey << "DIF" << pDifPtr->getID() << "_Triggers";

    pRawCalorimeterHitCollection->parameters().setValues(parameterKey.str(), trigger);
  }

  // check if any hits have been added to the collection
  // should never happened except if empty event
  if (pRawCalorimeterHitCollection->getNumberOfElements() == 0)
  {
    streamlog_out( ERROR )  << "No raw calorimeter hits produced !" << std::endl;
    delete pRawCalorimeterHitCollection;
    return;
  }

  // add the collection to event
  IMPL::LCEventImpl * pOutLCEvent = new IMPL::LCEventImpl();
  pOutLCEvent->setRunNumber (pLCEvent->getRunNumber());
  pOutLCEvent->setEventNumber (pLCEvent->getEventNumber());
  pOutLCEvent->setDetectorName (pLCEvent->getDetectorName());
  pOutLCEvent->setTimeStamp (pLCEvent->getTimeStamp());
  pOutLCEvent->setWeight (pLCEvent->getWeight());
  try
  {
    pOutLCEvent->addCollection(pRawCalorimeterHitCollection, m_outputCollectionName);
  }
  catch (IO::IOException &exception)
  {
    streamlog_out( ERROR ) << "Couldn't add collection '" << m_outputCollectionName << "' : already present" << std::endl;
    delete pRawCalorimeterHitCollection;
    return;
  }

  try
  {
    m_pLCStreamoutWriter->processReconstructedEvent(pOutLCEvent);
  }
  catch (IO::IOException &exception)
  {
    streamlog_out( ERROR ) << "Failed to write event '" << m_nEvt << "' to file..." << std::endl;
    delete pRawCalorimeterHitCollection;
    return;
  }
  m_nEvt ++ ;
  streamlog_out( ERROR ) << "Event processed : " << m_nEvt << std::endl;
  delete pRawCalorimeterHitCollection;
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::setRuShift(int ruShift)
{
  m_ruShift = ruShift;
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::setXDaqShift(unsigned int shift)
{
  m_xdaqShift = shift;
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::setInputCollectionName(const std::string &collectionName)
{
  m_inputCollectionName = collectionName;
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::setOutputCollectionName(const std::string &collectionName)
{
  m_outputCollectionName = collectionName;
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::setDropFirstRU(bool drop)
{
  m_dropFirstRU = drop;
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::setSkipFullAsic(bool skip)
{
  m_skipFullAsics = skip;
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::end() {
  delete m_pLCStreamoutWriter;

  std::vector<Int_t> difList;
  difList.push_back(18);
  difList.push_back(87);
  difList.push_back(63);
  difList.push_back(80);
  difList.push_back(182);
  difList.push_back(105);


  TCanvas *c1 = new TCanvas();
  c1->SetCanvasSize(1920,1080);
  c1->Update();
  c1->cd();
  c1->Divide(3,2);
  Int_t iPad = 1;
  for (const auto &dif:difList)
   { 
    c1->cd(iPad);
    std::cout << "Drawing for dif " << dif << " in pad " << iPad << std::endl;
    m_mapHitPerDif.at(dif)->Draw("colz");
    ++iPad;
   }
   std::stringstream ss;
   ss << m_plotFolder << "/hitMapChanAsicLayer48-50_run" << m_eventNbr << ".png";
   c1->SaveAs(ss.str().c_str());

  m_rootFile->Write();
  m_rootFile->Close();
}
