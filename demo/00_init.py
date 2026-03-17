"""
@Project: FastUMI Touch SDK
@File: arm.py
@Description: Control interface for FastUMI Touch robotic arm.
@Author: FastUMI Team
@License: Apache-2.0
"""

from fastumitouch_sdk  import  FastUMITouchArm

arm =  FastUMITouchArm(can_port="can0")
print("FastUMITouch initialized")
try:
    arm.go_home()
    print("FastUMITouch go home")
except Exception as e:
    print(f"\n运行出错: {e}")
finally:
    arm.cleanup()
    print("FastUMITouch released")