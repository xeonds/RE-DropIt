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
        if not os.path.isfile(self.config_path):
            with open(self.config_path, 'w') as f:
                f.write('{"default":{"jpg": {"action": "move","param":"./"}}}')
        self.config=json.load(open(self.config_path,mode='r'))
    def save(self):                 # 保存配置
        with open(self.config_path,mode='w') as config:
            config.write(json.dumps(self.config))
    def add_rule(self, conf, rule): # 添加配置
        self.config[conf].append(rule)
        self.save()


# 文件处理类
class Handler:
    def __init__(self,rules): # 加载配置
        self.rules = rules
    def __fun_selector(self,filename):  # 根据后缀选择文件处理函数
        subname = filename.split('.')[-1]
        if subname in self.rules.keys():
            self.rules[subname](filename)
    def process(self,path): # 遍历处理文件夹下所有文件
        (dirpath, dirname,filename) = os.walk(path)
        for file in filename:
            self.__fun_selector(file)
        for dir in dirpath: # 递归处理子文件夹
            self.process(dir)

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
            if path == '\n':    # 回车结束录入路径
                break
            file_list.append(path)
        # 用配置文件初始化文件处理器，并调用process进行处理
        Handler(conf.config['default' if c=='\n' else c]).process(file_list)
    elif s == 'a':
        # 一条规则包括文件后缀名，以及对应的处理函数和参数
        rule={}
        subname=input('input subname(like txt,pdf):')
        rule[subname] = {
            'action':input('input rule(move, copy, ...):'),'param':input('input rule(move, copy, ...):')
        }
        conf.add_rule('default' if c=='\n' else c, rule)