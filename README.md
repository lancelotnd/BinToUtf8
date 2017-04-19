# BinToUtf8
## The code is quite messy, you have been warned
A simple python program that converts a binary file into a utf8 representation for use with neural network such as torch-rnn or char-rnn

Its just a simple python version of [bintoutf8_pseudo.txt](http://robbi-985.homeip.net/information/bintoutf8_pseudo.txt) from [Neural Network Learns to Generate Voice (RNN/LSTM)](https://www.youtube.com/watch?v=FsVSZpoUdSU)

Tested on linux only don't know if it works on windows

How to use:
```
$ python bintoutf.py
Usage:
	python bintoutf.py -e <input> <output> Encodes a file
	python bintoutf.py -d <input> <output> Decodes a file
```