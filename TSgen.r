args<-commandArgs(TRUE)

suppressWarnings(suppressMessages(library(TSdist)))

options(warn=-1)

i<-args[1]

if(i==1){
  data(example.database)
  db<-t(example.database)
}
if (i==2){
  data(example.database2)
  db<-t(example.database2[[1]])
}
if(i!=1 & i!=2){
  data(example.database3)
  db<-t(example.database3[[1]])
  }
setwd(args[2])

write(db, "ts.data", sep = "\t", ncolumns = ncol(db))
