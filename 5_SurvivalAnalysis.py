
import os

topgene_file = "out_4_topGenes.tsv"
case_file = "out_1_getFileList_ByCase.tsv"

genecount=0

with open(topgene_file, "r") as fh:
    for line in fh:  # For each Gene
        ln = line.rstrip().split("\t")
        geneName = ln[-2]
        numCasesForGene = ln[-1]
        genecount+=1
        print('Genename = ' + geneName + '\t\tGene Count = ' + str(genecount) + '\t\tNum Cases Per Gene = ' + numCasesForGene)
         
        filecount=0
        if int(numCasesForGene) < 140 and int(numCasesForGene) > 30:
            os.chdir('./GDC_DATA/')
            directory = r'.'
            # for each geneName, read all .out files and get topGene indicator value and write filename, HL value
            for entry in os.scandir(directory): # For each HTSEQ file
                if entry.path.endswith(".htseq.counts.out") and entry.is_file():
                    with open(entry.path) as f:
                        datafile = f.readlines()
                        for line in datafile:
                            if geneName in line:
                                items=line.split()
                                end = entry.path.find('.out',2)
                                filename = entry.path[2:end]+'.gz' 
                                topgenes = items[3]
                                filecount+=1
                                # print('Processing htseq file number = ' + str(filecount))
                                # print(filename +"\t"+topgenes+"\t"+filecount)
                                os.chdir('../')
                                with open(case_file, "r") as fc:
                                    casefile = fc.readlines()
                                    for line in casefile:
                                        if filename in line:
                                            citems=line.split()
                                            submitterid = citems[0]
                                            days= citems[4]
                                            gender=citems[5]
                                            race=citems[6]
                                            # print('***'+submitterid+'***'+days)
                                os.chdir('./GDC_DATA/')
                                os.chdir('./Genes')
                                with open(geneName+'.txt', "a") as output_file:
                                    output_file.write(submitterid +"\t"+ days +"\t"+ "1" +"\t"+ topgenes +"\t"+ gender + "\t"+ race + "\n")            
                                    os.chdir('../')
            print('\t\tHTSEQ files processed = ' + str(filecount))
            os.chdir('../')
            output_file.close()               