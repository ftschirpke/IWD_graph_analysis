nextflow.enable.dsl=2

process transectAnalysis {
    publishDir 'output/dicts_fitted', mode: 'copy', pattern: '*transect_dict_fitted_*'
    publishDir 'output/dicts_avg', mode: 'copy', pattern: '*transect_dict_avg_*'
    container 'fondahub/iwd:latest'
    memory '4 GB'
    cpus 10

    input:
        tuple val(key), path(pkl), val(year)

    output:
        tuple val(key), path("*transect_dict_avg*"), path("*transect_dict_fitted_*"), emit: tup
        

    script:
    """
    c_transect_analysis.py ${pkl} ${year}
    """

}
