################################
# demo版，接近伪代码，待验证
# TODO: 添加命令行参数
# TODO: 添加GUI
################################
from fun import *  # 导入文件处理函数
import json
import os

# 规则处理类
class Rule:
    def __init__(self) -> None:     # 配置加载
        self.config_path='./config.json'
        self.config={"default":{"jpg": {"action": "move","param":"./"}}}
        if not os.path.isfile(self.config_path):
            self.save()
        else:
            self.config=json.load(open(self.config_path, 'r'))
    def save(self):                 # 保存配置
        with open(self.config_path,mode='w') as config:
            config.write(json.dumps(self.config))
    def add_rule(self, conf, rule): # 添加配置
        self.config[conf] = rule
        self.save()

# 文件处理类
class Handler:
    def __init__(self,rules): # 加载配置
        self.rules = rules
    def fun_selector(self,f_path):  # 根据后缀选择文件处理函数
        subname = f_path.split('.')[-1]
        if subname in self.rules.keys():
            globals()[self.rules[subname]['action']](f_path, self.rules[subname]['param'])
    def process(self,path): # 递归遍历处理文件夹下所有文件
        path = os.path.join(path)
        if os.path.isfile(path):
            self.fun_selector(path)
        else:
            for i in os.listdir(path):
                self.process(i)
        

if __name__ == '__main__':
    conf = Rule()   # 初始化规则管理器
    file_list = []  # 初始化待处理文件清单

    # 菜单：选择配置（一个配置包含一组文件处理规则）
    c = input('select a config(enter for default):')
    # 菜单：添加规则/开始处理文件
    s = input('s for start process,a for add rule:')

    if s == 's':
        while True:
            # 将待处理文件拽到窗口上添加路径，一行一个路径
            path = input()
            if path == '':    # 回车结束录入路径
                break
            file_list.append(path)
        # 用配置文件初始化文件处理器，并调用process进行处理
        for i in file_list:
            Handler(conf.config['default' if c=='' else c]).process(i)
    elif s == 'a':
        # 一条规则包括文件后缀名，以及对应的处理函数和参数
        rule={}
        subname=input('input subname(like txt,pdf):')
        rule[subname] = {
            'action':input('input rule(move, copy, ...):'),'param':input('input param:')
        }
        conf.add_rule('default' if c=='' else c, rule)
