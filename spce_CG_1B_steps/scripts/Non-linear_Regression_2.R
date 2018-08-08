library(splines)

finite.differences <- function(x, y) {
  if (length(x) != length(y)) {
    stop('x and y vectors must have equal length')
  }
  
  n <- length(x)
  
  # Initialize a vector of length n to enter the derivative approximations
  fdx <- vector(length = n)
  
  # Iterate through the values using the forward differencing method
  for (i in 2:n) {
    fdx[i-1] <- (y[i-1] - y[i]) / (x[i-1] - x[i])
  }
  
  # For the last value, since we are unable to perform the forward differencing method 
  # as only the first n values are known, we use the backward differencing approach
  # instead. Note this will essentially give the same value as the last iteration 
  # in the forward differencing method, but it is used as an approximation as we 
  # don't have any more information
  fdx[n] <- (y[n] - y[n - 1]) / (x[n] - x[n - 1])
  
  return(fdx)
}


AA <- read.table("RDF_dat")
x <- AA$V1
y <- AA$V2

x1 <- x[x>0.2]# & x < 0.5]
y1 <- y[x>0.2]# & x < 0.5]


plot(y1 ~ x1, type="l",col="red")

xout <- seq(0.22,1.4,0.002)

XT <- spline(x1,y1,n=202,method = "fmm",xout=xout)
lines(XT$x,XT$y)

finite1 <- finite.differences(XT$x,XT$y)

X0 <- 0.0

x1 <- XT$x[XT$x < 0.25]
y1 <- XT$y[XT$x < 0.25]
m <- nls(y1 ~ b/(x1)^6, start = list( b = 0.1), trace = TRUE)
lines(x1, fitted(m), lty = 2, col = "green", lwd = 2)

b<-coef(m)[1]

xout <- seq(0.002,0.218,0.002)
yout <- b/(xout)^6
finite0 <- finite.differences(xout,yout)

XY00 <- data.frame(R=X0,X0,X0,X0,X0,V=X0,F=X0)
XY0 <- data.frame(R=xout,X0,X0,X0,X0,V=yout,F=finite0)
XY1 <- data.frame(R=XT$x,X0,X0,X0,X0,V=XT$y,F=finite1)
xout <- seq(1.402,3.5,0.002)
XY2 <- data.frame(R=xout,X0,X0,X0,X0,V=X0,F=X0)
total <- rbind(XY00,XY0, XY1,XY2) 

write.table(total,"table_CG_CG.xvg", sep="\t", row.names=F,col.names=F)

plot(total$R[1:25],total$F[1:25], type="l")

