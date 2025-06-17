# python scripts/get_data.py qlib_data --target_dir ../qlib_data/cn_data --region cn

import qlib
# region in [REG_CN, REG_US]
from qlib.constant import REG_CN
provider_uri = "D:/project/tradenote/qlib_data/cn_data"  # target_dir
qlib.init(provider_uri=provider_uri, region=REG_CN)

# qrun benchmarks/LightGBM/workflow_config_lightgbm_Alpha1582.yaml
