args<-commandArgs(TRUE)
#install.packages("HotDeckImputation", repos="http://cran.rstudio.com/")
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

kalman<-function(path, data){
  
  suppressPackageStartupMessages(library(imputeTS))
  data1 = data
  for(i in 1:ncol(data)){
    data1[,i]<-na.seasplit(ts(data[,i]), algorithm = "kalman")
  }
  write1(path, "1", data1)
  
  return(data1)
  
}






# path<- "prets.data"
# setwd("C:\\Users\\Unai\\Desktop\\TSIM\\Python")
setwd(args[2])



options(warn=-1)

path<-args[1]

data<-read1(path)

data1<-kalman(path, data)



