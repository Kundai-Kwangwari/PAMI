**[CLICK HERE](index.html)** to access the PAMI manual.

# Theoretical representation

 A temporal database is a collection of transactions and their associated timestamps.  
 A sample temporal database generated from the set of items, I={a,b,c,d,e,f}, is shown in below table:
   
   TID |  Timestamp | Transactions 
     --- | ----- | ---
     1  | 1  | a, b, c
     2  | 2 | d, e
     3  | 5 | a, e, f
     4  | 5 | d, f, g  

### Rules to create a temporal database
1. Since TID of a transaction implicitly represents the row number, this information can be ignored to save space.
1. The first column of every transaction must represent a timestamp. 
1. The timestamp of the first transaction must always be 1. The timestamps of remaining transactions follow thereafter. 
   In other words, the timestamps in a temporal database must be relative to each other, rather than absolute timestamps.
1. Irregular time gaps can exist between the transactions.
1. Multiple transactions can have a same timestamp. In other words, multiple transactions can occur at a particular timestamp.

### Temporal database format
The PAMI library requires every transaction in a temporal database to exist in the following format:

      timestamp<sep>item1<sep>item2<sep>...<sep>itemN
      An example:

        1   a   b   c
        2   d   e
        5   a   e   f
        5   d   f   g

**Note:**
1. The default separator, i.e., \<sep>, used in PAMI is tab space (or \t). However, the users can override the default 
   separator with their choice. Since spatial objects, such as Point, Line, and Polygon, are represented using space 
   and comma, usage of tab space facilitates us to effectively distinguish the spatial objects.
1. In a temporal database, items can be represented as integers or strings.
1. The timestamps must exist as integers.

### Example: finding periodic-frequent patterns in a transactional database using PFP-growth++
1. Execute the following command if PAMI was not installed in your machine.
   
         pip install pami
   
1. [Click here](https://www.u-aizu.ac.jp/~udayrage/datasets/temporalDatabases/temporal_T10I4D100K.csv) to download the synthetic T10I4D100K temporal database.
1. Move the downloaded 'temporal_T10I4D100K.csv' file  into a directory, say /home/userName.
1. Change your present working directory to /home/userName
1. Copy and paste the below code in a python file, say testPAMI.py
   
   ```Python
   from PAMI.periodicFrequentPattern.basic import PFPGrowthPlus as alg
  
   inputFile = '/home/userName/temporal_T10I4D100K.csv' 
   outputFile = '/home/userName/temporalPatterns.txt'
   minSup = 10.0   # 10 percentage of the transactions
   maxPer = 1.0    # 1 percentage of the transactions
   
   obj = alg.PFPGrowthPlus(inputFile, minSup, maxPer) 
   
   #use obj = alg.fpGrowth(inputFile, minSup,sep=',')  to override the default tab space separator with comma
   obj.startMine()  #start the mining process
   obj.savePatterns(outputFile)      #store the generated patterns in a file
      

   ```
1. Execute the testPAMI.py file by typing the following command
      python3 testPAMI.py
1. After the successful execution, users will find the generated patterns in temporalPatterns.txt file
