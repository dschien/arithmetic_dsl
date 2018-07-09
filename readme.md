# Installation

## Install Antrl
http://www.antlr.org/
```bash
OS X
$ cd /usr/local/lib
$ sudo curl -O https://www.antlr.org/download/antlr-4.7.1-complete.jar
$ export CLASSPATH=".:/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH"
$ alias antlr4='java -jar /usr/local/lib/antlr-4.7.1-complete.jar'
$ alias grun='java org.antlr.v4.gui.TestRig'

```

## Check Java installation
Must be >6 (`java -version`) if not ->
https://stackoverflow.com/questions/26252591/mac-os-x-and-multiple-java-versions

## Install python runtime
`pip install antlr4-python2-runtime`

## Then, run ANTLR to compile the grammar and generate Python.
`java -Xmx500M -cp /usr/local/lib/antlr-4.7.1-complete.jar org.antlr.v4.Tool -Dlanguage=Python2 arithmetic.g4`

