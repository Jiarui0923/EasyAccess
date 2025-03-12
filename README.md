<img src="images/tulane_long.png" width="128px"><img src="images/icon_apl.png" width="256px"><img src="images/icon_long.png" width="128px"> 

# EasyAccess
`UPDATED: 2025/03/11`
This is part of [Antigen Processing Likelihood (APL) Suite](https://github.com/Jiarui0923/APL) Project.

## Introduction
EasyAccess is a Python package designed to seamlessly connect to and interact with EasyAPI. This package provides a user-friendly interface to access EasyAPI's algorithms as if they were local Python functions, simplifying remote computation tasks. It also includes features for automatic organization and visualization of documentation, making it easier to understand and use available functionalities.

This package is ideal for developers and researchers looking for a straightforward way to leverage EasyAPI's computational capabilities while maintaining a Pythonic workflow.

For detailed usage instructions, installation steps, and API references, please refer to the documentation included with the project or explore the source code.

If there is any issue, please put up with an issue or contact Jiarui Li (jli78@tulane.edu)

## Requirements
All code was developed in Python 3.12.x.

|Package|Version|Usage|Website|Require|
|:------|:-----:|:----|:-----:|:-----:|
|requests <img src="https://requests.readthedocs.io/en/latest/_static/requests-sidebar.png" width="24pt">|`2.32.3`|HTTP Requests|[🔗](https://requests.readthedocs.io/en/latest/)|`REQUIRED`|
|websocket-client|`1.8.0`|WebSocket Requests|[🔗](https://websocket-client.readthedocs.io/en/latest/)|`REQUIRED`|
|pandas <img src="https://pandas.pydata.org/docs/_static/pandas.svg" width="52pt">|`2.2.2`|Data processing|[🔗](https://pandas.pydata.org/)|`REQUIRED`|
|markdown |`3.6`|Markdown Render|[🔗](https://python-markdown.github.io/)|`REQUIRED`|
|docflow|`1.0.0`|Markdown Render|[🔗](https://github.com/Jiarui0923/DocFlow)|`REQUIRED`|

The markdown documentation is generated by DocFlow, `1.0.0` version of which is embedded to this package.
The details about docflow could be found at: https://github.com/Jiarui0923/DocFlow


## Getting Started
This is a quick start guideline.  
To connect to one EasyAPI server, host, API ID, and API key are required. Then a an EasyAccess Client could be created following:
```python
from easyaccess import EasyAccess
client = EasyAccess('http://localhost:8000', api_id='your_api_id', api_key='your_api_key')
```
Then, directly call `client` could check the available algorithms on this server:
```python
client
```
Example output:
```markdown
# local
Authenticated as `your_api_id`

- seq_entropy: Sequence Entropy
- select_chain: Select Chains from PDB File
```
Next, to access any function in the list, just need to index it in the `client`.  
Index `select_chain` as an example:
```python
client['select_chain']
```
This is the example output:
```markdown
### Select Chains from PDB File  

_source: local_  
`0.0.1`  
Select destinated chains from the given PDB file.  
  
#### Parameters  
- **pdb**: (string:**PDB File**)=`None`; The input PDB file.; (`None`) The protein PDB file.  
- **chain**: (string:**PDB Chain IDs**)_[OPTIONAL]_=`A`; The selected protein chains ID.; (`[A-Za-z0-9]+(,[A-Za-z0-9]+)*`) The protein chain ids, seperate with `,`, no blank character.  
#### Returns  
- **pdb**: (string:**PDB File**)=`None`; The output PDB file that only contains selected chains.; (`None`) The protein PDB file.  
#### References  

```
To run this algorithm, just need to call it as a python function. (Notice: required parameters must be provided)
```python
client['select_chain'](pdb=pdb_string, chain='A')
```
Then, the output would be a dictionary with all `Returns` section mentioned items as keys.

