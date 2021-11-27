# cross-section
This repository containing cross-section cut and fill calculations using Python programming language. This codes is made to calculate cut and fill volume in open channel planning.

1. Input file is given in the folder that has prefix "input"
  
2. Output file is given in the folder that has prefix "output"
  
3. Here are some steps to use this program:  
&nbsp;3.1. You have to familiarize yourself with csv in input file. Parameters are given in Indonesian. There will be an update for the English version.  
&nbsp;&nbsp;&nbsp;&nbsp;3.1.1. input         = raw data from geodetic GPS, it contains of E, N, Z for each of station.  
&nbsp;&nbsp;&nbsp;&nbsp;3.1.2. input_rencana = it gives the criteria of dimension and elevation where we plan the open channel.  
&nbsp;&nbsp;&nbsp;&nbsp;3.1.3. input_acad    = it contains several parameters to draw the cross-section to AutoCAD applications.  
&nbsp;3.2.  Delete all the folder that has prefix "output"   
&nbsp;3.3.  Run main.bat to process input and produces existing cross-section based on GPS raw data.  
&nbsp;3.4.  Run main2.bat to process cut and fill volume.  
&nbsp;3.5.  Run main3.bat to make AutoCAD script.  
&nbsp;3.6.  Voila, drag .scr file from output_scr file to AutoCAD and you will get thousands of existing and planned cross-sections.  
       
