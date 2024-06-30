nextflow.enable.dsl=2

process networkAnalysis {
    publishDir 'output/csv', mode: 'copy', pattern: '**.csv'
    container 'fondahub/iwd:latest'
    memory '300 MB'
    cpus 2

    input:
        tuple val(key), path(npy), path(edgelist), path(tif), val(year), path(transect_dict_avg), path(transect_dict_fitted)

    output:
        path("graph_*.csv"), emit: csvs
        tuple val(key), path("*weights.edgelist"), emit: weightedEdgelist

    script:
    """
    d_network_analysis.py ${tif} ${edgelist} ${npy} ${transect_dict_avg} ${year}
    """

}
