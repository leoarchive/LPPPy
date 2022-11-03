#!/bin/bash
example_dir=./examples

for example in "$example_dir"/*
do
  if [[ $example == *.lpp ]]
  then
    python3 src/lpp.py --debug-mode $example
    if [ $? -ne 0 ]; then
      echo "$example ❌"
      exit
    else
      echo "$example ✅"
    fi
  fi
done