#!/usr/bin/env python
# coding: utf-8

import sys
from math import sqrt, asin, degrees
from os import path


def set_new_yaw_angle(i, angle):
    global lines
    new_yaw_line = '   viewangles[1] {};'.format(round(angle, 6))
    if lines[i + 1][:15] == '   viewangles[0':
        if lines[i + 2][:15] == '   viewangles[1': # if both pitch and old yaw are set
            lines[i + 2] = new_yaw_line
            return
        else:                                      # if only pitch is set
            #lines.insert(i + 2, new_yaw_line)     # Adding a line breaks dm3 structure
            return
    if lines[i + 1][:15] == '   viewangles[1':     # if only yaw (old) is set
        lines[i + 1] = new_yaw_line
        return
    if lines[i][:15] == '   viewangles[1':         # if the very line is yaw change, means none of vx, vy changed
        lines[i] = new_yaw_line
        return
    #lines.insert(i + 1, new_yaw_line)             # if neither pitch nor yaw are set (adding a line breaks dm3 structure)


def set_direction_angle(i, vx=None, vy=None):
    global prev_vx, prev_vy
    vx = vx if not vx is None else prev_vx
    vy = vy if not vy is None else prev_vy
    prev_vx, prev_vy = vx, vy
    
    vxy = sqrt(vx * vx + vy * vy) # hypotenuse == XY speed
    if vxy == 0:
        return                    # No need to change yaw angle if speed == 0
    abs_yawangle = degrees(asin(abs(vy) / vxy))
    
    if vx > 0 and vy > 0:         # 1st quarter
        set_new_yaw_angle(i, abs_yawangle)
    elif vx < 0 and vy > 0:       # 2nd quarter
        set_new_yaw_angle(i, 180.0 - abs_yawangle)
    elif vx < 0 and vy < 0:       # 3rd quarter
        set_new_yaw_angle(i, -180.0 + abs_yawangle)
    elif vx > 0 and vy < 0:       # 4th quarter
        set_new_yaw_angle(i, 0.0 - abs_yawangle)
    elif vx == 0 and vy > 0:      # heading +Y
        set_new_yaw_angle(i, 90.0)
    elif vx == 0 and vy < 0:      # heading -Y
        set_new_yaw_angle(i, -90.0)
    elif vx > 0 and vy == 0:      # heading +X
        set_new_yaw_angle(i, 0.0)
    elif vx < 0 and vy == 0:      # heading -X
        set_new_yaw_angle(i, 180.0)


def iter_lines():
    global lines
    prev_vx, prev_vy = 0, 0
    for i, l in enumerate(lines):
        if l[:13] == '   velocity[0':                # If vx changed,
            if lines[i + 1][:13] == '   velocity[1': # and vy changed too
                continue                             # will process with next line.
            else:                                    # If only vx changed, call set_direction_angle with vx only.
                set_direction_angle(i=i, vx=float(l.split(' ')[-1][:-1]))
                continue
        if l[:13] == '   velocity[1':                # If vy changed
            if lines[i - 1][:13] == '   velocity[0': # and vx changed too
                set_direction_angle(i=i,             # call set_direction_angle with both vx and vy.
                                    vx=float(lines[i - 1].split(' ')[-1][:-1]),
                                    vy=float(l.split(' ')[-1][:-1]))
                continue
            else:                                    # If only vy changed, call set_direction_angle with vy only.
                set_direction_angle(i=i, vy=float(l.split(' ')[-1][:-1]))
                continue
        if l[:15] == '   viewangles[1': 
            # If yaw angle changed, but none of (vx, vy) changed (e.g. during some jumps),
            # then call set_direction_angle with prev_vx & prev_vy
            if not '   velocity' in [lines[i - 3][:11], lines[i - 2][:11], lines[i - 1][:11]]:
                set_direction_angle(i=i, vx=prev_vx, vy=prev_vy)


if __name__ == '__main__':
    # Iterate through all given filename arguments
    for dm3_txt_file in sys.argv[1:]:
        # Read file
        try:
            f = open(dm3_txt_file, 'r')
            demo_txt = f.read()
        except FileNotFoundError:
            print('File {} not found.'.format(dm3_txt_file))
            continue

        # Process lines and set new yaw angles
        print('Processing file {}... '.format(dm3_txt_file), end='')
        lines = demo_txt.split('\n')
        iter_lines()

        # Save new file
        lines_to_save = '\n'.join(lines)
        filename, extension = path.splitext(dm3_txt_file)
        file_to_save = filename + '(forwardlook)' + extension
        with open(file_to_save, 'w') as f:
            f.write(lines_to_save)
        print('Saved output as {}'.format(file_to_save))

    print('Finished successfully.')
