# coding=UTF-8
from GeoCommon import DbOperator
import sys


class ToolOperator:
    ''' 文件数据导入数据库基类'''
    m_Config = None
    m_dbOpera = None

    def __init__(self, toolconfig):
        self.m_Config = toolconfig
        self.m_dbOpera = DbOperator(self.m_Config.DATABASE_URL, self.m_Config.IMPORT_DATA_TYPE, self.m_Config)

    def CreatFormData(self, dataset=None, layernames=[]):
        '''根据相关数据生成表结构，不导入数据'''
        if dataset is None:
            sys.exit(1)
        LayerCount = dataset.GetLayerCount()
        print "开始创建数据表..."
        for i in range(LayerCount):
            layer = dataset.GetLayer(i)
            layername = layer.GetName()
            if layernames is not None and len(layernames) > 0:
                if layername not in layernames:
                    continue
            insertTable = None
            insertTable = self.m_dbOpera.CreateTable(layer)
            if insertTable is not None:
                print "表:%s创建成功" % layername
            else:
                print "表:%s创建失败" % layername
                continue

    def InsertData(self, dataset=None, layernames=[]):
        '''只导入数据'''
        LayerCount = dataset.GetLayerCount()
        print "开始导入数据..."
        for i in range(LayerCount):
            layer = dataset.GetLayer(i)
            layername = layer.GetName()
            if layernames is not None and len(layernames) > 0:
                if layername not in layernames:
                    continue
            insertTable = None
            if self.m_Config.IMPORT_IEARTHTYPE == 1:
                insertTable = self.m_dbOpera.GetIearthTahle()
            elif self.m_Config.IMPORT_IEARTHTYPE == 2:
                insertTable = self.m_dbOpera.CreateIearthAreaTable()
            else:
                insertTable = self.m_dbOpera.GetTable(layer)
            if insertTable is not None:
                print "表:%s获取成功" % layer.GetName()
            else:
                print "表:%s获取失败" % layer.GetName()
                continue
                #             导入操作
            print "开始对图层:%s进行导入操作" % layer.GetName()
            if self.m_Config.IMPORT_IEARTHTYPE == 1:
                self.m_dbOpera.InsertIearthData(insertTable[0], layer, insertTable[1])
            elif self.m_Config.IMPORT_IEARTHTYPE == 2:
                self.m_dbOpera.InsertAreaData(insertTable[0], layer, insertTable[1])
            else:
                self.m_dbOpera.InsertData(insertTable[0], layer, insertTable[1])

    def CreateAndInsert(self, dataset=None, layernames=[]):
        '''创建数据并导入数据'''
        LayerCount = dataset.GetLayerCount()
        print "开始导入数据..."
        for i in range(LayerCount):
            layer = dataset.GetLayer(i)
            layername = layer.GetName()
            if layernames is not None and len(layernames) > 0:
                if layername not in layernames:
                    continue
            insertTable = self.m_dbOpera.CreateTable(layer)
            if insertTable is not None:
                print "表:%s创建成功" % layer.GetName()
            else:
                print "表:%s创建失败" % layer.GetName()
                continue
                #             导入操作
            print "开始对图层:%s进行导入操作" % layer.GetName()
            self.m_dbOpera.InsertData(insertTable[0], layer, insertTable[1])

    def UpdateData(self, dataset=None, layernames=[]):
        """
        更新数据
        dataset:需要进行操作的数据集
        layernames:需要操作的图层列表
        """
        if dataset is None:
            print "无更新数据源"
            return
        LayerCount = dataset.GetLayerCount()
        print "开始更新数据..."
        for i in range(LayerCount):
            layer = dataset.GetLayer(i)
            layername = layer.GetName()
            if layernames is not None and len(layernames) > 0:
                if layername not in layernames:
                    continue
            updateTable = self.m_dbOpera.GetTable(layer)
            if updateTable is not None:
                print "表:%s获取成功" % layer.GetName()
            else:
                print "表:%s获取失败" % layer.GetName()
                continue
                #             导入操作
            print "开始对图层:%s进行更新操作" % layer.GetName()
            try:
                self.m_dbOpera.UpdateData(updateTable[0], layer, updateTable[1])
                self.updateFeatureStatus(layer)
            except:
                print "图层更新异常: %s" % layername

    def OpenData(self):
        '''打开数据'''
        pass

    def ExportData(self):
        '''将数据库文件导出'''
        pass

    def updateFeatureStatus(self, uLayer):
        '''更新完数据库后，需要修改源文件的状态'''
        print '开始更新源数据....'
        filterStr = self.m_Config.STATUSFILED + '<>0'
        uLayer.SetAttributeFilter(filterStr)
        uLayer.StartTransaction()
        feat = uLayer.GetNextFeature()
        while feat is not None:
            feat.SetField(self.m_Config.STATUSFILED, 0)
            uLayer.SetFeature(feat)
            uLayer.CommitTransaction()
            feat = uLayer.GetNextFeature()
        print '源数据更新完成'
