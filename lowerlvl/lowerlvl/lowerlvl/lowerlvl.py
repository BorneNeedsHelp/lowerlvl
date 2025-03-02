import time
import subprocess
import pyobjc_code


class lowerlvl:
    @staticmethod
    def get_touch_keyboard():
        return pyobjc_code.listen_keyboard()

    @staticmethod
    def replicate_keyboard(event_type, keycode):
        return pyobjc_code.replicate_key(event_type, keycode)

    @staticmethod
    def get_touch_mouse():
        return pyobjc_code.get_mouse_position()

    @staticmethod
    def replicate_mouse(event_type, posx, posy):
        return pyobjc_code.replicate_mouse(event_type, posx, posy)

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