# CompressedCrack

Compressed Crack is a simple tool to help you crack password zip and rar files.

Author: Thanh Minh

## Requirements:

[Python 3.x](https://www.python.org/downloads/)

## Install

```
apt-get -y install git
git clone https://github.com/thanhminh6996/CompressedCrack.git
cd ./CompressedCrack
```
## Use
```
python crack.py -i INPUT [rules [rules ...]]

positional arguments:
  rules                 <min> <max> <character>

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Insert the file path of compressed file
                        
```                       

## Example:
### Without Rules:
![Alt](https://s3-ap-southeast-1.amazonaws.com/kipalog.com/yzxax7vwym_1.png)

### With Rules:
![Alt](https://s3-ap-southeast-1.amazonaws.com/kipalog.com/mjj8814d1n_3.png)
