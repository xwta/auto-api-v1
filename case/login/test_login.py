
import pytest

case_list=["/xx/xx/xx","POST",{"name":"zwx"},{"xxx":"xxx"},{"code":200}]
@pytest.mark.parametrize("url,method,data,headers,exp",[case_list],ids=["ces"])
def test_login(url,method,data,headers,exp):
    print(url,method,data,headers,exp)





if __name__ == '__main__':
    pytest.main(["-s","-q","test_login.py"])