# function [ xyLimits ] = TransformImage2Ground( uvLimits,cameraInfo )
def TransformImage2Ground(uvLimits, cameraInfo):
    """
    Transforms UV limits from perspective image space to ground coordinates.

    Args:
    - uvLimits: numpy array, UV limits in perspective image space (2xN)
    - cameraInfo: object, containing camera parameters (focal lengths, optical center, rotation angles)

    Returns:
    - xyLimits: numpy array, transformed XY limits in ground coordinates (2xN)
    """
    import numpy as np
    from math import sin, cos, pi

    # Extract dimensions of uvLimits array
    row, col = uvLimits.shape[0:2]

    # Initialize array to hold UV limits with extra row for homogeneous coordinates
    inPoints4 = np.zeros((row + 2, col), np.float32)

    # Copy UV limits into the first two rows of inPoints4
    inPoints4[0:2] = uvLimits

    # Set the third row of inPoints4 to [1, 1, 1, 1] to represent homogeneous coordinates
    inPoints4[2] = [1, 1, 1, 1]

    # Extract only the first three rows of inPoints4 (for calculation purposes)
    inPoints3 = np.array(inPoints4)[0:3, :]

    # Calculate trigonometric functions of camera rotation angles
    c1 = cos(cameraInfo.pitch * pi / 180)
    s1 = sin(cameraInfo.pitch * pi / 180)
    c2 = cos(cameraInfo.yaw * pi / 180)
    s2 = sin(cameraInfo.yaw * pi / 180)

    # Define transformation matrix (matp) based on camera parameters
    matp = [
        [-cameraInfo.cameraHeight * c2 / cameraInfo.focalLengthX,
         cameraInfo.cameraHeight * s1 * s2 / cameraInfo.focalLengthY,
         (cameraInfo.cameraHeight * c2 * cameraInfo.opticalCenterX / cameraInfo.focalLengthX)
         - (cameraInfo.cameraHeight * s1 * s2 * cameraInfo.opticalCenterY / cameraInfo.focalLengthY)
         - (cameraInfo.cameraHeight * c1 * s2)],
        [cameraInfo.cameraHeight * s2 / cameraInfo.focalLengthX,
         cameraInfo.cameraHeight * s1 * c2 / cameraInfo.focalLengthY,
         (-cameraInfo.cameraHeight * s2 * cameraInfo.opticalCenterX
          / cameraInfo.focalLengthX) - (cameraInfo.cameraHeight * s1 * c2
                                        * cameraInfo.opticalCenterY / cameraInfo.focalLengthY)
         - (cameraInfo.cameraHeight * c1 * c2)],
        [0, cameraInfo.cameraHeight * c1 / cameraInfo.focalLengthY,
         (-cameraInfo.cameraHeight * c1 * cameraInfo.opticalCenterY / cameraInfo.focalLengthY)
         + cameraInfo.cameraHeight * s1],
        [0, -c1 / cameraInfo.focalLengthY,
         (c1 * cameraInfo.opticalCenterY / cameraInfo.focalLengthY) - s1]
    ]

    # Perform matrix multiplication to obtain transformed points in homogeneous coordinates
    inPoints4 = np.array(matp).dot(np.array(inPoints3))

    # Extract the fourth row of inPoints4 (homogeneous coordinate divisor)
    inPointsr4 = inPoints4[3, :]

    # Divide the first two rows of inPoints4 by the divisor to obtain final XY limits
    inPoints4[0, :] = inPoints4[0, :] / inPointsr4
    inPoints4[1, :] = inPoints4[1, :] / inPointsr4

    # Extract only the first two rows of inPoints4 (final XY limits)
    inPoints2 = inPoints4[0:2, :]

    # Set the transformed XY limits as the output
    xyLimits = inPoints2

    return xyLimits
