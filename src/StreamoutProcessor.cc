// -- streamoutProcessor
#include "StreamoutProcessor.h"
#include "DIFUnpacker.h"
#include "DIF.h"

// -- lcio header
#include "IMPL/RawCalorimeterHitImpl.h"
#include "IMPL/LCCollectionVec.h"
#include "IMPL/LCEventImpl.h"
#include "IMPL/LCFlagImpl.h"

// ----- include for verbosity dependend logging ---------
#include "marlin/VerbosityLevels.h"


// -- ROOT includes
#include <TCanvas.h>

#define DEBUGLOG    0
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

  m_cerenkovDifId = 3;
  registerProcessorParameter("CerenkovDifId",
                             "DifID number for the Cerenkov signal",
                             m_cerenkovDifId,
                             m_cerenkovDifId);

  // Cerenkov data format in RawCaloHit
  m_cerenkovOutDifId = 3;
  registerProcessorParameter("CerenkovOutDifId",
                             "DifID number for the Cerenkov signal after reconstruction",
                             m_cerenkovOutDifId,
                             m_cerenkovOutDifId);

  m_cerenkovOutAsicId = 1;
  registerProcessorParameter("CerenkovOutAsicId",
                             "AsicID number for the Cerenkov signal after reconstruction",
                             m_cerenkovOutAsicId,
                             m_cerenkovOutAsicId);

// TODO: Not changing TimeDelay for now... ( Cannot just force the time of the hit : Need to shift the time for each cerenkov hit otherwise we won't be able to remove noise hit that arrives at different time)
  m_cerenkovOutTimeDelay = 6;
  registerProcessorParameter("CerenkovOutTimeDelay",
                             "Time delay between physics event and cerenkov signal",
                             m_cerenkovOutTimeDelay,
                             m_cerenkovOutTimeDelay);

