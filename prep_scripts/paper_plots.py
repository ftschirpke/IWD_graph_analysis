import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import sys
from pathlib import Path
from osgeo import gdal
from osgeo import gdal_array
import glob
import pandas as pd
from affine import Affine
import pylustrator
import seaborn as sns

# activate pylustrator
pylustrator.start()

np.set_printoptions(threshold=sys.maxsize)

def plot_skel_on_det(detr_path, skel_path, id, filename):
    # detr_fname = (Path(detr_path).stem)
    # skel_fname = (Path(skel_path).stem)
    detr = gdal_array.LoadFile(detr_path)
    skel = gdal_array.LoadFile(skel_path)
    # detr = gdal.Open(detr_path)
    fname = Path(filename).stem[19:-5]
    # skel = np.ma.masked_where(skel == 0, skel)
    # plt.Figure()
    ax[int(id / 7), id % 7].imshow(detr, cmap=cm.gray)
    im = ax[int(id / 7), id % 7].imshow(skel, cmap=my_cmap,
                   interpolation='none',
                   clim=[0.9, 1])
    ax[int(id / 7), id % 7].axis('off')
    ax[int(id / 7), id % 7].set_title(fname)


def plot_skel_on_orig(orig_path, skel_path, id, filename):
    # detr_fname = (Path(detr_path).stem)
    # skel_fname = (Path(skel_path).stem)
    orig_t = gdal_array.LoadFile(orig_path)
    orig = orig_t[1:-1, 1:-1]
    skel = gdal_array.LoadFile(skel_path)
    # detr = gdal.Open(detr_path)
    fname = Path(filename).stem[19:-5]
    # skel = np.ma.masked_where(skel == 0, skel)
    # plt.Figure()
    ax[int(id / 7), id % 7].imshow(orig, cmap=cm.gray)
    im = ax[int(id / 7), id % 7].imshow(skel, cmap=my_cmap,
                   interpolation='none',
                   clim=[0.9, 1])
    ax[int(id / 7), id % 7].axis('off')
    ax[int(id / 7), id % 7].set_title(fname)


