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

# Export Modes
 
## Single .zlib archive into a .txt or .log file
  </br> Single archive extract happens when `--min` or `--max` is not specified. The input_name is the literal name of the archive specified with or without the .zlib format! 
  ```
  $ export_zlib.py --input_name="log.zlib" [--output_name="extracted_logs" --path="" --txt_log_format --rm --save_preset --show_preset --delete_preset --debug]
  ```

## Multiple .zlib archives into a .txt or .log file

</br> Single archive extract happens when both `--min` and `--max` are specified.

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
Example command for the above input files:
```
$ export_zlib.py --min 1 --max 9 --input_name="log_archive" --output_file="extracted_logs.txt"
```
Example output file:
```
extracted_logs.txt
```

# Arguments
```
optional arguments:
  -h, --help            show this help message and exit
  --max MAX, --max_archive_index MAX
                        Index of the last file, when unspecified single archive extraction is assumed
  --min MIN, --min_archive_index MIN
                        Index of the first file, when unspecified single archive extraction is assumed
  --path PATH, --archives_path PATH
                        Path to the archives directory. Output will be generated in this path too. Uses CWD by default
  --txt_log_format      Use .txt format for output logs. Default is .log. This setting can be overwritten in '--
                        output_name'
  --rm, --delete_zlibs  Delete the archives after uncompressing
  --input_name INPUT_NAME
                        Input file name (with or without format specifier)
  --output_name OUTPUT_NAME
                        Output file name (when format specified it will overwrite '--txt_log_format')
  -s, --save_preset     Save current arguments as a .preset.json file under /tmp/PyZlibExtractor/. Can be used when --load_preset specified
  --load_preset         Use previously set preset. Will be used automatically next time
  --show_preset         Display preset
  --delete_preset       Delete preset file
  -d, --debug           Enable debug logs
```
## Preset location
>/tmp/PyZlibExtractor/.preset.json

To use a preset simply use:
>$ export_zlib.py --load_preset

Or use preset with extra arguments :
>$ export_zlib.py --load_preset [any argument from previous section]

Preset will not save the following arguments:
```
--save_preset
--load_preset
--show_preset
--debug
```

<h2>WARNING! --rm can be saved into preset so be careful when using</h2>

# Preconditions

1. Install qpdf package:

> sudo apt install qpdf

# How to use?

Use the -h/--help flag to display help with usage examples