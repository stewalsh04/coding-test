params.reads = "$baseDir/data/breaks/*.bed" 
params.AsiSI = "$baseDir/references/chr21_AsiSI_sites.t2t.bed"

read_pairs_ch = Channel
            .fromPath(params.reads)
            .map { path -> tuple(path.baseName, path) }

process intersect {

    input:
    tuple val(id), path(reads)
    path AsiSI

    output:
    tuple val(id), path('*.csv')

    script:
    """
    bedtools intersect -a $AsiSI -b $reads > ${id}.csv -c
    """
}

process summary_metrics {

    input:
    tuple val(id), path(beds), path(intersects)

    output:
    path('*.csv')

    script:
    """
    python /home/steve/nextflow/bin/bed_processing.py $id ${intersects} $beds
    """
}

process collect_files {

    publishDir "./outputs"

    input:
    path metrics

    output:
    path('*.txt')

    script:
    """
    echo "SampleName,TotalBreaks,NormalisedBreaks,TotalIntersect,TotalNormalisedAsiSIbreaks,PercentageAsiSIBreaks" > summary.txt
    cat $metrics >> summary.txt
    """
}

process get_plot {

    publishDir "./outputs"

    input:
    path summary

    output:
    path('*png')

    script:
    """
    python /home/steve/nextflow/bin/plotter.py $summary
    """
}

workflow {
    intersect(read_pairs_ch,params.AsiSI)
    combined = intersect.out.combine(read_pairs_ch, by: 0)
    summary_metrics(combined)
    summary_metrics_list = summary_metrics.out.toList()
    collect_files(summary_metrics_list)
    get_plot(collect_files.out)
}
