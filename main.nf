nextflow.enable.dsl=2

include { demToGraph } from './scripts/demToGraph'
include { extractTroughTransects } from './scripts/extractTroughTransects'
include { transectAnalysis } from './scripts/transectAnalysis'
include { networkAnalysis } from './scripts/networkAnalysis'
include { mergeAnalysisCSVs} from './scripts/mergeAnalysisCSVs'
include { graphToShapefile } from './scripts/graphToShapefile'

// default value for version parameter
params.version = 3

// Main workflow
workflow {

    data = Channel.fromPath( params.indir + '/aoi*.tif' ).map {
        file -> {
            key = file.getName()
            year = file.getName().split("\\.")[0].split("_")[1]
            new Tuple(key, file, year)
        }
    }

    demToGraph(data)

    extractTroughTransects(data.join(demToGraph.out.npy_edgelist_tup))

    transectAnalysis(extractTroughTransects.out)
    
    networkAnalysisInput = demToGraph.out.npy_edgelist_tup.join(demToGraph.out.skel_tup)
    networkAnalysisInput = networkAnalysisInput.join(transectAnalysis.out.tup)
    networkAnalysis(networkAnalysisInput)

    graphToShapefileInput = demToGraph.out.npy_edgelist_tup.join(networkAnalysis.out.weightedEdgelist)
    graphToShapefile(graphToShapefileInput)

    csvs = networkAnalysis.out.csvs.flatten().collect()
    mergeAnalysisCSVs(csvs)

}
