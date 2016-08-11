


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

  // registerProcessorParameter( "RootFileName" ,
  //        "File name for the root output",
  //        outputRootName,
  //        std::string("toto.root") );
}

//-------------------------------------------------------------------------------------------------
// void StreamoutProcessor::InitParameters()
// {
/*------------algorithm::Cluster------------*/
// registerProcessorParameter( "Streamout::PrintDebug" ,
//              "If true, processor will print some debug information",
//              m_EfficiencyParameterSetting.printDebug,
//              (bool) false );

// m_EfficiencyParameterSetting.trackingParams=m_TrackingParameterSetting;

//   std::vector<float> vec,cev;
//   vec.push_back(-500.0);
//   vec.push_back(500.0);
//   registerProcessorParameter( "Layer::DetectorTransversalSize" ,
//                "Define the detector transversal size used by efficiency algorithm (vector size must be 2 or 4; if 2 -> first value is min, second value is max; if 4 -> two first values define x edges , two last values define y edges) ",
//                cev,
//                vec );
// }

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



  // rootFile = new TFile(outputRootName.c_str(),"RECREATE");

  // tree = (TTree*)rootFfile->Get("tree");
  // if(!tree){
  //   streamlog_out(  << "tree creation" << std::endl;
  //   tree = new TTree("tree","Shower variables");
  // }
  // tree->Branch("eventNum",&_nEvt);
  // tree->Branch("eventChi2",&_eventChi2);
  // tree->Branch("trackCosTheta",&_trackCosTheta);
  // tree->Branch("trackX0",&_trackX0);
  // tree->Branch("trackY0",&_trackY0);
  // tree->Branch("trackZ0",&_trackZ0);
  // tree->Branch("transverseRatio",&_transverseRatio);

  // tree->Branch("Efficiency","std::vector<double>",&_efficiency);
  // tree->Branch("EffEnergy","std::vector<double>",&_effEnergy);
  // tree->Branch("Multiplicity","std::vector<double>",&_multiplicity);
  // tree->Branch("Chi2","std::vector<double>",&_chi2);

  m_nRun = 0 ;
  m_nEvt = 0 ;

  /*--------------------Algorithms initialisation--------------------*/
  // algo_Cluster=new algorithm::Cluster();
  // algo_Cluster->SetClusterParameterSetting(m_ClusterParameterSetting);

  // algo_ClusteringHelper=new algorithm::ClusteringHelper();
  // algo_ClusteringHelper->SetClusteringHelperParameterSetting(m_ClusteringHelperParameterSetting);

  // algo_Tracking=new algorithm::Tracking();
  // algo_Tracking->SetTrackingParameterSetting(m_TrackingParameterSetting);

  // algo_InteractionFinder=new algorithm::InteractionFinder();
  // algo_InteractionFinder->SetInteractionFinderParameterSetting(m_InteractionFinderParameterSetting);

  // algo_Efficiency=new algorithm::Efficiency();
  // algo_Efficiency->SetEfficiencyParameterSetting(m_EfficiencyParameterSetting);

  // for(int i=0; i<_nActiveLayers; i++){
  //   caloobject::CaloLayer* aLayer=new caloobject::CaloLayer(i);
  //   aLayer->setLayerParameterSetting(m_LayerParameterSetting);
  //   layers.push_back(aLayer);
  // }
}

//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::processRunHeader( LCRunHeader* run)
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
  for (unsigned int e = 0 ; e < pLCCollection->getNumberOfElements() ; e++)
  {
    if (e == 0 && m_dropFirstRU)
      continue;

    LMGeneric *pLCGenericObject = (LMGeneric *)(pLCCollection->getElementAt(e));

    if (NULL == pLCGenericObject)
      continue;

    // grab the generic object contents
    int *pGenericRawBuffer = &(pLCGenericObject->getIntVector()[0]);
    unsigned char *pRawBuffer = (unsigned char *)pGenericRawBuffer;
    uint32_t ruSize = pLCGenericObject->getNInt() * sizeof(int32_t);
    uint32_t idStart = DIFUnpacker::getStartOfDIF(pRawBuffer, ruSize, m_xdaqShift);

    // create the DIF ptr
    unsigned char *pDifRawBuffer = &pRawBuffer[idStart];
    DIFPtr *pDifPtr = new DIFPtr(pDifRawBuffer, ruSize - idStart + 1);
    uint difId = pDifPtr->getID();

    int tag = 0;
    // Cerenkov dif in 12/2014 = 1; 3 afterwards
    if ( difId == 1 || difId == 3 )
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

      streamlog_out( DEBUG ) << " - Hit in Dif : " << pDifPtr->getID() << "\t NFrames : " <<  pDifPtr->getNumberOfFrames() << std::endl;
      for (uint32_t i = 0; i < pDifPtr->getNumberOfFrames(); i++)
      {
        streamlog_out( DEBUG ) << " - FrameTime : " << pDifPtr->getFrameTimeToTrigger(i) << std::endl;
        for (uint32_t j = 0; j < 64; j++)
        {
          if (pDifPtr->getFrameLevel(i, j, 0))
          {
            streamlog_out( DEBUG )  << " - FrameLevel0 - i: " << i << " j: " << j << std::endl;
            tag += 1;
          }
          if (pDifPtr->getFrameLevel(i, j, 1))
          {
            streamlog_out( DEBUG )  << " - FrameLevel1 - i: " << i << " j: " << j << std::endl;
            tag += 2;
          }
        }
      }
    }
    if ( 0 != tag)
      streamlog_out( DEBUG )  << " - Tag : " << tag << std::endl;


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
// void StreamoutProcessor::clearVec()
// {
//   for(std::map<int,std::vector<caloobject::CaloHit*> >::iterator it=hitMap.begin(); it!=hitMap.end(); ++it)
//     for( std::vector<caloobject::CaloHit*>::iterator jt=(it->second).begin(); jt!=(it->second).end(); ++jt)
//       delete *(jt);

//   hitMap.clear();
//   _efficiency.clear();
//   _effEnergy.clear();
//   _multiplicity.clear();
//   _chi2.clear();
// }


//-------------------------------------------------------------------------------------------------
// void StreamoutProcessor::check( LCEvent * evt ) {
//   // nothing to check here - could be used to fill checkplots in reconstruction processor
// }


//-------------------------------------------------------------------------------------------------
void StreamoutProcessor::end() {
  delete m_pLCStreamoutWriter;

  // delete algo_Cluster;
  // delete algo_ClusteringHelper;
  // delete algo_Tracking;
  // delete algo_InteractionFinder;
  // delete algo_Efficiency;

  // for(std::vector<caloobject::CaloLayer*>::iterator it=layers.begin(); it!=layers.end(); ++it)
  //   delete (*it);
  // layers.clear();

  // rootFile->Write();
  // rootFile->Close();
}
