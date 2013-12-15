# setup the working directory
setwd("C:\\TLR Document\\TLR Desktop\\Laboratory\\
       2012-07 NGS fusion analysis\\2013-02-07 TCGA")

# RNA seq data
rseq_origin <- read.table("clean.txt", sep="\t", header=T)
rownames(rseq_origin) <- rseq_origin$SampleID
rseq_origin = subset(rseq_origin, select=-SampleID)
rseq_origin <- t(rseq_origin)
rseq_origin <- data.frame(rseq_origin)

rseq_origin[1:4, 1:4]

# extend seq data with metadata about the samples
rseq_label <- read.table("label.txt", sep="\t", header=T)
rownames(rseq_label) <- rseq_label$Sample
rseq_merge <- merge(rseq_label, rseq_origin)

# select 1000 genes
rseq <- rseq_merge[, 1:100]

# construct the AnnotatedDataFrame
#rseq <- AnnotatedDataFrame(rseq_merge)

# modeling for heatmap
library("limma")
rseq_f <- factor(as.character(rseq$Category))
rseq_design <- model.matrix(~rseq_f)
rseq_fit <- eBayes(lmFit(data.matrix(rseq),rseq_design))
rseq_selected <- p.adjust(rseq_fit$p.value[, 2]) <0.05
rseqSel <- rseq [rseq_selected, ]
color.map <- function(mol.biol) { if (Category=="1") "#FF0000" else "#0000FF" }
patientcolors <- unlist(lapply(rseqSel$Category, color.map))
library("gplots")
heatmap.2(exprs(rseqSel), col=redgreen(75), scale="row", ColSideColors=patientcolors,
           key=TRUE, symkey=FALSE, density.info="none", trace="none", cexRow=0.5)


library("ALL")
data("ALL")
eset <- ALL[, ALL$mol.biol %in% c("BCR/ABL", "ALL1/AF4")]
library("limma")
f <- factor(as.character(eset$mol.biol))
design <- model.matrix(~f)
fit <- eBayes(lmFit(t,design))
selected  <- p.adjust(fit$p.value[, 2]) <0.05
esetSel <- eset [selected, ]
color.map <- function(mol.biol) { if (mol.biol=="ALL1/AF4") "#FF0000" else "#0000FF" }
patientcolors <- unlist(lapply(esetSel$mol.bio, color.map))
library("gplots")
heatmap.2(exprs(esetSel), col=redgreen(75), scale="row", ColSideColors=patientcolors,
           key=TRUE, symkey=FALSE, density.info="none", trace="none", cexRow=0.5)