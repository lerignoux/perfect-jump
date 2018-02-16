# Perfect-jump
A tool to make perfect jumps in 跳一跳 a wechat mini game.

## tldr
```
# connect your device with adb
play.py
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