def plot_graph_by_weight(graph, col_parameter, coord_dict, bg):
    micr = bg

    G_no_borders = graph.copy()
    for (s, e) in graph.edges():
        # print(graph[s][e])
        if col_parameter in graph[s][e]:
            # print(G_no_borders[s][e]['mean_depth'])
            continue
        else:
            G_no_borders.remove_edge(s, e)

    f = plt.figure(1, figsize=(3.75, 2.45), dpi=300)  # 900
    ax = f.add_subplot(1, 1, 1)

    colors = [G_no_borders[s][e][col_parameter] for s, e in G_no_borders.edges()]

    colors_nonnan = []
    for i in colors:
        if i > 0:
            colors_nonnan.append(i)

    colors = np.nan_to_num(colors, nan=np.mean(colors_nonnan), copy=True)

    if col_parameter == 'mean_width':
        tmp_coord_dict = {}
        tmp_keys = []
        tmp_vals = []
        for key, val in coord_dict.items():
            tmp_keys.append(key)
            tmp_vals.append(val)
        for i in range(len(tmp_keys)):
            tmp_coord_dict[tmp_keys[i]] = [tmp_vals[i][1], tmp_vals[i][0]]
        ax.imshow(micr, cmap='gray', alpha=0)
        # draw edge by weight
        edges = nx.draw_networkx_edges(G_no_borders, pos=tmp_coord_dict, arrows=False, edge_color=colors, edge_cmap=plt.cm.viridis,
                                       width=2, ax=ax, edge_vmin=0, edge_vmax=10)
                                       # , edge_vmin=np.min(colors), edge_vmax=np.max(colors)
        # # edges = nx.draw_networkx_edges(G_no_borders, pos=coord_dict, arrows=False, edge_color='blue', width=0.75, ax=ax)
        # nodes = nx.draw_networkx_nodes(G_no_borders, pos=tmp_coord_dict, node_size=0.5, node_color='black')
        cmap = plt.cm.viridis
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=10))
                                              # norm=plt.Normalize(vmin=np.min(colors), vmax=np.max(colors))
        sm.set_array([])
        cbar = plt.colorbar(sm)
        cbar.set_label('width [m]')
        # plt.gca().invert_xaxis()
        plt.axis('off')
        plt.margins(0.0)
        plt.tight_layout()
        # plt.title(col_parameter)
        # plt.savefig(r'D:\01_anaktuvuk_river_fire\00_working\01_processed-data\12_all_steps_with_manual_delin\images'
        #             r'graph_9m_2009_no-bg' + col_parameter + '.png', dpi=300)  # , bbox_inches='tight'
        # plt.show()
    elif col_parameter == 'mean_depth':
        tmp_coord_dict = {}
        tmp_keys = []
        tmp_vals = []
        for key, val in coord_dict.items():
            tmp_keys.append(key)
            tmp_vals.append(val)
        for i in range(len(tmp_keys)):
            tmp_coord_dict[tmp_keys[i]] = [tmp_vals[i][1], tmp_vals[i][0]]
        ax.imshow(micr, cmap='gray', alpha=0)
        edges = nx.draw_networkx_edges(G_no_borders, pos=tmp_coord_dict, arrows=False, edge_color=colors, edge_cmap=plt.cm.viridis,
                                       width=2, ax=ax, edge_vmin=0, edge_vmax=0.5)
                                       # , edge_vmin=np.min(colors), edge_vmax=np.max(colors)
        # # edges = nx.draw_networkx_edges(G_no_borders, pos=coord_dict, arrows=False, edge_color='blue', width=0.75, ax=ax)
        nodes = nx.draw_networkx_nodes(G_no_borders, pos=tmp_coord_dict, node_size=0.5, node_color='black')
        # plt.clim(np.min(colors), np.max(colors))
        # plt.colorbar(edges)
        cmap = plt.cm.viridis
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=0.5))
                                              # norm=plt.Normalize(vmin=np.min(colors), vmax=np.max(colors))
        sm.set_array([])
        cbar = plt.colorbar(sm)
        cbar.set_label('depth [m]')
        # plt.gca().invert_xaxis()
        plt.axis('off')
        plt.margins(0.0)
        plt.tight_layout()
        # plt.title(col_parameter)
        # plt.savefig(r'D:\01_anaktuvuk_river_fire\00_working\01_processed-data\12_all_steps_with_manual_delin\images'
        #             r'graph_9m_2009_no-bg' + col_parameter + '.png', dpi=300)  # , bbox_inches='tight'
        # plt.show()
    elif col_parameter == 'mean_r2':
        ax.imshow(micr, cmap='gray', alpha=0)
        tmp_coord_dict = {}
        tmp_keys = []
        tmp_vals = []
        for key, val in coord_dict.items():
            tmp_keys.append(key)
            tmp_vals.append(val)
        for i in range(len(tmp_keys)):
            tmp_coord_dict[tmp_keys[i]] = [tmp_vals[i][1], tmp_vals[i][0]]
        edges = nx.draw_networkx_edges(G_no_borders, pos=tmp_coord_dict, arrows=False, edge_color=colors,
                                       edge_cmap=plt.cm.viridis,
                                       width=2, ax=ax, edge_vmin=0.8, edge_vmax=1)
        # , edge_vmin=np.min(colors), edge_vmax=np.max(colors)
        # # edges = nx.draw_networkx_edges(G_no_borders, pos=coord_dict, arrows=False, edge_color='blue', width=0.75, ax=ax)
        nodes = nx.draw_networkx_nodes(G_no_borders, pos=tmp_coord_dict, node_size=0.5, node_color='black')
        # plt.clim(np.min(colors), np.max(colors))
        # plt.colorbar(edges)
        cmap = plt.cm.viridis
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0.8, vmax=1))
        # norm=plt.Normalize(vmin=np.min(colors), vmax=np.max(colors))
        sm.set_array([])
        cbar = plt.colorbar(sm)
        cbar.set_ticks([0.80, 0.85, 0.90, 0.95, 1.00])
        cbar.set_ticklabels(['0.80', '0.85', '0.90', '0.95', '1.00'])
        cbar.set_label('r2')
        # plt.gca().invert_xaxis()
        plt.axis('off')
        plt.margins(0.0)
        plt.tight_layout()
        # plt.title(col_parameter)
        # plt.savefig(r'D:\01_anaktuvuk_river_fire\00_working\01_processed-data\12_all_steps_with_manual_delin\images'
        #             r'graph_9m_2009_no-bg' + col_parameter + '.png', dpi=300)  # , bbox_inches='tight'
        # plt.show()
    elif col_parameter == "centrality":
        # micr = np.fliplr(micr)
        ax.imshow(micr, cmap='gray', alpha=0)
        tmp_coord_dict = {}
        tmp_keys = []
        tmp_vals = []
        for key, val in coord_dict.items():
            tmp_keys.append(key)
            tmp_vals.append(val)
        for i in range(len(tmp_keys)):
            tmp_coord_dict[tmp_keys[i]] = [tmp_vals[i][1], tmp_vals[i][0]]
        # draw directionality
        # (and plot betweenness centrality of edges via color)
        cmap = plt.cm.viridis
        sm = plt.cm.ScalarMappable(cmap=cmap,
                                   norm=matplotlib.colors.LogNorm(
                                       vmin=3.285928340474751e-07,
                                       vmax=0.0025840540469493443))  # this one's static
                                   # norm=matplotlib.colors.LogNorm(vmin=np.min(list(nx.edge_betweenness_centrality(graph).values())),
                                   #                    vmax=np.max(list(nx.edge_betweenness_centrality(graph).values()))))  # this one's dynamic
        nx.draw(graph, pos=tmp_coord_dict, arrowstyle='->', arrowsize=3.5, width=1, with_labels=False, node_size=0.005,
                edge_color=np.log(np.array(list(nx.edge_betweenness_centrality(graph).values()))), node_color='black',
                edge_cmap=cmap)
        print(np.min(np.array(list(nx.edge_betweenness_centrality(graph).values()))))
        print(np.max(np.array(list(nx.edge_betweenness_centrality(graph).values()))))
        sm.set_array([])
        cbar = plt.colorbar(sm)
        cbar.set_label('betweenness centrality')
        plt.margins(0.0)
        plt.axis('off')
        plt.tight_layout()
    elif col_parameter == 'directionality':
        # draw directionality
        tmp_coord_dict = {}
        tmp_keys = []
        tmp_vals = []
        for key, val in coord_dict.items():
            tmp_keys.append(key)
            tmp_vals.append(val)
        for i in range(len(tmp_keys)):
            tmp_coord_dict[tmp_keys[i]] = [tmp_vals[i][1], tmp_vals[i][0]]

        # without bg
        ax.imshow(micr, cmap='Greys_r', alpha=1)
        nx.draw(graph, pos=tmp_coord_dict, arrowstyle='-', arrowsize=3.5, width=0.8, with_labels=False, node_size=0,
                node_color='seagreen', edge_color='black')
        # with bg
        # ax.imshow(micr, cmap='Greens', alpha=0)
        # nx.draw(graph, pos=tmp_coord_dict, arrowstyle='->', arrowsize=3.5, width=0.8, with_labels=False, node_size=0.65,
        #         node_color='white', edge_color='black')
        # plt.title("directionality")
        plt.margins(0.0)
        plt.axis('off')
        plt.tight_layout()
    elif col_parameter == 'water_filled':
        tmp_coord_dict = {}
        tmp_keys = []
        tmp_vals = []
        for key, val in coord_dict.items():
            tmp_keys.append(key)
            tmp_vals.append(val)
        for i in range(len(tmp_keys)):
            tmp_coord_dict[tmp_keys[i]] = [tmp_vals[i][1], tmp_vals[i][0]]
        ax.imshow(micr, cmap='gray', alpha=0)
        # draw edge by weight
        edges = nx.draw_networkx_edges(G_no_borders, pos=tmp_coord_dict, arrows=False, edge_color="blue", edge_cmap=plt.cm.viridis,
                                       width=colors*2, ax=ax, edge_vmin=0, edge_vmax=1)
                                       # , edge_vmin=np.min(colors), edge_vmax=np.max(colors)
        # # edges = nx.draw_networkx_edges(G_no_borders, pos=coord_dict, arrows=False, edge_color='blue', width=0.75, ax=ax)
        # nodes = nx.draw_networkx_nodes(G_no_borders, pos=tmp_coord_dict, node_size=0.05, node_color='blue')
        cmap = plt.cm.viridis
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=1))
                                              # norm=plt.Normalize(vmin=np.min(colors), vmax=np.max(colors))
        sm.set_array([])
        cbar = plt.colorbar(sm)
        cbar.set_label('fraction')
        # plt.gca().invert_xaxis()
        plt.axis('off')
        plt.margins(0.0)
        plt.tight_layout()
    else:
        print("please choose one of the following col_parameters: 'mean_width', 'mean_depth', 'mean_r2', 'centrality', 'directionality'")


