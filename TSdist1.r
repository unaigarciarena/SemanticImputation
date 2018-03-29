args<-commandArgs(TRUE)

suppressWarnings(suppressMessages(library(TSdist)))

options(warn=-1)

i<-1
t1<-c()
t2<-c()
while(args[i]!=0){
  #print(as.numeric(args[i]))
  t1[i]<-as.numeric(args[i])
  i<-i+1
}

i<-i+1
while(i<=length(args)){
  #print(as.numeric(args[i]))
  t2[i-length(t1)-1]<-as.numeric(args[i])
  i<-i+1
}

ARLPCCepsDistance(t1, t2)
