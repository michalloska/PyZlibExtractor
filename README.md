```
$$$$$$$\            $$$$$$$$\ $$\ $$\ $$\       $$$$$$$$\             $$\                                    $$\                         
$$  __$$\           \____$$  |$$ |\__|$$ |      $$  _____|            $$ |                                   $$ |                        
$$ |  $$ |$$\   $$\     $$  / $$ |$$\ $$$$$$$\  $$ |      $$\   $$\ $$$$$$\    $$$$$$\  $$$$$$\   $$$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  
$$$$$$$  |$$ |  $$ |   $$  /  $$ |$$ |$$  __$$\ $$$$$\    \$$\ $$  |\_$$  _|  $$  __$$\ \____$$\ $$  _____|\_$$  _|  $$  __$$\ $$  __$$\ 
$$  ____/ $$ |  $$ |  $$  /   $$ |$$ |$$ |  $$ |$$  __|    \$$$$  /   $$ |    $$ |  \__|$$$$$$$ |$$ /        $$ |    $$ /  $$ |$$ |  \__|
$$ |      $$ |  $$ | $$  /    $$ |$$ |$$ |  $$ |$$ |       $$  $$<    $$ |$$\ $$ |     $$  __$$ |$$ |        $$ |$$\ $$ |  $$ |$$ |      
$$ |      \$$$$$$$ |$$$$$$$$\ $$ |$$ |$$$$$$$  |$$$$$$$$\ $$  /\$$\   \$$$$  |$$ |     \$$$$$$$ |\$$$$$$$\   \$$$$  |\$$$$$$  |$$ |      
\__|       \____$$ |\________|\__|\__|\_______/ \________|\__/  \__|   \____/ \__|      \_______| \_______|   \____/  \______/ \__|      
          $$\   $$ |                                                                                                                     
          \$$$$$$  |                                                                                                                     
           \______/                                                                                                                      
```


A simple Python script made for quick .zlib archive extraction. Relies on the zlib-flate program (part of the qpdf package) 

# What can this script do?
It can export: 
* a single .zlib archive into a .txt or .log file
* multiple .zlib archives into a .txt or .log file

Example input files:
```
log_archive.1.zlib
log_archive.2.zlib
log_archive.3.zlib
log_archive.4.zlib
log_archive.5.zlib
log_archive.6.zlib
log_archive.7.zlib
log_archive.8.zlib
log_archive.9.zlib
```

Example output file:
```
extracted_logs.log
```

# Preconditions

1. Install qpdf package:

> sudo apt install qpdf

# How to use?

Use the -h/--help flag to display help with usage examples