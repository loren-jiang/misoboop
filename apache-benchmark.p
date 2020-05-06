# output as png image
set terminal png

# save file to "benchmark.png"
set output "benchmark.png"

# graph title
set title "response vs request";

#nicer aspect ratio for image size
set size 1,0.7

# y-axis grid
set grid y

#x-axis label
set xlabel "request"

#y-axis label
set ylabel "response time (ms)"

#plot data from "benchmark.data" using column 9 with smooth sbezier lines
plot "benchmark.data" using 9 smooth sbezier with lines title "series 1"