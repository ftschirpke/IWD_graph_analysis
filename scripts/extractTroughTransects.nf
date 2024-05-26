nextflow.enable.dsl=2

process extractTroughTransects {

    container 'fondahub/iwd:latest'
    memory '300 MB'
    cpus 2

    input:
        tuple val(key), file(tif), file(tif_skel), file(npy), file(edgelist)
        val(version)

    output:
        tuple val(key), path("*.pkl")

    script:
    """
    b_extract_trough_transects.py ${tif} ${npy} ${edgelist} ${version}
    """

}