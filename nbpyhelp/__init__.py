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
    ## Loop over all the reads and check if UR and UB tags match
    for read in inputbam_handle:
        totalCount+=1
        UR=read.get_tag('UR');
        UB=read.get_tag('UB');
        if(UR!=UB):
            correctedCount+=1;
            if (out_corrected):
                outinfo_file.write('{}\t{}:{}-{}\t\n'.format(read.query_name, read.reference_name,read.reference_start,read.reference_end));
        ## Optionally print a message every 100k reads
        if(verbose):
            if(totalCount%100000==0):
                print('Processed {} reads'.format(totalCount));
    ## Print Output statics
    print('Done: {} of {} reads were corrected'.format(correctedCount,totalCount));
    ## Close the input bam file
    inputbam_handle.close();
    if(out_corrected):
        outinfo_file.close();

@click.command()
@click.option('--input-bam',help='input bam file')
@click.option('--verbose',default=False,is_flag=True,flag_value=True)
def countge(input_bam,verbose):
    """Counts number of reads with GE tag in the input bam file"""
    import pysam
    samfile=pysam.AlignmentFile(input_bam,'rb')
    ## Counters
    totalReadCount=0
    readCountWithTag=0
    ## Go over all reads
    for read in samfile:
        totalReadCount+=1
        if(verbose and totalReadCount % 1e5 == 0):
            print('Processed {} reads'.format(totalReadCount));
        try:
            gene = read.get_tag('GE');
            readCountWithTag+=1;
        except KeyError:
            pass
    samfile.close()
    ## Print output
    print('Done: With tag/without/total: {}/{}/{}'.format(readCountWithTag,totalReadCount - readCountWithTag,totalReadCount))
    
@click.command()
@click.option('--input-bam',help='input bam file')
@click.option('--output-bam',help='output bam file')
@click.option('--strip-tag',help='name of tag to strip')
@click.option('--verbose',help='verbose',default=False,is_flag=True,flag_value=True)
def striptag(input_bam,output_bam,strip_tag,verbose):
    """Strips the selected tag from all reads in the input bam file"""
    import pysam
    inputsam=pysam.AlignmentFile(input_bam,'rb')
    outputsam=pysam.AlignmentFile(output_bam,'wb',template=inputsam)
    totalReadCount=0;
    for read in inputsam:
        totalReadCount+=1;
        read.set_tag(strip_tag,None)
        outputsam.write(read)
        if(verbose and totalReadCount % 1e5 == 0):
            print('Processed {} reads'.format(totalReadCount));
    outputsam.close();
    inputsam.close();
        
## Cli bindings
cli.add_command(sam)
sam.add_command(umistats)
sam.add_command(countge)
sam.add_command(striptag)
