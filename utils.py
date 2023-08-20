# Import necessary libraries for image processing, data visualization, etc.
from fastai.vision.all import *
from nbdev.showdoc import *
from ipywidgets import widgets
from pandas.api.types import CategoricalDtype
import matplotlib as mpl
import json

# Commented out DPI setting for figures (can be enabled if needed)
# mpl.rcParams['figure.dpi']= 200

# Set DPI for saving figures and font size
mpl.rcParams['savefig.dpi'] = 200
mpl.rcParams['font.size'] = 12

# Set random seed for reproducibility and other backend settings
set_seed(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
pd.set_option('display.max_columns', 999)
np.set_printoptions(linewidth=200)
torch.set_printoptions(linewidth=200)

# Import Graphviz for graph visualization
import graphviz
def gv(s): return graphviz.Source('digraph G{ rankdir="LR"' + s + '; }')

# Get sorted image files from the specified path
def get_image_files_sorted(path, recurse=True, folders=None): return get_image_files(path, recurse, folders).sorted()

# Import Azure Image Search Client
from azure.cognitiveservices.search.imagesearch import ImageSearchClient as api
from msrest.authentication import CognitiveServicesCredentials as auth

# Search for images using Bing's API
def search_images_bing(key, term, min_sz=128, max_images=150):    
     params = {'q':term, 'count':max_images, 'min_height':min_sz, 'min_width':min_sz}
     headers = {"Ocp-Apim-Subscription-Key":key}
     search_url = "https://api.bing.microsoft.com/v7.0/images/search"
     response = requests.get(search_url, headers=headers, params=params)
     response.raise_for_status()
     search_results = response.json()    
     return L(search_results['value'])

# Search for images using DuckDuckGo
def search_images_ddg(key, max_n=200):
     # ... (see original code for details) ...

# Function to plot a given function f
def plot_function(f, tx=None, ty=None, title=None, min=-2, max=2, figsize=(6,4)):
    x = torch.linspace(min, max)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x, f(x))
    if tx is not None: ax.set_xlabel(tx)
    if ty is not None: ax.set_ylabel(ty)
    if title is not None: ax.set_title(title)

# Function to draw a decision tree using sklearn's export_graphviz
from sklearn.tree import export_graphviz
def draw_tree(t, df, size=10, ratio=0.6, precision=0, **kwargs):
    s = export_graphviz(t, out_file=None, feature_names=df.columns, filled=True, rounded=True,
                        special_characters=True, rotate=False, precision=precision, **kwargs)
    return graphviz.Source(re.sub('Tree {', f'Tree {{ size={size}; ratio={ratio}', s))

# Function to cluster DataFrame columns based on Spearman correlation
from scipy.cluster import hierarchy as hc
def cluster_columns(df, figsize=(10,6), font_size=12):
    corr = np.round(scipy.stats.spearmanr(df).correlation, 4)
    corr_condensed = hc.distance.squareform(1-corr)
    z = hc.linkage(corr_condensed, method='average')
    fig = plt.figure(figsize=figsize)
    hc.dendrogram(z, labels=df.columns, orientation='left', leaf_font_size=font_size)
    plt.show()
