# IPM

### 1. GetIPMImage.py
   * Main file to run
   * Where parameters currently need to be adjusted manually
      * Focal Length (unit: pixel)
      * Camera Height
      * Pitch
      * Yaw
      * Roll
      * left, right, top, bottom (the road range in the photo that needs to be used for IPM)
     ![](https://i.imgur.com/DtMI4rl.png)
   * The current resolution of OutImage is tentatively 640*640. If the aspect ratio of the top view is wrong, you can manually adjust the length and width of the output image.
     
### 2. GetVanishingPoint.py
   * It is used to find the vanishing point of the road (more suitable for photos with road ends). The purpose is to automatically find the top position, but I currently feel that the calculated results are not good, and I am trying new methods.

### 3. TransformImage2Ground.py
   * is used to find the relative positions of left, right, top, and bottom in world coordinates

### 4. TransformGround2Image.py
   * is used to find where each point in the original image that will be converted into a top view is located for coloring.

### 5. Example

   * #### road1
   ![](https://i.imgur.com/LdMTRGC.jpg)
   ![](https://i.imgur.com/l9qXDfG.png)
   ![](https://i.imgur.com/keOZYuY.png)
   * #### road2 
   ![](https://i.imgur.com/v2gTZ2Q.jpg)
   ![](https://i.imgur.com/nsHP6xo.png)
   ![](https://i.imgur.com/MMzzuOz.png)
   * #### road3
   ![](https://i.imgur.com/5lmKS2Q.jpg)
   ![](https://i.imgur.com/PE3705Q.png)
   ![](https://i.imgur.com/fXyihaJ.png)




## Reference
1. IPM
    * https://blog.csdn.net/monk1992/article/details/83780999
    * https://blog.csdn.net/yeyang911/article/details/51915348
    * https://sites.google.com/site/yorkyuhuang/home/research/computer-vision-augmented-reality/ipm
2. AutoStitch64
    * http://matthewalunbrown.com/autostitch/autostitch.html
