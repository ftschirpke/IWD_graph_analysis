nextflow.enable.dsl=2

include { demToGraph } from './scripts/demToGraph'
include { extractTroughTransects } from './scripts/extractTroughTransects'
include { transectAnalysis } from './scripts/transectAnalysis'
include { networkAnalysis } from './scripts/networkAnalysis'
include { mergeAnalysisCSVs} from './scripts/mergeAnalysisCSVs'
include { graphToShapefile } from './scripts/graphToShapefile'

// default value for version parameter
params.version = 3

Tuple tuple_from_version1_file(Path file) {
    // TODO: clean up this code
    // this is simply copied from an older version to ensure that it works
    key = file.getName().split("\\.")[0].substring(8)
    year = file.getName().split("\\.")[0].split("_")[2]
    new Tuple(key, file, year)
}

Tuple tuple_from_version2_file(Path file) {
    // TODO: clean up this code
    // this is simply copied from an older version to ensure that it works
    key = file.getName().split("\\.")[0].substring(13)
    year = file.getName().split("\\.")[0].split("PERMAX_")[1]
    new Tuple(key, file, year)
}

Tuple tuple_from_version3_file(Path file) {
    // TODO: clean up this code
    // this is simply copied from an older version to ensure that it works
    key = file.getName()
    year = file.getName().split("\\.")[0].split("_")[1]
    new Tuple(key, file, year)
}



// Main workflow
workflow {

    data = null

    if (params.version == 1) {
        data = Channel.fromPath( 'data/v'+ params.version +'/*dtm*.tif' ).map {
            file -> tuple_from_version1_file(file)
        }
    } else if (params.version == 2) {
        data = Channel.fromPath( 'data/v'+ params.version +'/PERMAX*.tif' ).map { 
            file -> tuple_from_version2_file(file)
        }
    } else if (params.version == 3) {
        data = Channel.fromPath( 'data/new/aoi*.tif' ).map {
            file -> tuple_from_version3_file(file)
        }
    }

    data.view()

    demToGraph(data)

    data.join(demToGraph.out.tup).view()

    extractTroughTransects(data.join(demToGraph.out.tup))
    transectAnalysis(extractTroughTransects.out, params.version)

    networkAnalysisInput = demToGraph.out.tup.join(transectAnalysis.out)

    networkAnalysis(networkAnalysisInput, params.version)

    graphToShapefileInput = demToGraph.out.tup.join(transectAnalysis.out)
    graphToShapefileInput = graphToShapefileInput.join(networkAnalysis.out.weightedEdgelist)
    graphToShapefileInput = graphToShapefileInput.map{it -> it[0,2,3,6]}

    graphToShapefile(graphToShapefileInput)

    csv = networkAnalysis.out.csvs.map{it[1]}flatten().buffer( size: Integer.MAX_VALUE, remainder: true )

    mergeAnalysisCSVs(csv)

}
