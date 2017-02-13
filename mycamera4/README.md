
MyCamera
========

Kamera resimleri, yön algılayıcısı (orientatıon sensor), GPS
değerleri, ivme algılayıcı (accelerometer) belli aralıklarla
biriktirir, ve istendiği anda (Rec düğmesine basarak) sonuçları
telefon dizinine kaydeder. Dosya SDCARD/Bass altında bir numaralı
dizindir, her Rec sonrası yeni bir dizin yaratılır. Böylece birkaç
ölçümü arka arkaya kaydetmek mümkün olur.

![](bass2.png)

Her olcum icin ayri bir txt dosyasi var, analiz amaciyla bu dosyalari USB ile
dizustune aktarmak yeterli.

# Haritada Yer Gostermek

Uygulama icinde ve eğer GPS baglantisi kurulduysa Map düğmesina
basılarak o anda olunan yerin haritası alınabilir. Haritalar bir zıp
dosyası içinde, örnek haritalar

https://dl.dropboxusercontent.com/u/1570604/data/istanbul.zip

https://dl.dropboxusercontent.com/u/1570604/data/berlin.zip

https://dl.dropboxusercontent.com/u/1570604/data/world1.zip

https://dl.dropboxusercontent.com/u/1570604/data/world2.zip

Bu dosyayı SDCARD/Başs/ dizini altına kopyalamak yeterli, bu dosyalara
işaret eden menü seçenekleri kodun içinde. Daha fazla harita eklemek
isteyenler kodda değişim yapmalı.

Dosya içindeki harita parçaları png dosyaları olarak kayıtlı, hangi
GPS kordinatının haritası oldukları dosya isminde kodlanmış halde,
kordinat haritanın orta noktasıdır.

Android / Java tekniği olarak faydalı olabilecek bazı kod bölümleri:

- ZIP içinden dosya okumak: Tüm haritalar zıp içinde, zıp içine bakıp
  oradaki dosya isimlerini almak, sonra istenilen tek dosyayı okuma
  tekniği var.

- Düzenli İfadeler (Regex): Harita orta noktası kordinatı harita dosya
  isminde kodlu olduğu için kordinatın geri alınması dosya ismini
  regex ile tarayıp içinden GPS enlem, boylam verisini almakla
  oluyor. Dosya isminde kordinat kodlama basitlik amaçlı yapıldı, eğer
  ayrı bir metin dosyasında kayıt olsaydı idare etmek zorlaşırdı. Ana
  amaç her zaman kod (veri) idaresinde kolaylık.

## Grafikleme

Geliştirme ortamında üstteki uygulamanın kullandığı aynı harita zıp
dosyalarını kullanrak herhangi bir enlem / boylamı harita üzerinde
grafiklemek mümkün, alttaki kod kullanılabilir. Mesela ilk nokta için
kutsal bir yeri seçelim, mesela Kabe - 40.987659,29.036428. Diğeri
künefe yenebilecek güzel bir yer, 40.992186,29.039228. Grafik altta,

```python
import pandas as pd, io
from PIL import Image
import os, glob, re, zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# enlem/boylam ve pikseller arasinda gecis icin
SCALEX = 23000. 
SCALEY = -35000.

def plot(res4,outfile):
    """
    Birinci noktayi baz alarak gerekli harita inajini bul, ve diger
    tum noktalari bu harita uzerinde grafikle
    """
    zfile = 'istanbul.zip'
    imgcoord = []
    with zipfile.ZipFile(zfile, 'r') as z:
        for f in z.namelist():
            # the lat/lon middle of the map is encoded in the map's
            # filename 
            tmp = re.findall("map_(-*\d+)_(\d+)_(-*\d+)_(\d+)",f,re.DOTALL)[0]
            imgcoord.append([float(tmp[0] + "." + tmp[1]), float(tmp[2] + "." + tmp[3]), f])
    imgcoord2 = pd.DataFrame(imgcoord,columns=['lat','lon','file'])
    
    dists = imgcoord2.apply(lambda x: np.sqrt((x['lat']-res4[0][0])**2 + (x['lon']-res4[0][1])**2), axis=1)
    print dists.argmin()
    # the closest map is picked
    found = imgcoord2.ix[dists.argmin()]
    print found.file
    mapcenter = np.array(found[['lat','lon']])
    print mapcenter
    
    with zipfile.ZipFile(zfile, 'r') as z:
         im = Image.open(z.open(found.file))
         nim = np.array(im)
         c = nim.shape[0] / 2, nim.shape[0] / 2
         plt.axis('off')
         fig=plt.imshow(im)
         fig.axes.get_xaxis().set_visible(False)
         fig.axes.get_yaxis().set_visible(False)
         plt.imshow(im)
         for [lat,lon] in res4:
             dx,dy=((lon-mapcenter[1])*SCALEX,(lat-mapcenter[0])*SCALEY)
             xx = c[0]+dx
             yy = c[1]+dy
             if xx > nim.shape[0] or yy > nim.shape[1] or xx<0 or yy<0: continue
             plt.plot(xx,yy,'r.')
             plt.hold(True)                          
         plt.savefig(outfile, bbox_inches='tight', pad_inches = 0)


pts = np.array([[40.987659,29.036428],[40.992186,29.039228]])
plot(pts,'istanbul.png')
```

```text
151
istanbul_map_40_9890312632_29_0305433684.png
[40.989031263199998 29.0305433684]
```

![](istanbul.png)

Kameranın kaydettiği video'nun herhangi bir zaman dilimindeki tek resmini elde
etmek için alttaki kod kullanılabilir. 


English
========

Example of how to use Android camera, recording of orientation sensor,
GPS, and camera frames. We skip some frames for performance / storage
reasons, and the unit of storage for all recording is the
frame. Whenever a frame is recorded, orientation, GPS will be recorded
along with it.

The data files are dumped under SDCARD/Bass folder, which can be taken
transferred to notebook for analysis, etc. Data can be analyzed with,

```
import pandas as pd

data = np.fromfile("cam.txt", dtype=np.uint8)
df = pd.read_csv("sizes.txt",header=None)
df['cum'] = df.cumsum()
df['cum2'] = df.cum.shift(-1)
df.columns = ['x','fr','to']
```

for textual data, and for cam images

```
import io
from PIL import Image
frame = 8
arr = data[int(df.ix[frame]['fr']) : int(df.ix[frame]['to'])]
im = Image.open(io.BytesIO(arr))
im.save('out.png')
```

There is also offline mapping support, see the sample zip data file
above. Simply drop this file under SDCARD/Bass.

The camera, preview code is based on

http://ibuzzlog.blogspot.tw/2012/08/how-to-use-camera-in-android.html

Zoomable map viewer is based on

https://github.com/MikeOrtiz/TouchImageView/blob/master/src/com/ortiz/touch/TouchImageView.java
