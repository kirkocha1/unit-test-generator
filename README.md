# unit-test-generator tool

## Overview
This CLI tool allows you to select a cide file from the current directory and generate unit test for it.

## Features
- List files in the current directory.
- Select a file via a simple numbered interface.
- Read and display the content of the selected file.
- Interact with the OpenAI through a custom prompt.

## Prerequisites
Ensure you have Python installed on your system. The tool has been tested with Python 3.7 and above. You can download and install Python from [python.org](https://www.python.org/downloads/).

Set up env variable OPENAI_API_KEY with the key you generate in https://platform.openai.com/
```
export OPENAI_API_KEY=api_key
```
## Installation

### Step 1: Download the Script
Download the `test_gen.py` script to a directory of your choice on your machine.

### Step 2: Make the Script Executable
To make the script executable from anywhere on your system, you will need to modify its permissions and place it in a directory that's on your system's PATH.

