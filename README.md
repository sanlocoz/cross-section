# cross-section
This repository is containing cut and fill calculations for cross-section using Python programming language. This codes is made to calculate cut and fill volume in open channel planning.

1. Input file is given in the folder that has prefix "input".
  
2. Output file is given in the folder that has prefix "output".
  
3. Here are some steps to use this program:  

	3.1. You have to familiarize yourself with csv in input file. Parameters are given in Indonesian. There will be an update for the English version.  
  
		3.1.1. input         = raw data from geodetic GPS, it contains of E, N, Z for each of station.  
		3.1.2. input_rencana = it gives the criteria of dimension and elevation where we plan the open channel.  
  		3.1.3. input_acad    = it contains several parameters to draw the cross-section to AutoCAD application.  
  
	3.2.  Delete all the folder that has prefix "output".
  
	3.3.  Run main.bat to process input and produces existing cross-section based on GPS raw data.  
  
	3.4.  Run main2.bat to process cut and fill volume.  
  
	3.5.  Run main3.bat to make AutoCAD script.  
  
	3.6.  Drag .scr file from output_scr file to AutoCAD and Voila you will get thousands of existing and planned cross-sections.  
       
