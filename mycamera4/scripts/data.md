
## Veri Islemek

Telefon tarafindan toplanan verileri nasil kullaniriz? 

```python
import pandas as pd

dir = "./data/mitte4/"
data = np.fromfile(dir + "cam.bin", dtype=np.uint8)
df = pd.read_csv(dir + "sizes.txt",header=None)
df['cum'] = df.cumsum()
df['cum2'] = df.cum.shift(-1)
df.columns = ['x','fr','to']
```

Herhangi bir video karesini cekip cikarmak


```python
import io
from PIL import Image
frame = 30
arr = data[int(df.ix[frame]['fr']) : int(df.ix[frame]['to'])]
im = Image.open(io.BytesIO(arr))
im.save('out1.png')
```

![](out1.png)


```python
import util
im = util.get_frame(dir, 105)
np.random.seed(1)
random_points = np.random.uniform(0, 320, (10000, 2)).astype(np.int)
random_points = random_points[random_points[:,1] < 240]
quad = [[100,0],[143,100.],[202,100],[224,0]]
h = np.array(im).shape[0]
util.plot_quad(quad, h, 'y')
plt.imshow(im)
plt.savefig('out2.png')
```

![](out2.png)














