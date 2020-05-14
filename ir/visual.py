import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from sklearn.decomposition import IncrementalPCA
from sklearn.metrics.pairwise import cosine_similarity
import random

def ipca2d(tfidf_matrix, cluster_labels, titles, name = 'Кластеризация'):
    dist = 1 - cosine_similarity(tfidf_matrix)

    icpa = IncrementalPCA(n_components=2, batch_size=16)
    icpa.fit(dist)
    points = icpa.transform(dist)
    xs, ys = points[:, 0], points[:, 1]

    #создаем data frame, который содержит координаты (из PCA) + номера кластеров и сами запросы
    df = pd.DataFrame(dict(x=xs, y=ys, label=cluster_labels, title=titles)) 
    #группируем по кластерам
    groups = df.groupby('label')

    #устанавливаем цвета
    cluster_colors = generate_colors(groups.ngroups)
    #даем имена кластерам
    cluster_names = generate_names(groups.ngroups)    

    fig, ax = plt.subplots(figsize=(24, 12)) #figsize подбирается под ваш вкус

    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=5, label=cluster_names[name], color=cluster_colors[name], mec='none')
        ax.set_aspect('auto')
        ax.tick_params(
            axis= 'x',          
            which='both',      
            bottom='off',      
            top='off',         
            labelbottom='off'
        )
        ax.tick_params(
            axis= 'y',         
            which='both',     
            left='off',      
            top='off',       
            labelleft='off'
        )
    
    ax.legend(numpoints=1)  #показать легенду только 1 точки
    ax.set_title(name)

    #добавляем метки/названия в х,у позиции с поисковым запросом
    # for i in range(len(df)):
    #     ax.text(df['x'][i], df['y'][i], df['title'][i], size=6)  
    
    #показать график
    plt.show() 
    plt.close()

#def ipca3d(tfidf_matrix):
    #nothing here right now
    
def generate_colors(n):
    color_list = []
    for c in range(0,n):
        r = lambda: random.randint(0,255)
        color_list.append( '#%02X%02X%02X' % (r(),r(),r()) )
    return color_list
    
def generate_names(n):
    name_list = []
    for c in range(0, n):        
        name_list.append(str(c + 1))
    return name_list
