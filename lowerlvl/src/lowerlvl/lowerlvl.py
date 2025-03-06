import time
import subprocess
import Quartz.CoreGraphics as CG
import sys
import os
import signal
import functools

def daemon_check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            PID = os.getpid()
            ppid_output = os.popen(f'ps -o ppid= -p {PID}').read().strip()
            PPID = int(ppid_output) if ppid_output else -1
        except Exception:
            PPID = '?'

        if PPID == 1:
            print('\x1b[1;31mTHIS PROGRAM CANNOT BE RUN AS A DAEMON!\x1b[0m')
            os.kill(PID, signal.SIGKILL)

        elif PPID in ('?', -1):
            times = 0
            print('\x1b[1;31mThis program cannot perform the daemon check. '
                  'Waiting until exit, or a correct PPID is found\x1b[0m')

            while True:
                print(f'\x1b[1;31mTrying {times} times...\x1b[0m')
                time.sleep(5)
                times += 1

                try:
                    PID = os.getpid()
                    ppid_output = os.popen(f'ps -o ppid= -p {PID}').read().strip()
                    PPID = int(ppid_output) if ppid_output else -1
                    if PPID not in ('?', -1):
                        print(f'\x1b[1;31mA good PPID is found! Code running after {times} attemps.\x1b[0m')
                        break

                    if PPID == 1:
                        print('\x1b[1;31mTHIS PROGRAM CANNOT BE RUN AS A DAEMON!\x1b[0m')
                        os.kill(PID, signal.SIGKILL)

                except Exception:
                    pass

        return func(*args, **kwargs)

    return wrapper

class lowerlvl:
    @staticmethod
    def daemon_check(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                PID = os.getpid()
                ppid_output = os.popen(f'ps -o ppid= -p {PID}').read().strip()
                PPID = int(ppid_output) if ppid_output else -1
            except Exception:
                PPID = '?'

            if PPID == 1:
                print('\x1b[1;31mTHIS PROGRAM CANNOT BE RUN AS A DAEMON!\x1b[0m')
                os.kill(PID, signal.SIGKILL)

            elif PPID in ('?', -1):
                times = 0
                print('\x1b[1;31mThis program cannot perform the daemon check. '
                      'Waiting until exit, or a correct PPID is found\x1b[0m')

                while True:
                    print(f'\x1b[1;31mTrying {times} times...\x1b[0m')
                    time.sleep(5)
                    times += 1

                    try:
                        PID = os.getpid()
                        ppid_output = os.popen(f'ps -o ppid= -p {PID}').read().strip()
                        PPID = int(ppid_output) if ppid_output else -1
                        if PPID not in ('?', -1):
                            print(f'\x1b[1;31mA good PPID is found! Code running after {times} attemps.\x1b[0m')
                            break

                        if PPID == 1:
                            print('\x1b[1;31mTHIS PROGRAM CANNOT BE RUN AS A DAEMON!\x1b[0m')
                            os.kill(PID, signal.SIGKILL)

                    except Exception:
                        pass

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def key_event(proxy, event, refcon):
        if event_type in (CG.kCGEventKeyDown, CG.kCGEventKeyUp):
            keycode = CG.CGEventGetIntegerValueField(event, CG.kCGKeyboardEventKeycode)
            print(keycode)
        return event

    @staticmethod
    @daemon_check
    def get_touch_keyboard():
        event_mask = (1 << CG.kCGEventKeyDown) | (1 << CG.kCGEventKeyUp)
        event_tap = CG.CGEventTapCreate(
            CG.kCGHIDEventTap,
            CG.kCGHeadInsertEventTap,
            CG.kCGEventTapOptionListenOnly,
            event_mask,
            key_event,
            None
        )

        if not event_tap:
            raise RuntimeError("Failed to create event tap. Check permissions.")

        run_loop_source = CG.CFMachPortCreateRunLoopSource(None, event_tap, 0)
        CG.CFRunLoopAddSource(CG.CFRunLoopGetCurrent(), run_loop_source, CG.kCFRunLoopCommonModes)
        CG.CGEventTapEnable(event_tap, True)

        CG.CFRunLoopRun()

    @staticmethod
    @daemon_check
    def replicate_keyboard(event_type, keycode):
        if type == 1:
            is_down = True
        elif type == 2:
            is_down = False
        else:
            raise Exception('must be in range of 1 - 2')

        event = CG.CGEventCreateKeyboardEvent(None, keycode, is_down)
        CG.CGEventPost(CG.kCGHIDEventTap, event)

    @staticmethod
    @daemon_check
    def get_touch_mouse():
        lowerlvl.DAEMON_CHECK()
        event = CG.CGEventCreate(None)
        location = CG.CGEventGetLocation(event)
        return location.x, location.y

    @staticmethod
    @daemon_check
    def replicate_mouse(event_type, posx, posy):
        lowerlvl.DAEMON_CHECK()
        if event_type == 1:
            down_event = CG.CGEventCreateMouseEvent(None, CG.kCGEventLeftMouseDown, (posx, posy), CG.kCGMouseButtonLeft)
            up_event = CG.CGEventCreateMouseEvent(None, CG.kCGEventLeftMouseUp, (posx, posy), CG.kCGMouseButtonLeft)
            CG.CGEventPost(CG.kCGHIDEventTap, down_event)
            CG.CGEventPost(CG.kCGHIDEventTap, up_event)
            return

        elif event_type == 2:
            down_event = CG.CGEventCreateMouseEvent(None, CG.kCGEventRightMouseDown, (posx, posy),
                                                    CG.kCGMouseButtonRight)
            up_event = CG.CGEventCreateMouseEvent(None, CG.kCGEventRightMouseUp, (posx, posy), CG.kCGMouseButtonRight)
            CG.CGEventPost(CG.kCGHIDEventTap, down_event)
            CG.CGEventPost(CG.kCGHIDEventTap, up_event)
            return

        elif event_type == 3:
            event_type = CG.kCGEventLeftMouseUp
            button = CG.kCGMouseButtonLeft
        elif event_type == 4:
            event_type = CG.kCGEventRightMouseUp
            button = CG.kCGMouseButtonRight
        elif event_type == 5:
            event_type = CG.kCGEventMouseMoved
            button = 0
        elif event_type == 6:
            event_type = CG.kCGEventLeftMouseDragged
            button = CG.kCGMouseButtonLeft
        elif event_type == 7:
            event_type = CG.kCGEventRightMouseDragged
            button = CG.kCGMouseButtonRight
        else:
            raise Exception('type must be in range of 1 - 7')

        event = CG.CGEventCreateMouseEvent(None, event_type, (posx, posy), button)
        CG.CGEventPost(CG.kCGHIDEventTap, event)

    @staticmethod
    def get_touch_cpu_processed_bytes(username, duration=10, interval=1):
        start_time = time.time()
        output = []
        while time.time() - start_time < duration:
            out = subprocess.check_output(f"top -U {username} -l 1 -n 0 -s 1", shell=True, text=True)
            output.append(out)
            time.sleep(interval)
        return "".join(output)

    @staticmethod
    def see_daemons():
        return subprocess.check_output('ps aux | grep -i "d$"', shell=True, text=True)