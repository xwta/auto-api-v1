
import re

txt="/xxx/xx/${code},dsdsdsds${{add()}},dddssss${{reduse()}}"


data=re.findall("\$\{[a-z]*\}",txt)
data_tips=re.findall("\$\{\{[a-z]*()\}\}",txt)
print(data)
print(data_tips)
