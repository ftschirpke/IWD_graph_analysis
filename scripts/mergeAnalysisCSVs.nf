nextflow.enable.dsl=2

process mergeAnalysisCSVs {
    publishDir 'output/csv', mode: 'copy'
    container 'fondahub/iwd:latest'
    memory '500 MB'
    cpus 4

    input:
        path("*.csv")

    output:
        path "merged_csv.csv"

    script:
    """
    merge_csvs.py `pwd`
    """

}
