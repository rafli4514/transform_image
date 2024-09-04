# import packages
import numpy as np
import cv2

def order_points(pts):
    # inisialisasi list dari koordinat yang akan diurutkan
    # yang di mana entri pertama dalam list di  kiri atas
    # entry kedua di kanan atas, entry ketiga berada di kanan bawah
    # dan entry keempat berada di kiri bawah

    rect = np.zeros((4, 2), dtype = "float32")

    # titik kiri atas akan mempunyai penjumlahan terkecil, sedangkan
    # titik kanan bawah akan mempunyai penjumlahan terbesar
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # sekarang, menghitung selisih antara titik
    # pada titik kanan atas akan mempunyai selisih terkecil, sedangkan
    # titik kiri bawah akan mempunyai selisih terbesar
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return koordinat
    return rect

def four_point_transform(image, pts):
    # dapatkan urutan poin yang konsisten dan uraikan 
    # secara individu
    rect = order_points(pts)
    
    # tl = top-left
    # tr = top-right
    # br = bottom-right
    # bl = bottom-left
    (tl, tr, br, bl) = rect

    # hitung lebar gambar baru, yang akan menjadi
    # jarak maksimum antara bottom-right dan bottom-left
    # x-koordinat atau top-right dan top-left x-koordinat
    # Rumus euclidean distance
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # hitung lebar gambar baru, yang akan menjadi
    # jarak maksimum antara top-right dan bottom-left
    # y-koordinat atau top-right dan bottom-left y-koordinat
    # Rumus euclidean distance
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # sekarang yang kita punya dimensi gambar baru
    # buatkan set titik tujuan untuk mendapatkan "birds eye view"
    # (alias tampilan dari atas ke bawah) gambar, 
    # sekali lagi menentukan titik di top-left, 
    # top-right, bottom-right, and bottom-left
    dst = np.array([
	[0, 0],
	[maxWidth - 1, 0],
	[maxWidth - 1, maxHeight - 1],
	[0, maxHeight - 1]], dtype = "float32")

    # hitung matrix transform perspektif lalu apply
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return gambar warped
    return warped