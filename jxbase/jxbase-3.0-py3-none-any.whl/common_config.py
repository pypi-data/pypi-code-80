"""
说明：这个配置文件是 for jxbase 这个包的

"""

# 下面这个常量 MONKEY_PATCH_ALL 表示是否使采用 gevent 的 monkey.patch_all() 给本包打猴子补丁以让同步库变成异步库
# 默认 False，表示不打补丁。因为测试发现打猴子补丁后在 ipython 下运行不正常，也担心出其他问题，
# 所以这里默认设 False，用户若确定需要使用 monkey.patch_all()，将下面这个常量改为 True，并重新 install 本包
MONKEY_PATCH_ALL = False

# --------------
# DOS 风格
DOS_ARR = [
	'DOS',
	'dos'
	]


# WINDOWS 风格
WINDOWS_ARR = [
	'WINDOWS',
	'windows'
	]


# LINUX 风格
LINUX_ARR = [
	'LINUX',
	'linux'
	]



# UNIX 风格
UNIX_ARR = [
	'UNIX',
	'unix'
	]


DOS_STYLE_ARR = DOS_ARR + WINDOWS_ARR
UNIX_STYLE_ARR = UNIX_ARR + LINUX_ARR



# --------------------------
# 程序中要用到的几种时间格式
DATE_FORMAT='%Y-%m-%d'
TIME_FORMAT='%H:%M:%S'

DATE_TIME_FORMAT1 = DATE_FORMAT + ' ' + TIME_FORMAT
DATE_TIME_FORMAT2 = DATE_FORMAT + ' - ' + TIME_FORMAT
DATE_TIME_FORMAT3 = '%Y%m%d%H%M%S'




