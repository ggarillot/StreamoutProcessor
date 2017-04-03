
#ifndef STREAMOUTPROCESSOR_H
#define STREAMOUTPROCESSOR_H


// -- Marlin headers
#include "marlin/Processor.h"

// -- lcio headers
#include "IO/LCReader.h"
#include "IO/LCWriter.h"
#include "IOIMPL/LCFactory.h"
#include "EVENT/LCCollection.h"
#include "EVENT/CalorimeterHit.h"
#include "EVENT/RawCalorimeterHit.h"
#include "UTIL/LCTOOLS.h"
#include "EVENT/LCIO.h"
#include "IMPL/LCGenericObjectImpl.h"

// -- ROOT headers
#include <TFile.h>
#include <TTree.h>
#include <TH2D.h>

// -- stl headers
#include <iostream>
#include <algorithm>

// -- Streamout headers
#include "DIFUnpacker.h"
#include "DIF.h"

class LCStreamoutWriter
{
public:
  LCStreamoutWriter(const std::string &outputFileName) :
    m_nProcessedEvent(0)
  {
    m_pLCWriter = IOIMPL::LCFactory::getInstance()->createLCWriter();
    m_pLCWriter->open( outputFileName , EVENT::LCIO::WRITE_NEW );
  }

  ~LCStreamoutWriter()
  {
    streamlog_out( MESSAGE ) << "\tNumber of reconstructed events : " << m_nProcessedEvent << std::endl;
    m_pLCWriter->close();
    delete m_pLCWriter;
  }

  void processReconstructedEvent(EVENT::LCEvent *pLCEvent)
  {
    streamlog_out( MESSAGE ) <<  " Writing rec event no " << pLCEvent->getEventNumber() << " to disk" << std::endl;

    // UTIL::LCTOOLS::dumpEvent(pLCEvent);

    m_pLCWriter->writeEvent(pLCEvent);
    m_nProcessedEvent++;
  }

private:
  unsigned int               m_nProcessedEvent;
  IO::LCWriter              *m_pLCWriter;
};

//-------------------------------------------------------------------------------------------------
//-------------------------------------------------------------------------------------------------
class StreamoutProcessor : public marlin::Processor {

public:

  virtual marlin::Processor*  newProcessor() { return new StreamoutProcessor ; }


  StreamoutProcessor() ;
  // ~StreamoutProcessor() ;

  /** Called at the begin of the job before anything is read.
   * Use to initialize the processor, e.g. book histograms.
   */
  virtual void init() ;

  /** Called for every run.
   */
  virtual void processRunHeader( LCRunHeader* run ) ;

  /** Process streamoutProcessor on the lcio event.
   *  Create a RawCalorimeterHit collection from a LCGenericObject
   *  collection of sdhcal raw dif buffers
   */
  virtual void processEvent( LCEvent * evt ) ;


  // virtual void check( LCEvent * evt ) ;

  /** Set the RU shift
   */
  void setRuShift(int ruShift);

  /** Set the collection name used as input for streamout.
   *  The input collection must be a LCGenericObject collection
   */
  void setInputCollectionName(const std::string &collectionName);

  /** Set the collection name used as output after streamout processing.
   *  The out put collection is a RawCalorimeterHit collection
   */
  void setOutputCollectionName(const std::string &collectionName);

  /** Set whether the first RU in the collection has to be dropped
   */
  void setDropFirstRU(bool drop);

  /** Set the XDAQ shift (dif ptr)
   */
  void setXDaqShift(unsigned int shift);

  /** Set whether to skip full asics (default is true)
   */
  void setSkipFullAsic(bool skip);


  /** Called after data processing for clean up.
   */
  virtual void end() ;

  // void clearVec();
protected:
  int m_nRun;
  int m_nEvt;
  int m_eventNbr;

  /** Input collection name.
   */
  std::vector<std::string> _hcalCollections;

private:
  int                m_ruShift;
  int                m_cerenkovDifId;
  int m_cerenkovOutDifId;
  int m_cerenkovOutAsicId;
  int m_cerenkovOutTimeDelay;
  int                m_xdaqShift;
  bool               m_dropFirstRU;
  bool               m_skipFullAsics;
  bool               m_isBefore2016Data;
  bool               m_shouldTreatEcal;
  std::vector<int>   m_ecalDetectorIds;
  std::string        m_runNumber;
  bool               m_drawPlots;
  std::string        m_plotFolder;

  std::string        m_processorDescription;
  std::string        m_inputCollectionName;
  std::string        m_outputCollectionName;
  std::string        m_outputFileName;

  LCStreamoutWriter *m_pLCStreamoutWriter;

  std::string        normal;
  std::string        red;
  std::string        green;
  std::string        yellow;
  std::string        blue;
  std::string        magenta;
  std::string        white;

  // ROOT
  TFile * m_rootFile;
  std::map<Int_t, TH2D*> m_mapHitPerDif;
  std::map<Int_t, TH2D*> m_mapHitPerDifFull;
  std::string m_rootFileName;
} ;

#endif  //  STREAMOUTPROCESSOR_H
