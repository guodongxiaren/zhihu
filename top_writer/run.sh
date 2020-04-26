#!/bin/bash
python top_writer.py |tee .README.md
cat .header.md .README.md > README.md
