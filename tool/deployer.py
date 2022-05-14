"""
deployer.py 
Motivation:
    1. Wrap the function and libs codes into a single zip file.
    2. Take the base64 encoded string
    3. Create a ConfigMap object, embed the payload under `data:code`
    4. Deploy the ConfigMap onto the environment
"""
