import cache_control

def read_CVP(cvp_value_str: str):
    """读取CVP字符串 A能力,T素质,J宝珠,E经验,S状态,F好感度,X信赖"""
    cvp_str_list = cvp_value_str.split("_")
    # print(f"cvp_str_list = {cvp_str_list}")
    cvp_str_list[0] = cvp_str_list[0].replace("CVP", "综合数值前提  ")
    cvp_str_list[1] = cvp_str_list[1].replace("A1", "自己")
    cvp_str_list[1] = cvp_str_list[1].replace("A2", "交互对象")
    cvp_str_list[2] = cvp_str_list[2].replace("F", "好感")
    cvp_str_list[2] = cvp_str_list[2].replace("X", "信赖")
    cvp_str_list[2] = cvp_str_list[2].replace("G", "攻略程度")
    cvp_str_list[2] = cvp_str_list[2].replace("Time", "时间")
    cvp_str_list[3] = cvp_str_list[3].replace("G", "大于")
    cvp_str_list[3] = cvp_str_list[3].replace("L", "小于")
    cvp_str_list[3] = cvp_str_list[3].replace("E", "等于")
    cvp_str_list[3] = cvp_str_list[3].replace("GE", "大于等于")
    cvp_str_list[3] = cvp_str_list[3].replace("LE", "小于等于")
    cvp_str_list[3] = cvp_str_list[3].replace("NE", "不等于")
    # 将cvp_str_list转为str的cvp_str
    cvp_str = ""
    for i in cvp_str_list:
        cvp_str += i
    # print(f"debug cvp_str = {cvp_str}, cvp_str_list = {cvp_str_list}")
    # 处理A3部分
    if "A3" in cvp_str:
        a3_value = cvp_str.split("A3|")[1].split("_")[0]
        cvp_str = cvp_str.replace(f"A3|{a3_value}", f"角色id为{a3_value}")
    # 然后处理B属性部分
    if "A" in cvp_str:
        b2_value = cvp_str_list[2].split("A|")[1]
        b2_name = cache_control.ability_data[b2_value]
        cvp_str = cvp_str.replace(f"A|{b2_value}", f"能力{b2_name}")
    elif "T" in cvp_str:
        b2_value = cvp_str_list[2].split("T|")[1]
        b2_name = cache_control.talent_data[b2_value]
        cvp_str = cvp_str.replace(f"T|{b2_value}", f"素质{b2_name}")
    elif "J" in cvp_str:
        b2_value = cvp_str_list[2].split("J|")[1]
        b2_name = cache_control.juel_data[b2_value]
        cvp_str = cvp_str.replace(f"J|{b2_value}", f"宝珠{b2_name}")
    elif "E" in cvp_str:
        b2_value = cvp_str_list[2].split("E|")[1]
        b2_name = cache_control.experience_data[b2_value]
        cvp_str = cvp_str.replace(f"E|{b2_value}", f"经验{b2_name}")
    elif "S" in cvp_str:
        b2_value = cvp_str_list[2].split("S|")[1]
        b2_name = cache_control.state_data[b2_value]
        cvp_str = cvp_str.replace(f"S|{b2_value}", f"状态{b2_name}")
    # 最后去掉所有的下划线
    cvp_str = cvp_str.replace("_", "")
    return cvp_str