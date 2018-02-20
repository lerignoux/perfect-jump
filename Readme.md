# Perfect-jump
A tool to make perfect jumps in 跳一跳 a wechat mini game.

## tldr
```
# Create or ensure you have a python3 environment/virtualenv
# install dependencies
pip install -r requirements.txt
# connect your device with adb
python play.py
```

## Android interaction.
The tool uses adb to connect to the device and play.

Simulate keypress:
```
adb shell input touchscreen swipe 100 100 100 100 500
```

Get game status:
```
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png
adb shell rm /sdcard/screen.png
```
-s device_id can be added if many devices are connected.

If you have premissions problem on your device:
```
adb kill-server
sudo adb start-server
```

## improvements:
ensure platform visibility on background could not be lost during gray scale conversion

## Distance power Computation
y 252, p 704 too low
 193 p 549 too big
330 908 too big
330 895 too big
154 436 tooo low
304 807 good
271 725 too big
243 656 too big
166 465 good
152 431 too low
185 512 good
131 379 too low
289 770 too low
213 582 too low
