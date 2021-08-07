import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from yaocetool import read_data, sparse, myplot

df = read_data('D:\\ShareCache\\马友\\1111.dat', indexname='时间')
df2 = sparse(df, '20210803', '20210809', 1)
print(df2)
myplot(df2, range(0,len(df.columns)))
ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(0.5))

