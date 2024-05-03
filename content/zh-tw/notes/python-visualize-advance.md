---
title: Python 視覺化(2) matplotlib 進階繪圖
date: 2022-01-27 14:56:12
categories: Python
description: 紀錄做數據研究時，使用 matplotlib 繪圖的進階操作。直方圖疊加、如何合併 twinx 下不同的圖例(legend)、將圖例移出繪圖區、在軸上使用省略符號..。
aliases: 
- /posts/2022-01-27-python-visualize-advance
---

## 多個直方圖疊加

- `histtype`
  - `bar`：傳統的 `bar` 形式圖，屬於同個 bin 不同的資料會肩並肩的橫向排列。
  - `barstacked`：`bar` 形式的，但是屬於同一個 bin 的不同資料會直接往上疊加。
  - `step`：只有階梯的框架線，沒有填滿顏色。
  - `stepfilled`：這是預設方法，除了階梯式之外在加上填滿色彩。

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
n_bins = 10
x = np.random.randn(1000, 3)

fig = plt.figure()
axes = fig.subplots(2, 3).reshape(-1)
colors = ['pink', 'blue', 'lime']

ax = axes[0]
ax.hist(x, n_bins, histtype='bar', color=colors, label=colors, alpha=0.5)
ax.set_title('histtype bar')

ax = axes[1]
ax.hist(x, n_bins, histtype='barstacked', color=colors, label=colors, alpha=0.5)
ax.set_title('histtype barstacked')

ax = axes[2]
ax.hist(x, n_bins, histtype='step', stacked=True, color=colors, label=colors, alpha=0.5)
ax.set_title('histtype step, stack steps')

ax = axes[3]
ax.hist(x, n_bins, histtype='step', color=colors, label=colors, alpha=0.5)
ax.set_title('histtype step')

ax = axes[4]
ax.hist(x, n_bins, histtype='stepfilled', color=colors, label=colors, alpha=0.5)
ax.set_title('histtype stepfilled')
plt.show()
```

![matplotlib histtype](https://i.imgur.com/tB4vKCK.jpeg)

## 圖例集合

當兩分資料想要放在一起比較，尺度卻又相差過大時常常會使用副軸 `ax.twinx()`，但是副軸上的圖例會被分開。若想要合併圖例，需要手動指定 `legend` 函式內的內容。

```python
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 8), dpi=80)
axes = fig.subplots(1, 2)
colors = ['pink', 'skyblue', 'lime']
ax = axes[0]
ax.plot(np.arange(0, 10, 0.1)/10+np.random.rand(100), color=colors[0], label="data 1")
ax_sub = ax.twinx()
ax_sub.plot(np.arange(100, 90, -0.1)+np.random.rand(100), color=colors[1], label="data 2")
ax.legend()
ax_sub.legend()
ax.set_title("No secondary axis legend")

ax = axes[1]
ax_sub = ax.twinx()
plist = []
plist += ax.plot(np.arange(0, 10, 0.1)/10+np.random.rand(100), color=colors[0], label="data 1")
plist += ax_sub.plot(np.arange(100, 90, -0.1)+np.random.rand(100), color=colors[1], label="data 2")
ax.legend(plist, [p.get_label() for p in plist], loc="best")
ax.set_title("Both axis legends")
fig.savefig("AxisLegends.jpg")
```

![將圖例集合顯示](https://i.imgur.com/pSvuVHf.jpeg)

範例中使用 `plist` 匯集所有的繪圖物件，但需要注意繪圖物件回傳的形式為何。Scatter 回傳的是單純繪圖物件，plot 回傳的則是一個包含繪圖物件的 list ，要視情況將物件蒐集進 `plist`，選擇用 `plist.append(xxx)` 或是 `plist.extend(xxx)`

```
In [196]: ax.scatter(np.ones(10), np.random.rand(10))
Out[196]: <matplotlib.collections.PathCollection at 0x207bc23ad08>

