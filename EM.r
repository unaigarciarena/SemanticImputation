args<-commandArgs(TRUE)
#install.packages("Amelia", repos="http://cran.rstudio.com/")
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

EMBoot<-function(path, m, data){
  
  x<-length(data[,1])
  
  suppressPackageStartupMessages(library(Amelia))

  data<-matrix(as.numeric(data), nrow = x)
  
  a.out<-amelia(x = data, p2s = 0, m = m, empri = length(data[,1]*0.1))
  
  a<-a.out$imputations$imp1
  
  for (i in 2:m)
  {
    a<-a+a.out$imputations[[i]]
  }
  
  a<-a/m
  
  write1(path, "1", a)
  
  return(a)
}

# i<-0;j<-0;k<-0
setwd(args[2])



options(warn=-1)

path<-args[1]

data<-read1(path)

data1<-EMBoot(path, 3, data)

