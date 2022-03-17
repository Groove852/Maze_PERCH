#!/usr/bin/env python3

import os

for i in range(0,500):
    os.system('touch scanData' + str(i) + '.json')

print("WELL DONE!!!")
