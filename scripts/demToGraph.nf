nextflow.enable.dsl=2

process demToGraph {
    publishDir 'output/tifs', mode: 'copy', pattern: '*.tif'
    container 'fondahub/iwd:latest'
    memory '500 MB'
    cpus 1

    input:
        tuple val(key), path(yearFile), val(year)

    output:
        tuple val(key), path("*.npy"), path("*.edgelist"), emit: npy_edgelist_tup
        tuple val(key), path("*skel.tif"), emit: skel_tup
        path("*_*.tif")

    script:
    """
    a_dem_to_graph.py ${yearFile} ${year}
    """

}
