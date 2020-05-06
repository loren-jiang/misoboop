#!/bin/bash


eval "$1";
gnuplot  "apache-benchmark.p";
eog "benchmark.png";