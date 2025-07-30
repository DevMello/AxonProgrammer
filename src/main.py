import hid
import time

VENDOR_ID = 0x0471
PRODUCT_ID = 0x13aa


poll_command = [0x04, 0x8A, 0x00, 0x00, 0x04] + [0x00] * (64 - 5)

def is_servo_present(report):
    return (
        len(report) >= 6 and
        report[0] == 0x04 and
        report[1] == 0x01 and
        report[2] == 0x00 and
        report[3] == 0x01 and
        report[5] == 0x03
    )

def main():
    try:
        device = hid.device()
        device.open(VENDOR_ID, PRODUCT_ID)
        device.set_nonblocking(True)

        print("Polling servo adapter... (Ctrl+C to stop)")
        last_status = None

        while True:
            device.write(poll_command)

            time.sleep(0.05) 
            report = device.read(64)

            if report:
                if is_servo_present(report):
                    if last_status != "plugged":
                        print("✅ Servo is PLUGGED in")
                        last_status = "plugged"
                else:
                    if last_status != "not":
                        print("❌ Servo is NOT plugged in")
                        last_status = "not"

            time.sleep(0.4)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()