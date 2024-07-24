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
