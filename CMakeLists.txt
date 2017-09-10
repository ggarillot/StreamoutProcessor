########################################################
# cmake file for building StreamoutProcessor
# @author Antoine Pingault
CMAKE_MINIMUM_REQUIRED(VERSION 2.6 FATAL_ERROR)
########################################################


# project name
PROJECT( StreamoutMarlin )

# project version
SET( ${PROJECT_NAME}_VERSION_MAJOR 0 )
SET( ${PROJECT_NAME}_VERSION_MINOR 1 )
SET( ${PROJECT_NAME}_VERSION_PATCH 0 )

# Require C++11
INCLUDE( CheckCXXCompilerFlag )
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
IF( COMPILER_SUPPORTS_CXX11 )
  SET (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
ELSE()
  MESSAGE( SEND_ERROR "Requires C++11 support. Please upgrade your compiler !" )
ENDIF()

### DEPENDENCIES ############################################################

FIND_PACKAGE( ILCUTIL REQUIRED COMPONENTS ILCSOFT_CMAKE_MODULES )

# load default settings from ILCSOFT_CMAKE_MODULES
INCLUDE( ilcsoft_default_settings )


FIND_PACKAGE( Marlin 1.0 REQUIRED ) # minimum required Marlin version
FIND_PACKAGE( ROOT REQUIRED )
FIND_PACKAGE( CLHEP REQUIRED ) # Required for Marlin >v1.10
FIND_PACKAGE( LCIO REQUIRED )

FOREACH( pkg LCIO ROOT Marlin CLHEP)
  IF( ${pkg}_FOUND )
    INCLUDE_DIRECTORIES( ${${pkg}_INCLUDE_DIRS} )
    LINK_LIBRARIES( ${${pkg}_LIBRARIES} )
    ADD_DEFINITIONS ( ${${pkg}_DEFINITIONS} )
    ENDIF()
ENDFOREACH()

### DOCUMENTATION ###########################################################

OPTION( INSTALL_DOC "Set to OFF to skip build/install Documentation" ON )
IF( INSTALL_DOC AND EXISTS "${PROJECT_SOURCE_DIR}/doc/CMakeLists.txt" )
    ADD_SUBDIRECTORY( ./doc )
ENDIF()



### LIBRARY #################################################################

# definitions to pass to the compiler
# ADD_DEFINITIONS( "-Wall -pedantic -Wunused-value -O2" )
# ADD_DEFINITIONS( "-Wno-long-long -Wreturn-type" )
# -Werror" )
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -pedantic -std=c++11 -O2 -Wno-effc++ -Wno-shadow")


# include directories
INCLUDE_DIRECTORIES( include )
#INSTALL_DIRECTORY( ./include DESTINATION . FILES_MATCHING PATTERN "*.h" )

# add library
AUX_SOURCE_DIRECTORY( src SRC_FILES )
ADD_SHARED_LIBRARY( ${PROJECT_NAME} ${SRC_FILES} )
INSTALL_SHARED_LIBRARY( ${PROJECT_NAME} DESTINATION ${PROJECT_SOURCE_DIR}/lib )

# display some variables and write them to cache
DISPLAY_STD_VARIABLES()

