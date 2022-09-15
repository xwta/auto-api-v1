

import re

def search_dict_rules(params_dict):
    if not isinstance(params_dict,dict):
        return
    for key,value in params_dict.items():
        if isinstance(value,dict):
            search_dict_rules(value)
        elif isinstance(value,str):
            setting_re = re.findall(r"\$\{\w+\}", value)
            cacheOrMethod_re = re.findall(r"\$\{{2}[^$]+\}{2}", value)
            try:
                params_dict[key]=value.replace(setting_re[0],"zwx")
            except:
                pass
            try:
                params_dict[key]=value.replace(cacheOrMethod_re[0],"yxy")
            except:
                pass

    return params_dict


data={'name':'${name}','age':{'name':'${{add()}}'}}

result=search_dict_rules(data)
print(result)


