# python_sockets
Simple python server using sockets.

# Config Parameters
  To configure the server you just need to create a file called "config.json" in the main folder, 
  and write a code similar to this:
  
  ```
  {
    "PORT"     : 65431,
    "MAX_SIZE" : 50,
    "TIMEOUT"  : 10,
    "FILENAME" : "PREFIX",
    "PATH"     : "database/"
  }
  ```
  
  "PORT" is the port used to connect. 
  "MAX_SIZE" is the maximum size allowed for a file to have.
  "TIMEOUT" is the maximum time in seconds the server will wait for a message.
  "FILENAME" is the preffix of the files to be created.
  "PATH" is the directory you want to save the created files

# Execute
  To run the server just type in a terminal:
  `
  python server.py
  `
  
  If you want to run a simple (and not very functional) client in order to test this you can type in another terminal:
  `
  python client.py
  `
  

# What you must deliver after the challenge is completed:

## 1) Source code of everything that was developed, whether the software is working or not;

## 2) The requirements.txt with the libraries used with the source files with pip.

## 3) Information about which libraries and versions were used
    Only python's default libraries were used.

## 4) What was the approximate time spent on the software development;
    It took me about 4-5 hours of development.
      
## 5) And last but not least, what difficulties did you face in the challenge.
    At the start I spent some time figuring out how to set up properly the sockets comunication
    especially using multiple clients. I also struggled a bit thinking in how to handle the data
    in order to break it in multiple files when the maximum size of bits is too small.
