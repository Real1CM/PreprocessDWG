import json


def convert_to_dialog(data):
    dialogs = []
    for feature in data['features']:
        properties = feature['properties']
        geometry = feature['geometry']

        layer = properties.get("Layer", "未知图层")
        subclass = properties.get("SubClasses", "未知子类")
        handle = properties.get("EntityHandle", "未知句柄")
        text = properties.get("Text", "未知文本")

        # 提取几何类型和坐标
        geometry_type = geometry.get("type", "未知类型")
        coordinates = geometry.get("coordinates", "未知坐标")

        # 判断是否有文本内容
        text_content = properties.get("文本内容", None)

        if text_content:
            dialog = (
                f"这个对象位于'{layer}'图层，它是一个‘{text}’对象，内容是'{text_content}'，"
                f"实体句柄是{handle}，几何类型是{geometry_type}，坐标为{coordinates}。"
            )
        else:
            dialog = (
                f"这个对象属于'{layer}'图层，它的子类是{subclass.split(':')[-1]}，"
                f"实体句柄是{handle}，几何类型是{geometry_type}，坐标为{coordinates}。"
            )

        dialogs.append(dialog)

    return dialogs

def json_to_dialogue(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = file.read()

    # 将字符串解析为字典
    try:
        data = json.loads(data)  # 将 JSON 字符串转换为 Python 字典
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return

    # 运行函数并生成对话列表
    dialogs = convert_to_dialog(data)

    # 将对话保存到文件中
    output_file = "output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for dialog in dialogs:
            f.write(dialog + "\n")