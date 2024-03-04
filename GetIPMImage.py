# Import necessary modules
from GetInfo import GetInfo
from GetVanishingPoint import GetVanishingPoint
from TransformImage2Ground import TransformImage2Ground
from TransformGround2Image import TransformGround2Image
import cv2
import numpy as np

# Define a class to store camera information
class Info(object):
    def __init__(self, dct):
        self.dct = dct

    def __getattr__(self, name):
        return self.dct[name]

# Specify the picture number and file details
pic = 16
file_name = 'processed_60_1705496977213150464'
file_type = '.jpg'
folder = '/home/aref/Desktop/IPM/Images/0_30_45_60/'

# Read the image
I = cv2.imread(folder + file_name + file_type)

# Extract image dimensions
R = I[:, :, :]
height = int(I.shape[0]) # number of rows (y)
width = int(I.shape[1]) # number of columns (x)

# Define camera information
cameraInfo = Info({
    "focalLengthX": 1567.9328940076439,
    "focalLengthY": 1563.5710737727954,
    "opticalCenterX": 915.9938327378984,
    "opticalCenterY": 451.13296389625447,
    "cameraHeight": 100,  # in mm
    "pitch": 60,           # rotation around x-axis
    "yaw": 0.0,            # rotation around y-axis
    "roll": 0              # rotation around z-axis
})

# Define IPM (Inverse Perspective Mapping) information
ipmInfo = Info({
    "inputWidth": width,
    "inputHeight": height,
    "left": 0,
    "right": width-1,
    "top": 0,
    "bottom": height-1
})

# Find vanishing point
vpp = GetVanishingPoint(cameraInfo)
vp_x = vpp[0][0]
vp_y = vpp[1][0]

# Update top value in IPM information
ipmInfo.top = float(max(int(vp_y), ipmInfo.top))

# Define UV limits for IPM
uvLimitsp = np.array([[vp_x, ipmInfo.right, ipmInfo.left, vp_x],
            [ipmInfo.top, ipmInfo.top, ipmInfo.top, ipmInfo.bottom]], np.float32)

# Transform UV limits to ground coordinates
xyLimits = TransformImage2Ground(uvLimitsp, cameraInfo)
row1 = xyLimits[0, :]
row2 = xyLimits[1, :]
xfMin = min(row1)
xfMax = max(row1)
yfMin = min(row2)
yfMax = max(row2)
xyRatio = (xfMax - xfMin)/(yfMax - yfMin)

# Initialize output image
outImage = np.zeros((640,960,4), np.float32)
outImage[:,:,3] = 255
outRow = int(outImage.shape[0])
outCol = int(outImage.shape[1])
stepRow = (yfMax - yfMin)/outRow
stepCol = (xfMax - xfMin)/outCol
xyGrid = np.zeros((2, outRow*outCol), np.float32)
y = yfMax-0.5*stepRow

# Generate XY grid for ground coordinates
for i in range(0, outRow):
    x = xfMin+0.5*stepCol
    for j in range(0, outCol):
        xyGrid[0, (i-1)*outCol+j] = x
        xyGrid[1, (i-1)*outCol+j] = y
        x = x + stepCol
    y = y - stepRow

# Transform ground coordinates to image coordinates
uvGrid = TransformGround2Image(xyGrid, cameraInfo)

# Calculate mean value of the image
means = np.mean(R)/255
RR = R.astype(float)/255

# Interpolate image values for the output image
for i in range(0, outRow):
    for j in range(0, outCol):
        ui = uvGrid[0, i*outCol+j]
        vi = uvGrid[1, i*outCol+j]
        if ui < ipmInfo.left or ui > ipmInfo.right or vi < ipmInfo.top or vi > ipmInfo.bottom:
            outImage[i, j] = 0.0
        else:
            x1 = np.int32(ui)
            x2 = np.int32(ui+0.5)
            y1 = np.int32(vi)
            y2 = np.int32(vi+0.5)
            x = ui-float(x1)
            y = vi-float(y1)
            outImage[i, j, 0] = float(RR[y1, x1, 0])*(1-x)*(1-y)+float(RR[y1, x2, 0])*x*(1-y)+float(RR[y2, x1, 0])*(1-x)*y+float(RR[y2, x2, 0])*x*y
            outImage[i, j, 1] = float(RR[y1, x1, 1])*(1-x)*(1-y)+float(RR[y1, x2, 1])*x*(1-y)+float(RR[y2, x1, 1])*(1-x)*y+float(RR[y2, x2, 1])*x*y
            outImage[i, j, 2] = float(RR[y1, x1, 2])*(1-x)*(1-y)+float(RR[y1, x2, 2])*x*(1-y)+float(RR[y2, x1, 2])*(1-x)*y+float(RR[y2, x2, 2])*x*y

# Set the last row of the output image to zeros
outImage[-1,:] = 0.0 

# Convert the output image to integer values (0-255) and save it
outImage = outImage * 255
print(f"{file_name} Finished.")
print(f"Height: {cameraInfo.cameraHeight},\nPitch: {cameraInfo.pitch},\nYaw: {cameraInfo.yaw},\nRoll: {cameraInfo.roll}.\n")

# Save the output image
cv2.imwrite(f'processed/p{cameraInfo.pitch}_h{cameraInfo.cameraHeight}_{file_name}.png',outImage)
