# pyCFIP
A tool helps you to find some usable Cloudflare IP.
## How to use:
### Windows(need install Python3 first)
```
python -m pip install -r requirements.txt
python main.py
```
### Linux(Debian-based)
```
apt-get -y install python3 python3-pip
python3 -m pip install -r requirements.txt
python3 main.py
```
### macOS(need Homebrew)
```
brew install python3
python3 -m pip install -r requirements.txt
python3 main.py
```
#### Following part is only for beginners:
1. Wait for the ip list to be generated (when running the program for the first time)
2. Enter all the way
3. Wait for ip speed test
4. Manually select the best ip from the output list

## Advanced:
* Modify ranges.json to customize cloudflare ip address range(在天朝104开头的IP比较快，如需Cloudflare官方提供的完整IP范围见ranges_cf_all.json。)
* Modify ips.json to customize the ip to be tested (ignore ranges.json)

## Build:
### Windows
```
python -m pip install pyinstaller
call build.cmd
```
### Linux
```
python3 -m pip install pyinstaller
chmod +x build.sh
./build.sh
```
### macOS
Same as Linux
