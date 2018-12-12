# SYSC3010_M3 Final Project 
# Created By Maveric Garde, Jack Turner, Gabriel Sarwar and Sahil Sharma
Preperation of the enviroment for automated aquarium 
1: Preparing a server using mongoDB
  Step 1: download MongoDB @ https://docs.mongodb.com/manual/installation/
  -NOTE MongoDBs newer version require a 64bit OS. Older version can be used to withg a 32bit system however this
  implementation has not been built with this in mind
  
  Step 2: Install Mongo using the .msi file wizard
  
  Step 3: Create a log and log directories
    -Use your C:\ path for best results
    
  Step 4: Starting the MongoDB
    -Open a command line and type "C:\ProgramFiles\MongoDB\Server\4.0\bin\mongod.exe" --dbpath="c:\data\db"
    granted either of these paths are relative to that chosen in step 3
    
  Step 5:  Install Pymongo from https://www.python.org/downloads/ using the pip extension
  
  
  
  #Testing
  The testing of the system must always be visually comfirmed to match the results given by the software 
  Integration testing should be done by sending the test character awaitited by the arduino as well as the request from the app 
  to refresh the data
