import click

@click.group()
def cli():
    pass

@click.group()
def sam():
    pass

@click.command()
@click.option('--input-bam',help='input bam file to analyze')
@click.option('--out-corrected', default=False, help='(options) file for corrected read names and locations')
@click.option('--verbose', default=False, is_flag=True, flag_value=True)
def umistats(input_bam, out_corrected, verbose):
    """Scans the input bam for reads where the UR and UB tags are not equal and provides statistics on corrected reads"""
    import pysam
    if(out_corrected):
        outinfo_file = open(out_corrected,'wt')
    inputbam_handle = pysam.AlignmentFile(input_bam,'rb')
    correctedCount=0;
    totalCount=0;
    for read in inputbam_handle:
        totalCount+=1
        UR=read.get_tag('UR');
        UB=read.get_tag('UB');
        if(UR!=UB):
            correctedCount+=1;
            if (out_corrected):
                outinfo_file.write('{}\t{}:{}-{}\t\n'.format(read.query_name, read.reference_name,read.reference_start,read.reference_end));
        if(verbose):
            if(totalCount%100000==0):
                print('Processed {} reads'.format(totalCount));
    print('Done: {} of {} reads were corrected'.format(correctedCount,totalCount));
    ## Close the input bam file
    inputbam_handle.close();
    if(out_corrected):
        outinfo_file.close();

## Cli bindings
cli.add_command(sam)
sam.add_command(umistats)


