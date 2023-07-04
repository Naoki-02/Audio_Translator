import configparser

conf = configparser.ConfigParser()
conf.read('config.ini',encoding='utf-8')

class config:
    
    def write_ini(dir_path):
        conf.set('USER','Dir_path',dir_path)
        
        with open ('config.ini','w') as f:
            conf.write(f)
            
    def read_ini():
        dir_path = conf.get('USER','Dir_path')
        return dir_path