# Javlibrary Bot

Use this poorly written Python bot to build your local Javlibrary.

## How to use

- Import the SQL file provided and modify the MySQL section in javlibrary.py
- Run javlibrary.py

## What you need

- Python 3
- A MySQL server
- 15 GB of free space to store images
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)
- [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup)

If you have both Python 2 and Python 3 installed make sure you use the correct pip.
```bash
dpkg -L python3-pip | tail -n 1
```
Then solve dependencies using the correct one.

## How it work

```
+-------------+                       +----------+             
| MAIN THREAD |                       | PROGESS  |             
+-------------+                       | SAVEFILE | <--+        
|                                     +----------+    |        
+-----------------+                   RESTORE PROGRESS ON START
| LOTS OF WORKERS |                   SAVE PROGRESS EVERY 60SEC
+--+--------------+                                   |        
   |                                                  |        
   +-> Get URL from pool <----------+ +----------+    |        
   |    +                             |          |    |        
   |    +-> Mark scanned +--------+   | URL POOL | <--+        
   |                              |   |          |    |        
   |                         +------> +----------+    |        
   +-> Extract all links     |    |                   |        
   |    +                    +    |   +----------+    |        
   |    +-> Select what we need   |   |          |    |        
   |                              |   | SCANNED  |    |        
   |                              +-> | URL POOL | <--+        
   +-> Extract all contents           |          |             
        +                             +----------+             
        +-> Save in database                                   
        |                                                      
        +-> Download images +-------> +--------+-> AAA-001     
                                      | IMAGES |               
                                      +----------> AAA-002     
                                               |               
                                               +-> ABC-123     
                                               |               
                                               +-> ...         
```

## Bugs

Need to suppress lots of database related errors:
- pymysql.err.InternalError: (1205, 'Lock wait timeout exceeded; try restarting transaction')