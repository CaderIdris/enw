#!/bin/bash
# ******************************************************************************
#
# Project: Demo scripts and templates for research users on NAME-on-JASMIN
#
# File:    metrestore script for use on NAME-on-JASMIN (GLOBAL and UK 1.5km met data)
#
# Author:  Andrew Jones, Atmospheric Dispersion, UK Met Office
#
# Date:    23/01/2024
#
# ******************************************************************************

# This script is designed to run with NAME on the JASMIN platform, and restores
# (or links) an archived met data file stored in the NAME-on-JASMIN met archive.
#
# It first checks for the existence of the file/link in the local met directory
# (if a local gzipped file exists then that file is unzipped), otherwise
# it searches for the met file in the main met archive. For the older gzipped
# met data, it then copies/unzips the met file to the local met directory.
# For the newer packed met data, it instead creates a link to that met file.


# Retrieve script arguments

if [[ $# -eq 2 ]] ; then
  
  METDIR=$1
  METFILENAME=$2
  
else
  
  echo "Error in script $0: two arguments METDIR and METFILENAME are needed"
  exit 1
  
fi


# Extract SUFFIX from METFILENAME

SUFFIX=`echo ${METFILENAME} | cut -f2- -d'.'`


# Set NAME Group Workspace

GWS=/gws/ssde/j25a/name


# Set top-level met archive on JASMIN

ARCHIVEROOTDIR=${GWS}/met_archive


# Set archive directory and restore method for each SUFFIX type

if   [[ ${SUFFIX} == UM1p5km_Mk4_[IM]_L57PT+([[:digit:]]).pp ]] ; then
  
  # UM1p5km_Mk4
  PT=$(echo ${SUFFIX} | cut -c20- | cut -d. -f1)
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/LimitedArea/UM1p5km_Mk4PT/PT${PT}"
  RESTORE_BY='link'
  
elif [[ ${SUFFIX} == UM1p5km_Mk3_[IM]_L57PT+([[:digit:]]).pp ]] ; then
  
  # UM1p5km_Mk3
  PT=$(echo ${SUFFIX} | cut -c20- | cut -d. -f1)
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/LimitedArea/UM1p5km_Mk3PT/PT${PT}"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == UM1p5km_Mk2_[IM]_L57PT+([[:digit:]]).pp ]] ; then
  
  # UM1p5km_Mk2
  PT=$(echo ${SUFFIX} | cut -c20- | cut -d. -f1)
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/LimitedArea/UM1p5km_Mk2PT/PT${PT}"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == UMG_Mk12_[IM]_L59PT+([[:digit:]]).pp ]] ; then

  # UMG_Mk12
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/UMG_Mk12PT"
  RESTORE_BY='link'

elif [[ ${SUFFIX} == UMG_Mk11_[IM]_L59PT+([[:digit:]]).pp ]] ; then
  
  # UMG_Mk11
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/UMG_Mk11PT"
  RESTORE_BY='link'
  
elif [[ ${SUFFIX} == UMG_Mk10_[IM]_L59PT+([[:digit:]]).pp ]] ; then
  
  # UMG_Mk10
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/UMG_Mk10PT"
  RESTORE_BY='link'
  
elif [[ ${SUFFIX} == UMG_Mk9_[IM]_L59PT+([[:digit:]]).pp ]] ; then
  
  # UMG_Mk9
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/UMG_Mk9PT"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == UMG_Mk8_[IM]_L59PT+([[:digit:]]).pp ]] ; then
  
  # UMG_Mk8
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/UMG_Mk8PT"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == UMG_Mk7_[IM]_L59PT+([[:digit:]]).pp ]] ; then
  
  # UMG_Mk7
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/UMG_Mk7PT"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == UMG_Mk6_L59PT+([[:digit:]]).pp ]] ; then
  
  # UMG_Mk6
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/UMG_Mk6PT"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == 'UMG_Mk5_L52.pp' ]] ; then
  
  # UMG_Mk5
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/UMG_Mk5"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == 'GLOUM6.pp' ]] ; then
  
  # GLOUM6pp
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/GLOUM6pp"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == 'GLOUM6' ]] ; then
  
  # GLOUM6
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/GLOUM6"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == 'GLOUM5' ]] ; then
  
  # GLOUM5
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/GLOUM5"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == 'GLOH2001' ]] ; then
  
  # GLOH2001
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/GLOH2001"
  RESTORE_BY='copy'
  
elif [[ ${SUFFIX} == 'GLOH' ]] ; then
  
  # GLOH
  ARCHIVEMETDIR="${ARCHIVEROOTDIR}/Global/GLOH"
  RESTORE_BY='copy'
  
else
  
  echo "Unknown file suffix = ${SUFFIX} in call to metrestore script"
  exit 2
  
fi


# Check ARCHIVEMETDIR directory is different to METDIR

if [[ "${ARCHIVEMETDIR}/" == ${METDIR} ]] ; then
 
 echo "!!! ERROR: THIS IS NOT ALLOWED - PLEASE CHANGE LOCAL MET DIRECTORY !!!"
 ARCHIVEMETDIR=MISTAKE
 exit 3
 
fi


# Switch to local met directory

cd ${METDIR}


# Test for presence of met file and attempt to restore from archive if necessary

METFILE=${METFILENAME}
echo "metrestore: looking for ${METFILE}"

if [[ ${RESTORE_BY} == 'copy' ]] ; then
  
  #
  # Restoring a copy in the local met directory
  #
  
  if   test -f ${METFILE}
  then
    
    # file already exists
    echo "metrestore: ${METFILE} exists"
    
  elif test -f ${METFILE}.gz
  then
    
    # gzip file already exists
    echo "metrestore: unzipping ${METFILE}.gz"
    gunzip ${METFILE}.gz
    
  elif test -f ${ARCHIVEMETDIR}/${METFILE}.gz
  then
    
    # copy met file from archive to working met directory
    echo "metrestore: copying ${METFILE}.gz from met archive"
    cp ${ARCHIVEMETDIR}/${METFILE}.gz ${METFILE}.gz
    gunzip ${METFILE}.gz
    
  else
    
    # met file not found
    echo "metrestore: ${METFILE} not found"
    exit 4
    
  fi
  
  # set file permissions on local copy for group read-write access
  chmod 664 ${METFILE}

elif [[ ${RESTORE_BY} == 'link' ]] ; then
  
  #
  # Restoring a link in the local met directory
  #
  
  if   test -L ${METFILE}
  then
    
    # link already exists
    echo "metrestore: ${METFILE} (as link) exists"
    
  elif test -f ${METFILE}
  then
    
    # file already exists
    echo "metrestore: ${METFILE} (as local file) exists"
    
  elif test -f ${ARCHIVEMETDIR}/${METFILE}
  then
    
    # create link to met file in archive
    echo "metrestore: linking to ${METFILE} in met archive"
    ln -s ${ARCHIVEMETDIR}/${METFILE} ${METFILE}
    
  else
    
    # met file not found
    echo "metrestore: ${METFILE} not found"
    exit 5
    
  fi
  
fi

exit 0