// TODO: IF Cer1+Cer2 within a few clocks -> Add only one hit with Threshold = 3


  // registerProcessorParameter("ROOTOutputFile",
  //                            "File name for the root output",
  //                            m_rootFileName,
  //                            std::string("toto.root"));

  // m_drawPlots = false;
  // registerProcessorParameter("DrawPlots",
  //                            "Bool to draw rootPlots",
  //                            m_drawPlots,
  //                            m_drawPlots);
  //
  // registerProcessorParameter("PlotFolder",
  //                            "Folder Path to save Plot",
  //                            m_plotFolder,
  //                            std::string("./"));
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
  m_runNumber = static_cast<int>(pLCEvent->getRunNumber());

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
      {
	std::cout << " Dropping RU.....\n\n"<<std::endl;
	continue;
      }
    LMGeneric *pLCGenericObject = (LMGeneric *)(pLCCollection->getElementAt(e));

    if (NULL == pLCGenericObject)
      {
	std::cout<< " null object! \n\n" << std::endl;
	continue;
      }
    // grab the generic object contents
    int *pGenericRawBuffer = &(pLCGenericObject->getIntVector()[0]);
    unsigned char *pRawBuffer = (unsigned char *)pGenericRawBuffer;

    /** Check for detectorId (2016 data)   |   2015 data -> No detectorId
     * _iptr[0] = detId  (int32_t)        |  _iptr[0] = timeBuffer
     * _iptr[1] = difId  (int32_t)        |  _iptr[1] = evtCounter
     * _iptr[2] = GTC (evtId) (int32_t)   |  _iptr[2] = evtCounter
     * _iptr[3] = timeBuffer=bxId(int64_t)|  _iptr[3] = evtCounter
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
        streamlog_out ( DEBUG ) << red << "Skipping ECAL data with detId '" << _iptr[0] << "'" << normal << std::endl;
        continue;
      }
    }

    uint32_t ruSize = pLCGenericObject->getNInt() * sizeof(int32_t);
    uint32_t idStart = DIFUnpacker::getStartOfDIF(pRawBuffer, ruSize, m_xdaqShift);

    if (idStart != (uint32_t)m_xdaqShift)
    {
      uint32_t *_iptr = (uint32_t *)pRawBuffer;
      // When running in combination with ecal idstart is shifted for ecal data (id 1100) and combined data (id 201). TODO: See with Laurent
      for (const auto& i : m_ecalDetectorIds)
        streamlog_out ( MESSAGE ) << green << "m_ecalDetectorIds: '" << i << "'" << normal << std::endl;

      streamlog_out( WARNING ) << red << " *** WARNING *** Unusual start of dif shift! idStart : " << idStart << "\t xdaqShift: " << m_xdaqShift << "\t detId: " << _iptr[0] << normal << std::endl;
      continue;
    }
    // create the DIF ptr
    unsigned char *pDifRawBuffer = &pRawBuffer[idStart];
    DIFPtr *pDifPtr = new DIFPtr(pDifRawBuffer, ruSize - idStart + 1);
    int difId = pDifPtr->getID();

    // streamlog_out( MESSAGE ) << blue << " DIF: " << difId << " idStart: " << idStart << normal << std::endl;
    EVENT::IntVec cerTagFrameLevel = {0, 0}; // For the 2 frame level

    if ( difId == m_cerenkovDifId )
    {
      std::vector<unsigned char*> theFrames_;
      std::vector<unsigned char*> theLines_;

      theFrames_.clear();
      theLines_.clear();
#if DEBUGLOG
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
#endif
      streamlog_out(MESSAGE) << green << " - Hit in Bif " << difId << "\t NFrames : " << pDifPtr->getNumberOfFrames() << normal << std::endl;
      for (uint32_t i = 0; i < pDifPtr->getNumberOfFrames(); i++)
      {
        streamlog_out(DEBUG) << " - FrameTime : " << pDifPtr->getFrameTimeToTrigger(i) << std::endl;
        streamlog_out(DEBUG) << " - FrameBCID : " << pDifPtr->getFrameBCID(i) << std::endl;
        streamlog_out(DEBUG) << " - FrameTimeStamp : " << (unsigned long int)(pDifPtr->getFrameTimeToTrigger(i)) << std::endl;
        for (uint32_t j = 0; j < 64; j++)
        {
          if (pDifPtr->getFrameLevel(i, j, 0))
          {
            streamlog_out(DEBUG) << " - FrameLevel0 - i: " << i << " j: " << j << std::endl;
            ++cerTagFrameLevel[0];
          }
          if (pDifPtr->getFrameLevel(i, j, 1))
          {
            streamlog_out(DEBUG) << " - FrameLevel1 - i: " << i << " j: " << j << std::endl;
            ++cerTagFrameLevel[1];
          }
        }
      }
    }

    if ( 0 != cerTagFrameLevel[0] || 0 != cerTagFrameLevel[1])
      streamlog_out( MESSAGE )  << " - TagFrameLevel0 : " << cerTagFrameLevel[0] << " / TagFrameLevel1 : " << cerTagFrameLevel[1] << std::endl;

    // pRawCalorimeterHitCollection->parameters().setValues("CerTagFrameLevel", cerTagFrameLevel);

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
        {
          if (difId == m_cerenkovDifId)
          {
            streamlog_out(ERROR) << " Removing Full asic from cerenkovDif ??? " << std::endl;
          }
            streamlog_out(ERROR) << " Removing Full asic" << std::endl;
          continue;
      }
      }

      bool isSynchronised = false;
      // TODO add synchronisation from laurent streamout?
      // if ((std::find(seeds.begin(), seeds.end(), pDifPtr->getFrameTimeToTrigger(f)) == seeds.end()) &&
      //     (std::find(seeds.begin(), seeds.end(), pDifPtr->getFrameTimeToTrigger(f) - 1) == seeds.end()) &&
      //     (std::find(seeds.begin(), seeds.end(), pDifPtr->getFrameTimeToTrigger(f) + 1) == seeds.end()) &&
      //     (std::find(seeds.begin(), seeds.end(), pDifPtr->getFrameTimeToTrigger(f) - 2) == seeds.end()) &&
      //     (std::find(seeds.begin(), seeds.end(), pDifPtr->getFrameTimeToTrigger(f) + 2) == seeds.end()))
      // {
      //   isSynchronised = false;
      // }

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

        //
        // const auto& mapFind = m_mapHitPerDif.find(difId);
        // if (mapFind == m_mapHitPerDif.end())
        // {
        //   std::string       histoName;
        //   std::stringstream oss; // osstringstream crash Marlin at some point...
        //   oss << "hitMapChanAsic_Dif" << difId;
        //   m_mapHitPerDif.insert(m_mapHitPerDif.end(), std::pair<int, TH2D *>(difId, new TH2D(oss.str().c_str(), oss.str().c_str(), 48, 0, 48, 64, 0, 64)));
        //   m_mapHitPerDif.at(difId)->GetXaxis()->SetTitle("Asic");
        //   m_mapHitPerDif.at(difId)->GetYaxis()->SetTitle("Channel");
        // }

        // streamlog_out( MESSAGE ) << yellow << "Filling trackPos for Dif '" << difId << "'..." << normal << std::endl;
        // m_mapHitPerDif.at(difId)->Fill(asicId, chanId);
        // m_hitPerDifAsic->Fill(difId * asicId, chanId);
        // streamlog_out( MESSAGE ) << blue << "Booking trackPos for Dif '" << difId << "'...OK" << normal << std::endl;

        /* ================================= =================================*/


        unsigned short    difId     = pDifPtr->getID();
        unsigned short    asicId    = pDifPtr->getFrameAsicHeader(f);
        int               chanId    = channel.to_ulong();
        unsigned long int frameTime = pDifPtr->getFrameBCID(f);
        if (difId == m_cerenkovDifId)
        {
          difId = m_cerenkovOutDifId;
          if (asicId != m_cerenkovOutAsicId)                       // bug in firmware when two signals are plugged in the BIF
          {
            // streamlog_out(MESSAGE) << " BIF: Dif/Asic/Chan/TimeToTrigger/bcid: " << difId << "/"
            //                        << asicId << "/" << chanId << "/" << timeStamp << "/" << frameTime << std::endl;
            asicId = asicId & m_cerenkovOutAsicId;
            // streamlog_out(MESSAGE) << " NEWBIF: Dif/Asic/Chan/TimeToTrigger/bcid: " << difId << "/"
            //                        << asicId << "/" << chanId << "/" << timeStamp << "/" << frameTime << std::endl;
            if (asicId != m_cerenkovOutAsicId)
            {
              streamlog_out(ERROR) << " Found a weird asicId for Cerenkov: Dif/Asic/Chan/TimeToTrigger/bcid: " << difId << "/"
                                   << asicId << "/" << chanId << "/" << timeStamp << "/" << frameTime << std::endl;
            }
          }
        }

        // 8 firsts bits: DIF Id
        id0 = (unsigned long int)(difId & 0xFF);
        // 8 next bits:   Asic Id
        id0 += (unsigned long int)((asicId << 8) & 0xFF00);

        //6 next bits:   Asic's Channel
        id0 += (unsigned long int)((chanId << 16) & 0x3F0000);

        //(40 barrel + 24 endcap) modules to be coded here 0 for testbeam (over 6 bits)
        id0 += (unsigned long int)((barrelEndcapModule << 22) & 0xFC00000);

        // cell id 1
        id1 = (unsigned long int)(frameTime);

        amplitudeBitSet[0] = pDifPtr->getFrameLevel(f, ch, 0);
        amplitudeBitSet[1] = pDifPtr->getFrameLevel(f, ch, 1);
        amplitudeBitSet[2] = isSynchronised;

        IMPL::RawCalorimeterHitImpl *pRawCalorimeterHit = new IMPL::RawCalorimeterHitImpl();

        pRawCalorimeterHit->setCellID0(id0);
        pRawCalorimeterHit->setCellID1(id1);
        pRawCalorimeterHit->setAmplitude(amplitudeBitSet.to_ulong());
	unsigned long int TTT = (unsigned long int)(pDifPtr->getFrameTimeToTrigger(f));
        pRawCalorimeterHit->setTimeStamp(TTT);



        // if (f == 0){
        //   if (pDifPtr->getID() == m_cerenkovDifId){
        //     streamlog_out( MESSAGE )  << " - Adding CerenkovHit : " << std::endl;
        //   }
        //   streamlog_out( MESSAGE )  << "difId: " << pDifPtr->getID() <<
        //     " - dif/asic/chan : " << difId << " " << asicId << " " << chanId <<
        //     " - id0 : " << id0 << " id1 : " << id1 <<
        //     " - ampBitSet : " << amplitudeBitSet.to_ulong() <<
        //     " - TimeStamp : " << timeStamp << 
        //     "\n--- True pRawCalorimeterHit value: " <<
        //     " - id0 : " << pRawCalorimeterHit->getCellID0() << " id1 : " <<  pRawCalorimeterHit->getCellID1()  <<
        //     " - ampBitSet : " << pRawCalorimeterHit->getAmplitude() <<
        //     " - TimeStamp : " << pRawCalorimeterHit->getTimeStamp() <<
        //     " - ID : " << pRawCalorimeterHit->id() <<
        //     " -- Collection size: " << pRawCalorimeterHitCollection->getNumberOfElements()
        //     << std::endl;
        // }


        pRawCalorimeterHitCollection->addElement(pRawCalorimeterHit);
        // if (pDifPtr->getID() == m_cerenkovDifId)
        // {
        //   streamlog_out( MESSAGE )  << " -- New Collection size: " << pRawCalorimeterHitCollection->getNumberOfElements() << std::endl;
        //   streamlog_out( MESSAGE )  << " -- Hit ID: " << pRawCalorimeterHitCollection->getElementAt(pRawCalorimeterHitCollection->getNumberOfElements()-1)->id() << std::endl;
        // }
        // TODO Add Cerenkov Collection
        // pRawCalorimeterHitCollection->addElement(pRawCalorimeterHit);
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

  streamlog_out( DEBUG ) << " Number of hits in event '" << pLCEvent->getEventNumber() << "' : " << pRawCalorimeterHitCollection->getNumberOfElements() << std::endl;
  std::cout << pLCEvent->getEventNumber() << " Number of Hit BiBitch" << pRawCalorimeterHitCollection->getNumberOfElements() << std::endl;

  // add the collection to event
  IMPL::LCEventImpl * pOutLCEvent = new IMPL::LCEventImpl();
  pOutLCEvent->setRunNumber (pLCEvent->getRunNumber());
  pOutLCEvent->setEventNumber (pLCEvent->getEventNumber());
  pOutLCEvent->setDetectorName (pLCEvent->getDetectorName());
  pOutLCEvent->setTimeStamp (pLCEvent->getTimeStamp());
  pOutLCEvent->setWeight (pLCEvent->getWeight());
  m_runNumber = int(pLCEvent->getRunNumber());

  // Write marlin parameters used
  // StringVec paramKeys;
  // parameters()->marlin::StringParameters::getStringKeys( paramKeys );

  // for ( unsigned int i = 0; i < paramKeys.size(); i++ ) {
  //     StringVec paramValues;
  //     parameters()->getStringVals(paramKeys[i], paramValues);

  //     std::string str;
  //     for ( unsigned int j = 0; j < paramValues.size(); j++ ) {
  //       str += paramValues[j].c_str();
  //       str += " ";
  //     }
  //     // streamlog_out( DEBUG ) << "\t param : "   << paramKeys[i]
  //     // << ":  "  << str
  //     // << std::endl ;
  //     pOutLCEvent->parameters().setValues(paramKeys[i].c_str(), paramValues);
  // }

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

  // if (m_drawPlots)
  // {
  //   std::vector<unsigned int> difList;
  //   difList.push_back(18);
  //   difList.push_back(87);
  //   difList.push_back(63);
  //   difList.push_back(80);
  //   difList.push_back(182);
  //   difList.push_back(105);
  //
  //
  //   TCanvas *c1 = new TCanvas();
  //   c1->SetCanvasSize(1920, 1080);
  //   c1->Update();
  //   c1->cd();
  //   c1->Divide(3, 2);
  //   Int_t iPad = 1;
  //   for (const auto& dif : difList)
  //   {
  //     c1->cd(iPad);
  //     std::cout << "Drawing for dif " << dif << " in pad " << iPad << std::endl;
  //     if (m_mapHitPerDif.size() > dif)
  //     {
  //       m_mapHitPerDif.at(dif)->Draw("colz");
  //     }
  //     ++iPad;
  //   }
  //   std::stringstream ss;
  //   ss << m_plotFolder << "/hitMapChanAsicLayer48-50_run" << m_runNumber << ".png";
  //   c1->SaveAs(ss.str().c_str());
  // }
  // m_rootFile->Write();
  // m_rootFile->Close();
  // delete m_rootFile;
}
