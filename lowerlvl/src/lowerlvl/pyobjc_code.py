import Quartz.CoreGraphics as CG
import subprocess

def key_event(proxy, event_type, event, refcon):
    if event_type in (CG.kCGEventKeyDown, CG.kCGEventKeyUp):
        keycode = CG.CGEventGetIntegerValueField(event, CG.kCGKeyboardEventKeycode)
        print(keycode)
    return event

def replicate_key(type, keycode):
    if type == 1:
        is_down = True
    elif type == 2:
        is_down = False
    else:
        raise Exception('must be in range of 1 - 2')

    event = CG.CGEventCreateKeyboardEvent(None, keycode, is_down)
    CG.CGEventPost(CG.kCGHIDEventTap, event)

def listen_keyboard():
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

def replicate_mouse(type, posx, posy):
    if type == 1:
        down_event = CG.CGEventCreateMouseEvent(None, CG.kCGEventLeftMouseDown, (posx, posy), CG.kCGMouseButtonLeft)
        up_event = CG.CGEventCreateMouseEvent(None, CG.kCGEventLeftMouseUp, (posx, posy), CG.kCGMouseButtonLeft)
        CG.CGEventPost(CG.kCGHIDEventTap, down_event)
        CG.CGEventPost(CG.kCGHIDEventTap, up_event)
        return

    elif type == 2:
        down_event = CG.CGEventCreateMouseEvent(None, CG.kCGEventRightMouseDown, (posx, posy), CG.kCGMouseButtonRight)
        up_event = CG.CGEventCreateMouseEvent(None, CG.kCGEventRightMouseUp, (posx, posy), CG.kCGMouseButtonRight)
        CG.CGEventPost(CG.kCGHIDEventTap, down_event)
        CG.CGEventPost(CG.kCGHIDEventTap, up_event)
        return

    elif type == 3:
        event_type = CG.kCGEventLeftMouseUp
        button = CG.kCGMouseButtonLeft
    elif type == 4:
        event_type = CG.kCGEventRightMouseUp
        button = CG.kCGMouseButtonRight
    elif type == 5:
        event_type = CG.kCGEventMouseMoved
        button = 0
    elif type == 6:
        event_type = CG.kCGEventLeftMouseDragged
        button = CG.kCGMouseButtonLeft
    elif type == 7:
        event_type = CG.kCGEventRightMouseDragged
        button = CG.kCGMouseButtonRight
    else:
        raise Exception('type must be in range of 1 - 7')

    event = CG.CGEventCreateMouseEvent(None, event_type, (posx, posy), button)
    CG.CGEventPost(CG.kCGHIDEventTap, event)


def get_mouse_position():
    event = CG.CGEventCreate(None)
    location = CG.CGEventGetLocation(event)
    return location.x, location.y