In [197]: ax.plot(np.arange(0, 10, 0.1)/10+np.random.rand(100), color=colors[0], label="data 1")        
Out[197]: [<matplotlib.lines.Line2D at 0x207bca2c248>]
```



## [Break The axis][Break the axis]

這裡先根據 matplotlib 的教學繪製了這種可以跳躍部份數值的圖：

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(8, 8), dpi=80)
gs = gridspec.GridSpec(2, 2)

# 畫同一張
ax = plt.subplot(gs[:, 0]) 
data1 = np.random.rand(100, 2)*10+np.array([[0, 100]])
data2 = np.random.rand(25, 2)*5
ax.scatter(data1[:, 0], data1[:, 1], color="b")
ax.scatter(data2[:, 0], data2[:, 1], color="orange")
ax.set_title("Plot in 1 graph", fontsize="x-large")

# 切割不同張
ax_up = plt.subplot(gs[0, 1])
ax_bot = plt.subplot(gs[1, 1], sharex=ax_up)
ax_up.scatter(data1[:, 0], data1[:, 1], color="b")
ax_bot.scatter(data2[:, 0], data2[:, 1], color="orange")

ax_up.spines['bottom'].set_visible(False)
ax_bot.spines['top'].set_visible(False)
ax_up.xaxis.tick_top()
ax_up.tick_params(labeltop=False)  # don't put tick labels at the top
ax_bot.xaxis.tick_bottom()

d = .015  
kwargs = dict(transform=ax_up.transAxes, color='k', clip_on=False)
ax_up.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax_up.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax_bot.transAxes)  # switch to the bottom axes
ax_bot.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax_bot.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
ax_up.set_title("Plot in broken axis", fontsize="x-large")
plt.show()
```

![切割軸](https://i.imgur.com/1jZK1wb.jpeg)

其實原始的套件並不好用，網路上有一個 [brokenaxes](https://pypi.org/project/brokenaxes/) 的套件，能讓我們更輕鬆的達成這件事情。

```python
from brokenaxes import brokenaxes 
fig = plt.figure(figsize=(8,8), dpi=80) 
baxes = brokenaxes(xlims=((-0.001, 5.001), (99, 111)), ylims=((-0.001, 5.001), (99, 111)), hspace=.1) 

data1 = np.random.rand(100, 2)*10+np.array([[100, 100]])
data2 = np.random.rand(25, 2)*5
baxes.scatter(data1[:, 0], data1[:, 1], color="b")
baxes.scatter(data2[:, 0], data2[:, 1], color="orange")
fig.savefig("brokenaxes_pkg.jpg")
```

![切割軸在兩個維度上](https://i.imgur.com/F9siwYf.jpeg)


## [圖例移出繪圖][legend out of plot]

```python
ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
```

但需要注意，將圖例移出繪圖之後，圖例很容易被切掉。我自己是在環境有寫 matplotlibrc 檔案，裡面有設置自動調整版面 :

```
figure.autolayout: True
```

如果沒有寫 matplotlibrc ，要記得對繪圖做 `fig.tightlayout()`

[legend out of plot]:<https://www.delftstack.com/zh-tw/howto/matplotlib/how-to-place-legend-outside-of-the-plot-in-matplotlib/> "Matplotlib 中如何將圖例放置在繪圖之外"

## 假色圖

```python
data1 = np.repeat(np.sin(np.linspace(0, 1, 10)).reshape(1,-1), 10, axis=0)
pc = ax.pcolor(data1.T, cmap=plt.cm.Blues, vmin=0, vmax=1)
ax.set_title("Sin")
fig.colorbar(pc, ax=ax, orientation="horizontal")
```

在下圖一併展示

## 熱力圖

```python
x = np.random.randn(1000)
y = np.random.randn(1000)
heatmap, xedges, yedges = np.histogram2d(x, y, bins=1000)
heatmap = gaussian_filter(heatmap, sigma=16)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
img = heatmap.T
pc = ax.imshow(img, extent=extent, origin='lower', cmap=cm.jet,)
fig.colorbar(pc, ax=ax, orientation="horizontal", )
```

Heatmap 的程式碼參考: [Generate a heatmap in MatPlotLib using a scatter data set][heatmap]



![Heatmap 的展示與圖移出圖例](https://i.imgur.com/F1yQcLB.jpeg)

---



[Brokenaxes]:<https://github.com/bendichter/brokenaxes> "brokenaxes (github package)"
[Break the axis]: <https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/broken_axis.html> "Broken Axis (matplotlib)"
[heatmap]: <https://stackoverflow.com/questions/2369492/generate-a-heatmap-in-matplotlib-using-a-scatter-data-set> "熱力圖"

