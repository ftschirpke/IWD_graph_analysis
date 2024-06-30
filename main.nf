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

    demToGraph(data)

    extractTroughTransects(data.join(demToGraph.out.npy_edgelist_tup))

    transectAnalysis(extractTroughTransects.out)

    
    networkAnalysisInput = demToGraph.out.npy_edgelist_tup.join(demToGraph.out.skel_tup)
    networkAnalysisInput = networkAnalysisInput.join(transectAnalysis.out)
    networkAnalysis(networkAnalysisInput)

    graphToShapefileInput = demToGraph.npy_edgelist_tup.join(networkAnalysis.out.weightedEdgelist)
    graphToShapefile(graphToShapefileInput)

    csv = networkAnalysis.out.csvs.map{it[1]}flatten().buffer( size: Integer.MAX_VALUE, remainder: true )

    mergeAnalysisCSVs(csv)

}
