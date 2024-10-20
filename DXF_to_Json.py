import os
from osgeo import ogr, gdal


def dxf_to_json(dxf_path):
    try:
        # 检查输入文件是否存在
        if not os.path.exists(dxf_path):
            raise FileNotFoundError(f"CAD file not found: {dxf_path}")

        # 构造输出文件路径
        basename = os.path.dirname(dxf_path)
        filename = os.path.splitext(os.path.basename(dxf_path))[0]
        outfile = os.path.join(basename, f"{filename}.json")

        # 注册所有的OGR驱动
        ogr.RegisterAll()

        # 设置GDAL和DXF相关配置
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        gdal.SetConfigOption("SHAPE_ENCODING", "")
        gdal.SetConfigOption("DXF_ENCODING", "ASCII")  # 设置DXF默认编码

        # 打开
        po_ds = ogr.Open(dxf_path, False)
        if po_ds is None:
            raise Exception(f"Failed to open CAD file: {dxf_path}")

        # 获取GeoJSON驱动
        po_driver = ogr.GetDriverByName("GeoJSON")
        if po_driver is None:
            raise Exception("GeoJSON driver not available.")

        # 保存文件为GeoJSON格式
        if os.path.exists(outfile):
            print(f"Output file already exists, overwriting: {outfile}")

        res = po_driver.CopyDataSource(po_ds, outfile)
        if res is None:
            raise Exception(f"Failed to create output file: {outfile}")

        print(f"Conversion successful! Output saved to: {outfile}")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 释放资源，关闭数据源
        if po_ds is not None:
            po_ds.Destroy()