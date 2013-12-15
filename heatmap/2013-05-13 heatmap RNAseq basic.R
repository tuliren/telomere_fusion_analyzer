setwd("C:\\TLR Document\\TLR Desktop\\Laboratory\\
       2012-07 NGS fusion analysis\\2013-02-07 TCGA")
rseq_origin <- read.table("cluster.txt", sep="\t", header=T)
row.names(rseq_origin) <- rseq_origin$GeneID
rseq_origin = subset(rseq_origin, select=-GeneID)
rseq_matrix <- data.matrix(rseq_origin[1:100,])
color = rev(terrain.colors(256))
rseq_heatmap <- heatmap(rseq_matrix, Rowv=NA, Colv=NA, col = color, scale="column", margins=c(3,3))