import hid
import time

# Vendor ID and Product ID for Axon servo adapter
VENDOR_ID = 0x0471
PRODUCT_ID = 0x13aa

# Command to poll the servo adapter
# This is a 64-byte report, with the first 5 bytes containing the command
# and the rest padded with zeros.
poll_command = [0x04, 0x8A, 0x00, 0x00, 0x04] + [0x00] * (64 - 5)

def is_servo_present(report):
    """
    Checks if the servo is present based on the received HID report.
    This function inspects specific bytes in the report to determine
    if a servo is detected by the adapter.
    """
    return (
        len(report) >= 6 and
        report[0] == 0x04 and
        report[1] == 0x01 and
        report[2] == 0x00 and
        report[3] == 0x01 and
        report[5] == 0x03
    )

def main():
    """
    Main function to continuously monitor the servo adapter.
    It handles initial connection, maintains polling while connected,
    and gracefully manages disconnections and reconnections.
    """
    device = None
    adapter_connected = False
    last_servo_status = None

    print("Starting servo adapter monitoring... (Press Ctrl+C to stop)")

    while True:
        if not adapter_connected:
            print("Searching for servo adapter...")
            while not adapter_connected:
                try:
                    device = hid.device()
                    device.open(VENDOR_ID, PRODUCT_ID)
                    device.set_nonblocking(True)
                    adapter_connected = True
                    print("✅ Adapter connected.")
                    last_servo_status = None
                except (IOError, OSError) as e:
                    print(f"Adapter not found or accessible: {e}. Retrying in 2 seconds...")
                    time.sleep(2)
                except Exception as e:
                    print(f"An unexpected error occurred while opening the device: {e}. Retrying in 2 seconds...")
                    time.sleep(2)

        if adapter_connected:
            try:
                device.write(poll_command)
                time.sleep(0.05) 

                report = device.read(64)

                if report:
                    if is_servo_present(report):
                        if last_servo_status != "plugged":
                            print("✅ Servo is PLUGGED in")
                            last_servo_status = "plugged"
                    else:
                        if last_servo_status != "not_plugged":
                            print("❌ Servo is NOT plugged in")
                            last_servo_status = "not_plugged"

                time.sleep(0.4)

            except (IOError, OSError) as e:
                print(f"❌ Adapter disconnected: {e}")
                if device:
                    device.close()
                adapter_connected = False 
                device = None
                last_servo_status = None
                time.sleep(1)
            except Exception as e:
                print(f"An unexpected error occurred during polling: {e}")
                if device:
                    device.close()
                adapter_connected = False
                device = None
                last_servo_status = None
                time.sleep(1)

if __name__ == "__main__":
    main()
