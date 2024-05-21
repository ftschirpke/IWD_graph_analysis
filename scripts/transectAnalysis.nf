nextflow.enable.dsl=2

process transectAnalysis {
    publishDir 'output/dicts', mode: 'copy', pattern: '*transect_dict_fitted_*'
    publishDir 'output/dicts', mode: 'copy', pattern: '*transect_dict_avg_*'
    container 'fondahub/iwd:latest'

    input:
        tuple val(key), path(pkl)
        val(version)

    output:
        tuple val(key), path("*transect_dict_avg*"), path("*transect_dict_fitted_*"), emit: irgendwas
        

    script:
    """
    c_transect_analysis.py ${pkl} ${version}
    """

}