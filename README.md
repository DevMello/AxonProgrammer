
# AXON Servo Cross-Platform Programmer

The Axon servo is an amazing servo used by many FTC teams. One of the downsides of the servo is that to program it, you need a Windows laptop. For those who do not have access to one or prefer using macOS or Linux, this can be a significant limitation. This project was created to solve that exact problem. By reverse-engineering the communication between the official Windows-based Axon programmer and the USB HID device, we developed a lightweight, cross-platform Python tool. Currently all it can do is poll when the adapter has been connected, and tell whether a servo has been plugged into the adapter or not (basically nothing). 

This program is in its VERY early stages. If you have experience reverse engineering protocols for USB devices, contributions are welcome!

This project is a Python-based tool that communicates with a custom USB HID servo adapter (based on the SA33/USBBootloader) to detect whether a servo is currently connected to the adapter.

It replicates the behavior of a proprietary `.exe` tool by sending low-level HID reports to the device and interpreting its responses.

---

## 🔧 Features

- ✅ Detects when a servo is plugged into the USB adapter
- 🔄 Continuously polls the adapter for status
- ⚙️ Uses `hidapi` (via the `hid` Python package)
- 🖥️ Works on **Windows**, **Linux**, and **macOS**

---


## 🚧 Future Plans

The current version of this project only scratches the surface of what the official Axon Programming Software can do. The long-term goal is to fully recreate and extend all of its functionality — in a **free**, **open-source**, and **cross-platform** package.

Planned features include:

* 🔌 **Automatic adapter and servo detection** on all supported OSes
* 🔄 **Read/write servo configuration parameters** (PID values, direction, etc.)
* ⬆️ **Upload new firmware** directly to the servo (Continous or Positional)
* 💾 **Save and load profiles** for repeatable tuning
* 🧪 **Test mode** to control servo position or speed from the GUI
* 🔍 **Log and decode all USB traffic** for debugging and advanced development

To support these features, we will continue reverse-engineering the USB HID protocol used by the original Windows `.exe` and documenting the command structure.

---

### 🖼️ Planned GUI

A modern GUI is also in development using [PyQt6](https://pypi.org/project/PyQt6/) or [Tkinter](https://docs.python.org/3/library/tkinter.html), with features such as:

* Real-time status display (servo connected, current position, etc.)
* Interactive controls for configuration and testing
* Visual feedback and logging
* Cross-platform builds for Windows, macOS, and Linux

---

This tool is being built **by FTC teams, for FTC teams**, with the goal of making Axon servo configuration accessible to everyone, not just those with Windows laptops.

If you'd like to contribute to the protocol decoding, GUI development, or feature implementation, feel free to open an issue or pull request.

---


## 📦 Requirements

- Python 3.6+
- `hidapi` Python bindings

Install dependencies:

```bash
pip install hidapi
````

On Linux/macOS, you may also need:

```bash
sudo apt install libhidapi-libusb0  # Debian/Ubuntu
brew install hidapi                 # macOS
```

---

## 🛠️ Setup (Linux/macOS Users)

To avoid running as root, add a udev rule:

1. Create file `/etc/udev/rules.d/99-servo.rules`:

```text
SUBSYSTEM=="usb", ATTRS{idVendor}=="0471", ATTRS{idProduct}=="13aa", MODE="0666"
```

2. Reload rules:

```bash
sudo udevadm control --reload
sudo udevadm trigger
```

---

## 🚀 Usage

```bash
python servo_monitor.py
```

You will see output like:

```
Polling servo adapter... (Ctrl+C to stop)
✅ Servo is PLUGGED in
❌ Servo is NOT plugged in
```

The program sends a 64-byte HID "poll" command (`04 8A 00 00 04...`) to the adapter every 500 ms and reads its response.

---

## 🧪 How It Works

* The adapter uses a known HID interface (`VID=0x0471`, `PID=0x13aa`)

* A specific OUT report must be sent to trigger a status response:

  ```
  04 8A 00 00 04 00 00 00 ... (total 64 bytes)
  ```

* The adapter replies with a 64-byte IN report:

  * If servo is **plugged in**: `04 01 00 01 01 03 ...`
  * If servo is **not plugged**: `04 01 FA 00 01 00 ...`
