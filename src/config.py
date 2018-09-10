# coding=UTF-8


# 导入数据类型
class importdatatype:
    def __init__(self):
        pass

    # shapefile单个文件
    SHAPEFILE = 1
    # GDB数据库
    FILEGEODATABASE = 2
    # MDB数据库
    PERSONALGEODATABASE = 3
    # shapfile文件夹
    SHAPEFILEPATH = 4
    # 栅格数据
    RASTER = 5
    # 其他数据格式
    OTHER = 0


# 工具操作类型
class TOOLOPERATYPE:
    # 只导入
    INSERT = 1
    # 创建表并导入
    CREATRANDINSERT = 2
    # 更新
    UPDATE = 3
    # 导出
    EXPORT = 4
    # 创建表结构
    CREATE = 5
    # 创建GIS物体对象
    CREATEOBJECT = 6


class IEARTHDATATYPE:
    '''导入数据类型'''
    # 智慧城市基础数据
    IEARTHDATA = 1
    # 智慧城市区域数据
    IEARA = 2
    # 其他数据
    OTHER = 0


# 工具配置
class config:
    '''数据库配置'''
    DATABASE_URL = "postgresql://dev:asdasd123@192.168.1.158/sz_db"
    # DATABASE_URL = "postgresql://dba_iearth:fengdays0105@10.28.11.7/db_iearth_gis"
    # DATABASE_URL = "postgresql://dba_iearth:fengdays0105@192.168.1.201/db_iearth_gis"
    '''导入文件类型'''
    Enum = importdatatype()
    IMPORT_DATA_TYPE = Enum.FILEGEODATABASE
    '''导入文件路径'''
    IMPORTFILENAME = 'F:\\ygc\\20180825\\vearth_1.gdb'
    '''导入方式，如果数据库中有表，则使用更新方式；如果没有表则使用创建并导入的方式'''
    OPERATETYPE = TOOLOPERATYPE.UPDATE
    '''导入数据类型，后续可以不用这个配置'''
    IMPORT_IEARTHTYPE = IEARTHDATATYPE.OTHER
    '''全局ID字段'''
    FEATUREID = "globalid"
    '''忽略字段，表示这些字段将不会导入和更新到数据库中'''
    IGNORFIELD = ['shape_length', 'shape_area']
    '''同步状态字段'''
    STATUSFILED='status'
