import os
import cv2
import glob
import numpy as np
import random

def colorjitter(img, cj_type="b"):
    '''
    ### Different Color Jitter ###
    img: image
    cj_type: {b: brightness, s: saturation, c: constast}
    '''
    if cj_type == "b":
        # value = random.randint(-50, 50)
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50]))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            v[v > lim] = 255
            v[v <= lim] += value
        else:
            lim = np.absolute(value)
            v[v < lim] = 0
            v[v >= lim] -= np.absolute(value)

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
    
    elif cj_type == "s":
        # value = random.randint(-50, 50)
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50]))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            s[s > lim] = 255
            s[s <= lim] += value
        else:
            lim = np.absolute(value)
            s[s < lim] = 0
            s[s >= lim] -= np.absolute(value)

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
    
    elif cj_type == "c":
        brightness = 10
        contrast = random.randint(40, 100)
        dummy = np.int16(img)
        dummy = dummy * (contrast/127+1) - contrast + brightness
        dummy = np.clip(dummy, 0, 255)
        img = np.uint8(dummy)
        return img


def filters(img, f_type = "blur"):
    '''
    ### Filtering ###
    img: image
    f_type: {blur: blur, gaussian: gaussian, median: median}
    '''
    if f_type == "blur":
        image=img.copy()
        fsize = 3
        return cv2.blur(image,(fsize,fsize))
    
    elif f_type == "gaussian":
        image=img.copy()
        fsize = 3
        return cv2.GaussianBlur(image, (fsize, fsize), 0)
    
    elif f_type == "median":
        image=img.copy()
        fsize = 3
        return cv2.medianBlur(image, fsize)


if __name__ == "__main__":
    # Create Output Folder
    dir_path = f"augmentation"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # move to folder contains images
    os.chdir("/content/images")
    for file in glob.glob("*.png"):
        image = cv2.imread(file)
        img_name = file.split('.')[0]
        # ColorJitter
        b_img = colorjitter(image, cj_type="b")
        s_img = colorjitter(image, cj_type="s")
        c_img = colorjitter(image, cj_type="c")
        cv2.imwrite(f"{dir_path}/{img_name}_brightness.png", b_img)
        cv2.imwrite(f"{dir_path}/{img_name}_saturation.png", s_img)
        cv2.imwrite(f"{dir_path}/{img_name}_contrast.png", c_img)

        # Filtering
        blur_img = filters(image, f_type = "blur")
        cv2.imwrite(f"{dir_path}/{img_name}_blur.png", blur_img)

        print(f"Generating {file} Done!")
