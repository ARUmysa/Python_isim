import torch
from facenet_pytorch import InceptionResnetV1, MTCNN, fixed_image_standardization, training
from PIL import Image, ImageDraw, ImageFont, ImageOps, ExifTags
import numpy as np
import os, glob, time, pickle
import argparse
import cv2
import os
import shutil
import piexif

ap = argparse.ArgumentParser()
ap.add_argument("-img", "--image", required=False, help="Arama yapılacak görüntü pathini giriniz.")
ap.add_argument("-d", "--dir", required=False, help="Search Directory giriniz.")
args = ap.parse_args()



main_path = 'C:/Users/cypoint_3/Desktop/kk/'

args.pickle = 'C:/Users/cypoint_3/Desktop/kk/tum.pickle'
arguman =args.pickle 
aranan_isim = 'KEMAL KILICDAROGLU'
hedef_klasor_adi = aranan_isim



kod_dizini = os.path.dirname(os.path.abspath(__file__))
print(kod_dizini,"a")
# Hedef klasör adını belirleyin
hedef_klasor_tekli = os.path.join(kod_dizini, aranan_isim, "TEKLİ")
hedef_klasor_coklu = os.path.join(kod_dizini, aranan_isim, "GRUP")



ID_imagenames = glob.glob(main_path + '/*.j*')
device = 'cpu'

#--------------------------------------------------------------#
#--------------Face Detection Pipeline Initialization----------#
#--------------------------------------------------------------#
mtcnn = MTCNN( image_size=160, margin=0, min_face_size=60, thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True, keep_all=False, device=device )
mtcnn_dir = MTCNN( image_size=160, margin=0, min_face_size=60, thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True, keep_all=True, device=device )

#--------------------------------------------------------------#
#--------------Embedding Generator Pipeline--------------------#
#--------------------------------------------------------------#
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
xback = []
label_images = []


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dir", required=False, help="test Image pathi giriniz, JPG/PNG resim...")
ap.add_argument("-p", "--pickle", required=False, help="Pickle dosya pathini giriniz")
args = ap.parse_args()
score=0.65


def add_metadata_to_image(img_al, comment):
    # Exif verilerini yükle
    exif_data = piexif.load(img_al)

    # ImageDescription alanını güncelle
    exif_data['0th'][piexif.ImageIFD.ImageDescription] = comment

    # Exif verilerini yeniden kaydet
    exif_bytes = piexif.dump(exif_data)
    piexif.insert(exif_bytes, img_al)
    print("veri eklenedi")

def pickle_oku (args1,isim):
    with open( arguman, 'rb') as handle:
            veriler = pickle.load(handle)

   
    indexsignatures = []
    for veri in veriler:
        if veri['ID'] == aranan_isim:
            aranan_vektor = veri['signature']
            print(veri['ID'],aranan_vektor)
            #print("buldum",veri['ID'] )
            #print("array",aranan_vektor)
            break
    else:
        print("İstenen isim bulunamadı.")
    return(aranan_vektor)

np_indexsignatures=pickle_oku(arguman,aranan_isim)
for i, filename in enumerate(ID_imagenames):
    test_im = Image.open(filename)
    detected_faces = mtcnn_dir(test_im)
    img_probs = resnet( detected_faces )
    np_testsignatures = img_probs.detach().numpy()
    #print("np_testsignatures", np_testsignatures)
    xback.append( img_probs )
    #print("asiye",xback)
    for itera in range(detected_faces.size(0)):
        label_images.append(i)
      
    similarity_rate = np.matmul( np_testsignatures, np_indexsignatures.T )
    if np.all(similarity_rate >= score):
        print("BENZERLİK BULUNDU - TEKLİ")
        if not os.path.exists(hedef_klasor_tekli):
            os.makedirs(hedef_klasor_tekli)
            print("Tekli klasör oluşturuldu")
        kopya_dosya_adi = os.path.basename(filename)
        hedef_dosya_yolu = os.path.join(hedef_klasor_tekli, kopya_dosya_adi)
        shutil.copy2(filename, hedef_dosya_yolu)
        add_metadata_to_image(hedef_dosya_yolu, aranan_isim)
    elif np.any(similarity_rate >= score) and not np.all(similarity_rate >= score):
        print("BENZERLİK BULUNDU - ÇOKLU")
        if not os.path.exists(hedef_klasor_coklu):
            os.makedirs(hedef_klasor_coklu)
            print("Çoklu klasör oluşturuldu")
        kopya_dosya_adi = os.path.basename(filename)
        hedef_dosya_yolu = os.path.join(hedef_klasor_coklu, kopya_dosya_adi)
        shutil.copy2(filename, hedef_dosya_yolu)
        add_metadata_to_image(hedef_dosya_yolu,  aranan_isim)
    else:
        print("BENZERLİK YOK")

    print(similarity_rate)


    
xback2 = torch.vstack( xback ).detach().numpy()
#print("x2back", xback2.shape[1])
label_images = np.array( label_images )