def plot_all_subfigures():
    path = r'E:\02_macs_fire_sites\00_working\01_processed-data\06_workflow_outputs'

    my_cmap = cm.autumn
    my_cmap.set_under('k', alpha=0)
    fig, ax = plt.subplots(7, 7, figsize=(20, 20))
    id = 0

    for filename in glob.iglob(f'{path}/02_skeletons/*'):
        # print(Path(filename).stem)
        fname = Path(filename).stem[7:-5]
        print(fname)
        plot_skel_on_orig(f'E:/02_macs_fire_sites/00_working/00_orig-data/03_lidar/product-dem/dtm_1m/proj/cut_to_aoi/PERMAX{fname}.tif', f'{path}/02_skeletons/PERMAX_{fname}_skel.tif', id, filename)
        # plot_skel_on_det(f'{path}/01_detrended/arf_microtopo_{fname}.tif', f'{path}/02_skeletons/PERMAX_{fname}_skel.tif', id, filename)

        id += 1

    ax[6, 5].axis('off')
    ax[6, 6].axis('off')

    # plt.savefig(r'E:\02_macs_fire_sites\00_working\03_code_scripts\IWD_graph_analysis\figures\outputs\skeletons_on_original.pdf', bbox_inches='tight')
    plt.show()


def plot_graph_results(df, x, y, col, siz, mar, lab):
    # coef = np.polyfit(df[x], df[y], 3)
    # poly1d_fn = np.poly1d(coef)
    colors = {'n': 'red', 'y': 'green'}
    colors = {0: '#2a4858', 1: '#00898a', 2: '#64c987', 3: '#fafa6e'}
    plt.scatter(df[x], df[y], c=df['num_fires'].map(colors), s=siz, marker=mar, label=lab)  # , c=df['cc_count'], s=df['cc_count']
    # df.boxplot(column=[x, y])  # , c=df['cc_count'], s=df['cc_count']
    # plt.plot(df[x], poly1d_fn(df[x]), color=col, alpha=0.5)
    # plt.errorbar(df[x], poly1d_fn(df[x]), yerr=poly1d_fn(df[x]) - df[y], color=col, alpha=0.5)

    plt.xlabel('Years passed since first fire')
    plt.ylabel(str(y))
    plt.ylabel("Graph density")
    # sns.regplot(data=df, x=x, y=y, x_ci='sd', scatter=True, color=col, marker=mar, label=lab)
    # plt.legend()

def count_cc(df):
    cc_list = []
    for i in df['connected_comp']:
        # print(i)
        obj = i[8:-1]
        # print(obj)
        Dict = eval(obj)
        cc = 0
        for v in Dict.values():
            # print(v)
            cc += v
        # print(cc)
        cc_list.append(cc)
    # print(cc_list)
    df['cc_count'] = cc_list
    return df


if __name__ == '__main__':
    # plot_all_subfigures()
    df = pd.read_csv('E:/02_macs_fire_sites/00_working/01_processed-data/06_workflow_outputs/merged_csv.csv', sep='\t')
    df = count_cc(df)
    df = df.loc[df['good_seg'] == 'y']
    plt.Figure()
    plot_graph_results(df, 'fire_age_1', 'graph_density', col='#931C47', siz=df['graph_density']*200, mar='.', lab='First recorded fire')
    # plot_graph_results(df, 'fire_age_3', 'total_channel_length_m', col='#d62728', siz=df['graph_density']*200-0, mar='+', lab='Last recorded fire')

    plt.show()