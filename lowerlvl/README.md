# lowerlvl

### lowerlvl is a module that focuses on low level system applications like getting mouse data, replicating keyboards, seeing what data has been processed by the cpu for a user for a given time, and much more.

## Functions:

1. **`get_touch_keyboard()`**
2. **`replicate_keyboard(event_type, keycode)`**
3. **`get_touch_mouse()`**
4. **`replicate_mouse(event_type, posx, posy)`**
5. **`get_touch_cpu_processed_bytes(username, duration=10, interval=1)`**
6. **`see_daemons()`**

## How to use:

`get_touch_keyboard()` records keyboard data until it is stopped. It may ask for permission from 
`Settings > Privacy & Security > Accessibility`. It prints raw keyboard data (if you type 'a' it wont print 'a', it will print '0'
but it depends on the keyboard).

on `pyobjc_code.py` its the same thing but, its `listen_keyboard()`.

`replicate_keyboard()` replicates key data. It may also ask for permission from
`Settings > Privacy & Security > Accessibility`. type should be 1 or 2 (1 is key down, 2 is key up) and keycode needs a keycode.

`replicate_keyboard` on `pyobjc_code.py` has `proxy and refcon`. Those dont need a value and arent being used at all. The reason is because Quartz will raise an error if those arent there.

`get_touch_mouse()` prints mouse x and y coordinates. It also may need permission from
`Settings > Privacy & Security > Accessibility`.

`get_touch_mouse()` on `pyobjc_code.py` is the same but its name is `get_mouse_position()`.

`replicate_mouse()` replicates mouse data. You may need permission from
`Settings > Privacy & Security > Accessibility`. `type` can be in range of 1 - 7 (1 is left mouse down, 2 right mouse down, 3 is left mouse up, 4
is right mouse up, 5 is mouse moved, 6 is left mouse dragged, 7 is right mouse dragged).
`posx and posy` is mouse coordinates.

`replicate_mouse()` on `pyobjc_code.py` is the exact same.

`get_touch_cpu_processed_bytes()` returns a values based on `username, duration, and interval`. You may need permission from
`Settings > Privacy & Security > Accessibility`. `username` is just your users username, `duration` is how long you want it to run, and
`interval` is how long the program sleeps for every iteration

`get_touch_cpu_processed_bytes()` is not on `pyobjc_code.py`

`see_daemons()` return all running daemons (things that run in the background). You may need permission from
`Settings > Privacy & Security > Accessibility`

`see_daemons()` is not on `pyobjc_code.py`
