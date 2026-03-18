# FastUMI Touch Python SDK

The official Python SDK for FastUMITouch robotic arms. Enabling high-precision joint control, end-effector pose manipulation, and seamless gripper management via CAN bus communication.

## Introduction

FastUMITouch Python SDK is designed to provide a lightweight, high-performance interface for controlling FastUMITouch robotic arms. Whether you are developing complex automation tasks or performing real-time servo control, our SDK offers

1 High Precision: Real-time trajectory planning with multi-polynomial interpolation.

2 Developer-Friendly API: Intuitive methods for both joint-space and Cartesian-space control.

3 Flexible Control Modes: Seamless switching between planned trajectory movements and raw servo streaming.




## Hardware Overview

| Feature            | Specification                          |
|--------------------|----------------------------------------|
| Degrees of Freedom | 6 DOF                                  |
| Communication      | CAN Bus (1 Mbps)                       |
| Control Frequency  | 400HZ                                  |
| OS Support         | Linux (Ubuntu 20.04/22.04 recommended) |
| Power Supply       | 24V DC                                 |
| Weight             | 5kg                                    |
| Arm length         | 600mm                                  |
| Payload capacity   | 3kg                                    |

## Installation

### 1.clone the git

```bash
git clone https://github.com/BestManRobotics/BestMan_FastUMI_Touch.git
cd BestMan_FastUMI_Touch
```

### 2.create a conda environment

```bash
conda create -n FastUMITouch python=3.10
conda activate FastUMITouch
```

### 3.install CAN tools and dependencies

```bash
sudo apt-get install can-utils
sudo apt-get install liborocos-kdl-dev
sudo apt-get install pybind11-dev
```

### 4.install SDK

```bash
#comman installation
pip install .

# or editable mode installation (for modifying source code)
pip install -e .
```

### 5. Activate CAN Interface



**Single arm：**
```bash
sudo ip link set can0 up type can bitrate 1000000
```

**Two arms：**
```bash
sudo ip link set can0 up type can bitrate 1000000
sudo ip link set can1 up type can bitrate 1000000
```


Different robotic arms use different CAN interfaces (can0, can1, can2...), which are specified during initialization via the can_port parameter.

⚠️The CAN port is hot-swappable; the order of CAN0 and CAN1 settings is related to the insertion/removal order.

## Quick Start

```python
import time
from fastumitouch_sdk import FastUMITouch

# 1. Initialize the robot arm
arm = FastUMITouch(can_port="can0")

try:
    # 2. return to homing point
    arm.go_home()
    time.sleep(3.5)  # Wait for movement to complete

    # 3. Move to the target joint angle (unit: radians)
    arm.set_joint(positions=[0.2,0.0, 0.4, 0.0, 0.5, 0.0], tf=3.0)
    time.sleep(3.5)

    # 4. Get current location
    positions = arm.get_joint_positions()
    print(f"Current joint angle: {positions}")

    # 5. Control the gripper (0.0 = closed, 1.0 = fully open)
    arm.openGripper()  # or closeGripper()

finally:
    # 6. Release resources (This step is necessary!)
    arm.cleanup()
```

## API  Documentation

### initialization

```python
arm = FastUMITouch(can_port="can0")  # The default value for `can_port` is "can0"
```

### Motion control


| Feature                  | Specifiction                                      |
|--------------------------|---------------------------------------------------|
| `go_home()`  | Move to home point            |
| `set_joint(positions, tf, ctrl_hz)` | Joint Space Planning Movement  |
| `set_joint_raw(positions, velocities)`    | Joint service pass-through (no plans) |
| `set_end_effector_pose_euler(pos, euler, tf)`    | Termination position attitude control (Euler angles) |
| `set_end_effector_pose_quat(pos, quat, tf)`     | Termination position attitude control (quaternion) |


**Parameter description：**
- `positions`: List of target joint angles, length 6, in radians.
- `tf`: Movement time (seconds)
- `ctrl_hz`:Control frequency, default 400Hz
- `pos`: End position [x, y, z], in meters
- `euler`: Euler angles [roll, pitch, yaw], in radians
- `quat`:Quaternion [w, x, y, z]

### status reading

| Feature                  | Specifiction                                      |
|--------------------------|---------------------------------------------------|
| `get_joint_positions()`  | Get joint angle (np.ndarray, 6)                   |
| `get_joint_velocities()` | Get joint speed (np.ndarray, 6)                   |
| `get_joint_torques()`    | Get joint torque (np.ndarray, 6)                  |
| `get_ee_pose_euler()`    | Get the end-effector pose (Position, Euler angle) |
| `get_ee_pose_quat()`     | Get the end-effector pose (Position, Quaternion ) |

### Gripper control

| Feature  | Specifiction      |
|------|-------------------|
| `openGripper()` | Open Gripper      |
| `closeGripper()` |Close Gripper             |
| `setGripperPosition(position)` | Gripper position control with planning|
| `setGripperPosition_raw(position)` | Transparent gripper position control (0.0-1.0) |
| `get_gripper_position()` | Get the current position of the gripper         |

### Resource release

```python
arm.cleanup()  # The CAN resource must be released when the program ends.
```

## Sport mode description

### Planned movement vs. through movement

The SDK provides two control modes:

1. **Planned movement**（such `set_joint`, `set_end_effector_pose_euler`）
   - Contains time parameters `tf`
   - Generating a smooth trajectory using polynomial interpolation
   - Suitable for point relocation

2. **through movement**（such `set_joint_raw`, `set_end_effector_pose_euler_raw`）
   - No time planned
   - Directly issue instructions
   - Suitable for servo control

## Sample script

`demo/` The directory contains multiple examples.

| Document             | Fuction                            |
|----------------------|------------------------------------|
| `00_init.py`         | Initialization and reset           |
| `01_read_status.py`  | Read the status of the robotic arm |
| `02_movj.py`         | Joint space movement               |
| `03_servoj.py`       | Joint servo control                |
| `04_movp.py`         | End-effector pose control          |
| `05_servop.py`       | Terminal servo control             |
| `06_gripper_ctrl.py` | Control gripper                    |


Run the example：
```bash
python demo/02_movj.py
```

## Pay attention

1. **CAN Must be activated**：Execute before use `sudo ip link set can0 up type can bitrate 1000000`（The multi-armed system then sequentially activates can0, can1, etc.）
2. **Clean up resources**：The program must be called before it terminates. `arm.cleanup()` release CAN
3. **Sports safety**：Ensure there are no obstacles within the working range of the robotic arm.
4. **Gripper safety**：Ensure no fingers or objects are within the gripper's travel range when closing the gripper.
