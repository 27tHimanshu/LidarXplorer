import os

def beep_alert():
    """Play a beep sound for alerts."""
    try:
        import winsound
        winsound.Beep(1000, 500)
    except:
        print("Beep not supported on this platform.")