

def query_params(raw_uri):
    param=raw_uri.split("?")[-1]
    result = {}
    
    if param == raw_uri:
        return None
    
    param_list = param.split("&")
    for param in param_list:
        key_value = param.split("=")
        result[key_value[0]] = key_value[-1]
        
    return result
        