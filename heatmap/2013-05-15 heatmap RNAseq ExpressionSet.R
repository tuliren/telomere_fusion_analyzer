# setup the working directory
setwd("E:\\Document\\WindowsÎÄ¼þ¼Ð\\Desktop\\2012-07 NGS fusion analysis\\2013-02-07 TCGA")

# filename
exprsFile <- "2013-05-16 cluster log norm.txt"
pDataFile <- "2013-05-16 covariable.txt"
desFile <- "2013-05-16 description.txt"

# RNA seq data
exprs <- as.matrix(read.table(exprsFile, header=TRUE, sep="\t", row.names=1, as.is=T))
# check the input file
#class(exprs)
#dim(exprs)
#colnames(exprs)
#head(exprs[,1:5])

# creating minimal ExpressionSet
library("Biobase")
minimalSet <- ExpressionSet(assayData=exprs)

# import phenotypic data
pData <- read.table(pDataFile, row.names=1, header=T, sep="\t")
# check the covariable file
#dim(pData)
#rownames(pData)
#summary(pData)
#all(rownames(pData)==colnames(exprs))

# read description of covariables
metadata <- read.table(desFile, row.names=1, header=TRUE, sep="\t")

# create AnnotatedDataFrame
phenoData <- new("AnnotatedDataFrame", data=pData, varMetadata=metadata)

# assemble an ExpressionSet
RNA <- ExpressionSet(assayData=exprs, phenoData=phenoData)

# gene selection
eset <- RNA[, RNA$Category %in% c("l", "m", "s")]
library("limma")
f <- factor(as.character(eset$Category))
design <- model.matrix(~f)
fit <- eBayes(lmFit(eset, design))
# selected <- (p.adjust(fit$p.value[, 2], method="BH") < 0.96)
# no feature could pass the p.adjust < 0.05 criteria
selected <- fit$p.value[, 2] < 0.01
esetSel <- eset [selected, ]
# esetSel
# exprs(esetSel)

# heatmap
color.map <- function(Category) { if (Category=="l") "#587498" else if (Category=="m") "#587058" else "#E86850" }
patientcolors <- unlist(lapply(esetSel$Category, color.map))
library("gplots")
heatmap.2(exprs(esetSel), col=redgreen(75), scale="row", ColSideColors=patientcolors,
           key=TRUE, symkey=FALSE, density.info="histogram",
           trace="none", cexRow=0.5, labCol=esetSel$Relative_length_e9)

# toptable
topTable(fit, coef=2)
