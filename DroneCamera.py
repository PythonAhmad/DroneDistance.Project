# ============================================================================
#  Name        : DroneCamera.py
#  Author      : Ahmad Parvaresh
#  Version     : V0.1
#  Copyright   : Free
#  Description : Calculating distance of camera from drone
#  Date        : Jan, 2022
# ============================================================================

import cv2, json, math

def readJson(jsonPath):
    with open(jsonPath) as f:
        data = json.load(f)
    return data

def droneOrientation(data,ind):    
    # Drone positions
    # (x1,y1)---------------------------------(x2,y1)
    # -----------------------------------------------
    #  ...                                      ...
    # -----------------------------------------------
    # (x1,y2)---------------------------------(x2,y2)

    x2= data[ind]['rects'][0]['x2']  # right x coordinate of the bounding rectangle
    y1= data[ind]['rects'][0]['y1']  # top y coordinate
    x1= data[ind]['rects'][0]['x1']  # left x coordinate
    y2= data[ind]['rects'][0]['y2']  # bottom y coordinate
    droneClass =  data[ind]['rects'][0]['class']
    droneData = [x1,x2,y1,y2,droneClass]
    return droneData

def droneImage(imgPath,droneOrient):

    image = cv2.imread(imgPath)
    window_name = 'Image'
    start_point = (droneOrient[0], droneOrient[2])
    end_point = (droneOrient[1], droneOrient[3])
    color = (255, 0, 0)
    thickness = 2
    image = cv2.rectangle(image, start_point, end_point, color, thickness)

    W = image.shape[1]
    H = image.shape[0]
    imgSize = [W,H]

    # Displaying the image
    # cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return imgSize

def distanceCalculation(imgSize, droneOreint):
    
    # DWR = Drone Width in Reality (m)
    if droneOreint[4]   == 'MAVIC':
        DWR = 0.3
    elif droneOreint[4] == 'PHANTOM':
        DWR = 0.35
    elif droneOreint[4] == 'INSPIRE':
        DWR = 0.5

    # DWI = Drone Width in Image (pixel)
    DWI = droneOreint[1] - droneOreint[0]
    
    FOV_H = 2  # deg
    FOV_V = 1  # deg

    # conver deg to radian
    FOV_H = math.radians(FOV_H/2)

    # D = Distance of Camera from Drone 
    D = (DWR*imgSize[0])/(DWI*2*float(math.tan(FOV_H)))
    
    return D

def addJson(data,ind,D):
    data[ind]['rects'][0]['Distance'] = math.ceil(D)
    
    return data

def main():

    print(" ")
    jsonPath = 'DroneDistance.Project/img/annotation.json'
    imageNumber = 462

    data = readJson(jsonPath)

    for ind in range(imageNumber+1):
        if ind <10:
            imgPath = f'DroneDistance.Project/img/frame_000000{ind}.jpg'
        elif ind >=10 and ind <100:
            imgPath = f'DroneDistance.Project/img/frame_00000{ind}.jpg'
        else:
            imgPath = f'DroneDistance.Project/img/frame_0000{ind}.jpg'
        
        droneOreint = droneOrientation(data,ind)
        imgSize     = droneImage(imgPath,droneOreint)
        D           = distanceCalculation(imgSize,droneOreint)
        data        = addJson(data,ind,D)
        print(f"Distance in Image- {ind} = {math.ceil(D)} m")

    with open(jsonPath, 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    
    main()