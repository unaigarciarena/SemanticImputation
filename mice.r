args<-commandArgs(TRUE)
#install.packages("mice", repos="http://cran.rstudio.com/")
read1<-function(path){
  data<- read.csv(path, header = FALSE, stringsAsFactors=FALSE, na.strings = "NaN", sep = "\t")
  data<-matrix(unlist(data), ncol = ncol(data))
  data[is.nan(data)]<-NA
  
  malas<-c()
  for(i in 1:length(data[1,])){
    if(2 > length(levels(factor(data[,i]))))
      malas[length(malas)+1]<-i
  }
  print(malas)
  if(length(malas)>0)
    data<-data[,-malas]
  
  return(data)
}

write1<-function(path, method, data){
  
  dir<-strsplit(path, "[.]")
  dir = paste(unlist(dir)[1], method, ".", unlist(dir)[2], sep = "")
  write(t(data), dir, ncolumns = ncol(data), sep = "\t")
}


mice1<-function(path, data){
  
  suppressPackageStartupMessages(library(mice))
  
  x<-length(data[,1])

  
  data<-matrix(as.numeric(data), nrow = x)
  
  imp <- mice(data, print = FALSE)
  imp <- complete(imp)
  data<-matrix(unlist(imp), ncol = ncol(imp))
  write1(path, "1", data)
  
  return(cbind(data, class))
}

# i<-0;j<-0;k<-0
setwd(args[2])



options(warn=-1)

path<-args[1]

data<-read1(path)

data1<-mice1(path, data)
