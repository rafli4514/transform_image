# import package
from transform import four_point_transform
import numpy as np
import argparse
import cv2

# Membuat dan mengonfigurasi parser argumen, lalu memproses argumen
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
ap.add_argument("-c", "--coords",
	help = "comma seperated list of source points")
args = vars(ap.parse_args())

# load gambar dan ambil koordinat sumber (list dari titik (x, y))
image = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]), dtype = "float32")

# terapkan transform 4 titik untuk mendapatkan "birds eye view" dari gambar
warped = four_point_transform(image, pts)

# tampilkan gambar original dan yang sudah di warped
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)