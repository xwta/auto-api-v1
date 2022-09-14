
from utils.handle_yaml_tips.call_deps_method import call_deps_method

# import re
#
# txt="/xxx/xx/${code},${rr}dsdsdsds${{add()}},dddssss${{reduse}}"
#
#
# data=re.findall("\$\{[a-z]*\}",txt)
# tips=re.findall("\$\{\{.*\}$",txt)
# print(data)
# print(tips)

# datas="${{add()}}"
# print(datas.split("{{")[1].split("(")[0])
# print(datas.split("{{")[1].split("(")[1].split(")")[0].split(','))
#
# call_deps_method(datas.split("{{")[1].split("(")[0],datas.split("{{")[1].split("(")[1].split(")")[0].split(","))

ces="/xxx/xxx/${host},${{add(1,2)}}"
print(ces.replace("${host}","192.168.2.31"))

