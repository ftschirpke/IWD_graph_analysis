nextflow.enable.dsl=2

process extractTroughTransects {

    container 'fondahub/iwd:latest'
    memory '300 MB'
    cpus 2

    input:
        tuple val(key), path(tif), val(year), path(npy), path(edgelist)

    output:
        tuple val(key), path("*.pkl"), val(year)

    script:
    """
    b_extract_trough_transects.py ${tif} ${npy} ${edgelist} ${year}
    """

}
