# coding=utf-8
from config import config, importdatatype, TOOLOPERATYPE
from GeoTool import OperatorFactory
from GeoCommon import DbOperator
from IearthAearManager import areaquest
import gdal
import numpy


class TooFactory:
    '''工具工厂'''
    m_Config = None

    def __init__(self, toolConfig):
        self.m_Config = toolConfig

    def RunTool(self):
        tool = OperatorFactory(self.m_Config)
        if self.m_Config.OPERATETYPE == TOOLOPERATYPE.CREATE:
            tool.m_ToolOperator.CreatFormData()
        elif self.m_Config.OPERATETYPE == TOOLOPERATYPE.CREATRANDINSERT:
            tool.m_ToolOperator.CreateAndInsert()
        elif self.m_Config.OPERATETYPE == TOOLOPERATYPE.INSERT:
            tool.m_ToolOperator.InsertData()
        elif self.m_Config.OPERATETYPE == TOOLOPERATYPE.UPDATE:
            tool.m_ToolOperator.UpdateData()


def CreateCopyRaster(sourcefilename, targetfilename, newValue):
    '''GeoTiff拷贝，新数据只包含一个数据'''
    fileformat = "GTiff"
    driver = gdal.GetDriverByName(fileformat)
    metadata = driver.GetMetadata()
    if metadata.get(gdal.DCAP_CREATE) == "YES":
        print("Driver {} supports Create() method.".format(fileformat))
    if metadata.get(gdal.DCAP_CREATE) == "YES":
        print("Driver {} supports CreateCopy() method.".format(fileformat))
    src_ds = gdal.Open(sourcefilename)
    dst_ds = driver.CreateCopy(targetfilename, src_ds, strict=0,
                               options=["TILED=YES", "COMPRESS=PACKBITS"])
    # Once we're done, close properly the dataset
    band = dst_ds.GetRasterBand(1)
    raster = numpy.zeros((band.YSize, band.XSize), dtype=numpy.uint16)
    for index in range(len(raster)):
        rows = raster[index]
        for rowindex in range(len(rows)):
            rows[rowindex] = newValue
    dst_ds.GetRasterBand(1).WriteArray(raster)
    dst_ds = None
    src_ds = None


if __name__ == "__main__":
    geotool = TooFactory(config)
    geotool.RunTool()
    print "操作成功"
    # CreateCopyRaster('F:\\hefei\\clip\\4c90631948e5448b8a1caeb75b8c0c21.tif','F:\\temp\\jxsfz.tif',40)
