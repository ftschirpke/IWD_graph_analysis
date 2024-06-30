nextflow.enable.dsl=2

process networkAnalysis {
    publishDir 'output/csv', mode: 'copy', pattern: '**.csv'
    container 'fondahub/iwd:latest'
    memory '300 MB'
    cpus 2

    input:
        tuple val(key), path(tif), val(year), path(npy), path(edgelist), path(transect_dict_avg), path(transect_dict_fitted)

    output:
        tuple val(key), path("graph_*.csv"), emit: csvs
        tuple val(key), path("*weights.edgelist"), emit: weightedEdgelist

    script:
    """
    echo "========================================================================"
    ls
    echo "========================================================================"
    echo ${tif}
    echo ${edgelist}
    echo ${npy}
    echo ${transect_dict_avg}
    echo ${year}
    echo "========================================================================"
    d_network_analysis.py ${tif} ${edgelist} ${npy} ${transect_dict_avg} ${year}
    """

}
