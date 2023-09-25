dm3txt_make_forwardlook
This program is intended to smooth out boted defrag strafe demos. Defrag bots and scripts utilizing snapzones for strafes often look twitchy.
Example of twitchy original demo and smoothed demo in one video: https://youtu.be/71mwmbcti8Y
This program works along with lmpc-decompiled dm3 text and modifies yaw angles in playerstate blocks in such a way that the player always looks at the direction of horizontal speed. It requires python3 installed, or (optionally) a Jupyter notebook server. WARNING: the files made this way are not legit anymore. The player position is the same as in the original file, but the yaw viewangles are different. The main purpose of this program is to prepare demos for movies (for a smooth look).

Usage
The pipeline is the following: 1. Decompile a demo with lmpc 2. Process it with this program 3. Compile it back with lmpc

Step 2 if you use Jupyter: 1. Open the ipynb file 2. Edit file names (or absolute paths) in the 2nd and the last cell 3. Run all the cells sequentially

Step 2 if you use python3 in command line: Issue command python3 dm3txt_make_forwardlook.py <args> where <args> is one or more file names (or full paths) separated by spaces. The program will output in a file in the same folder, with the same name + _(forwardlook) right before the file extention.

Known issues
dm3 text doesn't store fields in playerstate that didn't change since the previous frame. So if there was no yaw angle change in a frame, and the previous yaw angle is bad (looking too far right or left), we might want to insert the new value for the yaw angle in this frame. However, it breaks dm3 structure, and these demos can't be compiled back usimb lmpc then. Whether it is possible to work it around (e.g. by modifying lmpc code) is unclear yet.

The dm3 text (at least, the one output by lmpc) appears to be in OpenDDL format or similar (https://en.wikipedia.org/wiki/Open_Data_Description_Language). Due to the lack of OpenDDL libraries in Python, this program doesn't parse OpenDDL, but rather reads text lines one by one. Having a library parsing this format would simplify this task.
