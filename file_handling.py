import yaml

def get_cfg():
    cfg_file = 'config/config.yml'

    with open(cfg_file, 'r') as file:
        cfg = yaml.safe_load(file)

    return(cfg)