---
title: Python 視覺化(3) matplotlib 進階繪圖
date: 2024-07-15 16:53:36
categories: Python
description: 紀錄一些資源，為視覺化提供一點參考的靈感。並記錄如何用 matplotlib 繪製 Waffle Chart 。
---
數據視覺化在資料分析中是重要的環節，研究型分析跟發表型分析更有不同的表達方式。當拿到一筆資料，最頭痛的就是不知道該用何種圖來「觀察」它。

## 沒有繪圖靈感時的資源

以下幾個網站可以提供一點靈感: 

- [The Python Graph Gallery](https://python-graph-gallery.com/): 列出多種圖，和實際在海報上會看到的，很 fancy 的圖。透過現成的圖像得到靈感! 
- [from Data to Viz](https://www.data-to-viz.com/#explore): 
    - 提供一個決策樹，使用者可以根據手上的資料分析，例如: 一維/二維/多維數據? 是否需要排序?
    - 提供 Case Study，例如: [公寓價格與地面居住面積](https://www.data-to-viz.com/story/TwoNum.html) 就是來自 Kaggle 的 dataset. 

前面兩者都還偏向圖庫加上快速分析，下面兩篇則針對商業上「說故事」與「畫哪種圖」一些簡單的引導。

- [7 Data Storytelling Techniques to Build Dashboards That Engage your Customers](https://www.toucantoco.com/en/blog/7-data-storytelling-techniques-to-engage-your-customers)
- [8 Data Storytelling Concepts](https://twooctobers.com/blog/8-data-storytelling-concepts-with-examples/)


## Waffle Chart 

`matplotlib` 畫一些基本的圖很方便，複雜的圖則依賴 `seaborn` 。但如果只有一兩種特別的圖，不想特別載新的模組，還是可以透過 `matplotlib` 達成。以 Waffle Chart 來說，可以用 `plt.matshow` 達成。在[這篇 stackoverflow](https://stackoverflow.com/a/41440802) 有個範例，流程大致是

1. 製作一個 np.array，每一格填入數字代表它的 class 
2. `plt.matshow` 繪製
3. 手動加 `legend` 說明每種 color 代表什麼類別。

我根據那篇留言的案例，再做了點變化而成下面的範例

1. 改用 Numpy reshape 的方式得到 array 

2. 使用 `ListedColormap` 自訂 color map。

    如果不想用既有的色盤，想針對每個類別給指定的顏色可以用 `ListedColormap`，但建議在 `matshow` 的時候要指定 `vmin` 與 `vmax`。`vmin` 應為資料中可能的的最小值，而 `vmax` 為可能的最大值。否則 `matshow` 在取色的時候，會以「當前資料的最小與最大值」作為上下界取色，如果每筆資料的最大最小值都不同，則相同數值取到的顏色會不一樣。

    在這個例子中，我讓 `0` 為補空格 (如果資料不能被 10 整除，則需要補齊 array )，1~3 才是真正的類別，因此應該這樣給: 
    
    ```python
    ax.matshow(arr2d, cmap=colormap, vmin=0, vmax=3)
    ```
    

### 完整範例

![waffle_chart_example](../img/python-visualize-advance-2/waffle_chart_example.png)

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as color 
import numpy as np 
from sklearn import datasets

wine = datasets.load_wine()
target = wine.target
names = wine.target_names
cls_data = {
    names[0] : (target==0).sum(),
    names[1] : (target==1).sum(),
    names[2] : (target==2).sum(),
}

def waffle_plot(cls_data, ax, colormap=plt.cm.coolwarm, base_hight=10 ):
    base_hight = 10
    legends = []
    i = 0 # None 
    targets = []
    for i, (k, v) in enumerate(cls_data.items()):
        targets.append(np.ones(v)*(i+1))
        color_val = colormap(float(i+1)/len(cls_data))
        legends.append(mpatches.Patch(color=color_val, label=k))
    arr = np.concatenate(targets)

    if len(arr) % base_hight != 0:
        width = len(arr) // base_hight + 1 
    total = base_hight * width 
    arr2d = np.concatenate([arr, np.zeros(total - len(arr))]).reshape(base_hight, -1)

    ax.matshow(arr2d, cmap=colormap, vmin=0, vmax=3)
    height, width = arr2d.shape

    # Minor ticks
    ax.set_xticks(np.arange(-.5, (width), 1), minor=True)
    ax.set_yticks(np.arange(-.5, (height), 1), minor=True)

    # Gridlines based on minor ticks
    ax.grid(which='minor', color='white', linestyle='-', linewidth=2)
    
    
    # Add the legend. Still a bit of work to do here, to perfect centering.
    ax.legend(handles=legends, loc=1, ncol=len(legends),
               bbox_to_anchor=(0., -0.1, 0.95, .10))

    ax.set_frame_on(False)
    ax.set_xticks([])
    ax.set_yticks([])
    return 

fig = plt.figure(figsize=(12, 6), dpi=80, layout="constrained")
axes = fig.subplots(1, 2).reshape(-1)

waffle_plot(cls_data, axes[0])
axes[0].set_title("coolwarm")

cmap = color.ListedColormap(colors=["white", "lime", "pink", "cyan"])
waffle_plot(cls_data, axes[1], colormap=cmap)
axes[1].set_title("ListedColormap")

fig.savefig("test.png")
plt.show()

```

## 其他

還有 API 太難記了，這也有 `matplotlib` 的 [Cheat Sheets](https://python-graph-gallery.com/cheat-sheets/)

