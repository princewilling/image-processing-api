import cv2
import matplotlib.pyplot as plt

def edges(input_image):
    # read the image
    image = cv2.imread(input_image)

    # convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # perform the canny edge detector to detect image edges
    edges = cv2.Canny(gray, threshold1=30, threshold2=100)

    # save the detected edges
    plt.imsave(f"images/edge/edge_{input_image.split('/')[2]}", edges)
    return f"images/edge/edge_{input_image.split('/')[2]}"
