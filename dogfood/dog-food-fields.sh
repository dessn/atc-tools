#!/bin/sh

# Fields from 6231-v3 "Supernova Field Locations" by D'Andrea and Gupta.
# [20130125 http://des-docdb.fnal.gov:8080/cgi-bin/ShowDocument?docid=6231]
# From the same document "for reference, one can approximately represent the
# DECam footprint as an ellipse with semi-major horizontal axis of 1.084
# degrees and a semi-minor vertical axis of 0.981 degrees."  We use the
# ellipse definition here.

atc.py delete field SN-C1
atc.py delete field SN-C2
atc.py delete field SN-C3
atc.py delete field SN-E1
atc.py delete field SN-E2
atc.py delete field SN-S1
atc.py delete field SN-S2
atc.py delete field SN-X1
atc.py delete field SN-X2
atc.py delete field SN-X3

atc.py create field --units=sexagesimal -- SN-C1 03:37:05.83 -27:06:41.8 1.084 0.981
atc.py create field --units=sexagesimal -- SN-C2 03:37:05.83 -29:05:18.2 1.084 0.981
atc.py create field --units=sexagesimal -- SN-C3 03:30:35.62 -28:06:00.0 1.084 0.981
atc.py create field --units=sexagesimal -- SN-E1 00:31:29.86 -43:00:34.6 1.084 0.981
atc.py create field --units=sexagesimal -- SN-E2 00:38:00.00 -43:59:52.8 1.084 0.981
atc.py create field --units=sexagesimal -- SN-S1 02:51:16.80 +00:00:00.0 1.084 0.981
atc.py create field --units=sexagesimal -- SN-S2 02:44:46.66 -00:59:18.2 1.084 0.981
atc.py create field --units=sexagesimal -- SN-X1 02:17:54.17 -04:55:46.2 1.084 0.981
atc.py create field --units=sexagesimal -- SN-X2 02:22:39.48 -06:24:43.6 1.084 0.981
atc.py create field --units=sexagesimal -- SN-X3 02:25:48.00 -04:36:00.0 1.084 0.981
