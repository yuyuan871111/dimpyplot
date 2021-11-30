#!/usr/bin/env Rscript
args = commandArgs()

## Example of chord plot: https://jokergoo.github.io/circlize_book/book/the-chorddiagram-function.html#reduce
# Create an edge list: a list of connections between 10 origin nodes, and 10 destination nodes:
#origin <- paste0("orig ", sample(c(1:10), 20, replace = T))
#destination <- paste0("dest ", sample(c(1:10), 20, replace = T))
#data <- data.frame(origin, destination)
# Transform input data in a adjacency matrix
#adjacencyData <- with(data, table(origin, destination))
# Charge the circlize library
#library(circlize)
# Make the circular plot
#chordDiagram(adjacencyData, transparency = 0.5)

# import packages
library(magrittr)
suppressPackageStartupMessages(library(circlize))
circos.clear()

library("optparse")

# set arguments here
option_list = list(
  make_option(c("-w", "--wkdir"), type="character", default="./test_pdb", metavar="character",
              help="working directory; read and save your data here. [default= %default]"),
  make_option(c("-n", "--pdb_name"), type="character", default="7a91_delta_npt_noPBC", 
              help="input file name [default= %default]", metavar="character"),
  make_option("--chain1_name", type="character", default="S1RBD",
              help="one chain for analysis [default= %default]"),
  make_option("--chain2_name", type="character", default="hACE2",
              help="one chain for analysis [default= %default]")            
)
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)


# data from wkdir
chain1_name <- opt$chain1_name
chain2_name <- opt$chain2_name
pdb_name <- opt$pdb_name 
wkdir <- paste0(opt$wkdir, "/")
#debug
#pdb_name <- '7v80_beta_afterMD' 
#wkdir <- '/Users/yuyuan/Desktop/Work/CMDM_Lab/COVID19_Proj_toGitHub/metadata/md_results/variants_7v80/beta/7v80_beta_afterMD_dimplot/'

# define function
read_and_process <- function (wkdir, pdb_name, ext = '.dimplot.hhb.csv'){
  if (ext == '.dimplot.hhb.csv') {
    filename <- paste0(wkdir, pdb_name, ext)
    data_origin <- read.csv(filename)
    donor <- paste(data_origin$donor_chain, 
                   data_origin$donor_aapos, 
                   'hhb',
                   sep = '_')
    receptor <- paste(data_origin$receptor_chain,
                      data_origin$receptor_aapos, 
                      'hhb',
                      sep = '_')
    data <- data.frame(donor, receptor)
    return(list(data, data_origin))
    
  } else if (ext == '.dimplot.nnb.csv'){
    filename <- paste0(wkdir, pdb_name, ext)
    data_origin <- read.csv(filename)
    atom1 <- paste(data_origin$atom1_chain, data_origin$atom1_aapos, 'nnb', sep = '_')
    atom2 <- paste(data_origin$atom2_chain, data_origin$atom2_aapos, 'nnb', sep = '_')
    data <- data.frame(atom1, atom2)
    return(list(data, data_origin))
    
  } else {
    stop("please check your extension")
  }
}
shift_to_same <- function(data, regex = "S1RBD_.*"){
  data_temp <- data %>% sapply(., as.character)
  for ( i in c(1:dim(data_temp)[1]) ){
    if ( grepl(regex, data_temp[i,1]) ){
      temp <- data_temp[i,1]
      data_temp[i,1] <- data_temp[i,2]
      data_temp[i,2] <- temp
      
    }
  }
  return(data.frame(data_temp))
}

## Hydrophobic bond show
data_nnb <- read_and_process(wkdir, pdb_name, ext = '.dimplot.nnb.csv')

## H bond show
chain1_regex <- paste0(chain1_name, "_.*")
chain2_regex <- paste0(chain2_name, "_.*")

data_hhb <- read_and_process(wkdir, pdb_name, ext = '.dimplot.hhb.csv')
if ( grepl(chain1_regex, data_nnb[[1]][1,1]) ){
  data_hhb_shift <- shift_to_same(data_hhb[[1]], regex = chain1_regex)
} else if ( grepl(chain2_regex, data_nnb[[1]][1,1]) ){
  data_hhb_shift <- shift_to_same(data_hhb[[1]], regex = chain2_regex)
}

## merge all data
data_all <- data_hhb_shift
colnames(data_all) <- c('Var1', 'Var2')
data_temp <- data_nnb[[1]]
colnames(data_temp) <- c('Var1', 'Var2')
data_all <- rbind(data_all, data_temp)
#chordDiagram(data_all) #check

# Transform input data in a adjacency matrix
adjacencyData <- with(data_all, table(Var1, Var2))

# set color for hydrophobic bond and h bond
col_mat <- rand_color(length(adjacencyData), hue = 'green', luminosity = 'bright')
dim(col_mat) <- dim(adjacencyData)
col_mat[ adjacencyData < exp(log(max(adjacencyData))/3*2) ] <- '#dde0c1' # print little interactions in not so light green
hhb_length <- colnames(adjacencyData) %>% grepl("_hhb$", .) %>% sum(.)
col_mat[1:hhb_length, 1:hhb_length] <- '#d10000' #color h bond interaction (red)
rownames(adjacencyData) <- rownames(adjacencyData) %>% gsub("(\\w+)_[h|n|b]+","\\1", .)
colnames(adjacencyData) <- colnames(adjacencyData) %>% gsub("(\\w+)_[h|n|b]+","\\1", .)


# group name: chain1, chain2
name <- unique(unlist(dimnames(adjacencyData)))
name <- name[order(gsub("(\\w+)_\\w+([0-9]+)", "\\1", name), 
                   as.numeric(gsub("(\\w+)_[A-Z]+([0-9]+)", "\\2", name)))]
group <- structure(gsub("_.+", "", name), names = name)
grid.col <-  gsub(chain1_name, "#ff8400", group) %>% gsub(chain2_name, "#00c3ff", .) 


# Make the circular plot (include saving)
png(file=paste0(wkdir,"interaction_chord.png"), width=6, height=6, units = "in", res = 300) #save
circos.par(start.degree =-5)
#col_fun = colorRamp2(range(adjacencyData), c("#FFEEEE", "#FF0000"), transparency = 0.5)
chordDiagram(adjacencyData, group = group, col = col_mat, 
             annotationTrack = c("grid"), grid.col = grid.col,
             annotationTrackHeight = c(0.01), big.gap = 10,
             preAllocateTracks = 1, transparency = 0.53)
circos.track(track.index = 1, panel.fun = function(x, y) {
  circos.text(CELL_META$xcenter, CELL_META$ylim[1], CELL_META$sector.index, 
              facing = "clockwise", niceFacing = TRUE, adj = c(0, 0.5), cex = 0.5)
}, bg.border = NA)
title(gsub('_',' ', pdb_name))
invisible(dev.off()) #save
