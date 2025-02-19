from typing import Tuple, Dict
from types import FunctionType
from uuid import UUID
from Script.Core import cache_control, game_type, get_text, flow_handle, text_handle, constant, py_cmd
from Script.Design import map_handle, handle_premise, update
from Script.UI.Moudle import draw, panel
from Script.Config import game_config, normal_config

cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """
_: FunctionType = get_text._
""" 翻译api """
line_feed = draw.NormalDraw()
""" 换行绘制对象 """
line_feed.text = "\n"
line_feed.width = 1
window_width: int = normal_config.config_normal.text_width
""" 窗体宽度 """


class Find_call_Panel:
    """
    总面板对象
    Keyword arguments:
    width -- 绘制宽度
    """

    def __init__(self, width: int):
        """初始化绘制对象"""
        self.width: int = width
        """ 绘制的最大宽度 """
        self.now_panel = _("干员位置一览")
        """ 当前绘制的食物类型 """
        self.handle_panel: panel.PageHandlePanel = None
        """ 当前名字列表控制面板 """

    def draw(self):
        """绘制对象"""
        title_draw = draw.TitleLineDraw("干员位置一览", self.width)
        self.handle_panel = panel.PageHandlePanel([], FindDraw, 60, 3, self.width, 1, 1, 0)
        while 1:
            py_cmd.clr_cmd()
            npc_list,return_list = [],[]
            title_draw.draw()
            info_draw = draw.NormalDraw()
            follow_count = cache.character_data[0].pl_ability.follow_count
            if not cache.debug_mode:
                info_draw.text = f"●当前最大同时跟随角色数量：{str(follow_count)}，跟随中的角色会带*\n\n"
            else:
                info_draw.text = "●当前最大同时跟随角色数量：999(debug模式)，跟随中的角色会带*\n\n"
            info_draw.width = self.width
            info_draw.draw()
            if cache.debug_mode:
                text = "  [一键全召集]"
                name_draw = draw.LeftButton(text, text, self.width, cmd_func=self.call_all)
                name_draw.draw()
                line_feed.draw()
                line_feed.draw()
                return_list.append(name_draw.return_text)
            # 遍历角色id
            for npc_id in cache.npc_id_got:
                if npc_id != 0:
                    npc_list.append(npc_id)
            self.handle_panel.text_list = npc_list
            self.handle_panel.update()
            self.handle_panel.draw()
            return_list.extend(self.handle_panel.return_list)
            line_feed.draw()
            back_draw = draw.CenterButton(_("[返回]"), _("返回"), window_width)
            back_draw.draw()
            line_feed.draw()
            return_list.append(back_draw.return_text)
            yrn = flow_handle.askfor_all(return_list)
            if yrn == back_draw.return_text:
                cache.now_panel_id = constant.Panel.IN_SCENE
                break

    def call_all(self):
        """一键全召集"""
        for npc_id in cache.npc_id_got:
            if npc_id != 0:
                character_data = cache.character_data[npc_id]
                character_data.sp_flag.is_follow = 1

class FindDraw:
    """
    显示可点击的NPC名字+位置按钮对象
    Keyword arguments:
    npc_id -- 干员角色编号
    width -- 最大宽度
    is_button -- 绘制按钮
    num_button -- 绘制数字按钮
    button_id -- 数字按钮id
    """

    def __init__(
        self, NPC_id: int, width: int, is_button: bool, num_button: bool, button_id: int
    ):
        """初始化绘制对象"""
        self.npc_id: int = NPC_id
        """ 干员角色编号 """
        self.draw_text: str = ""
        """ 名字绘制文本 """
        self.width: int = width
        """ 最大宽度 """
        self.num_button: bool = num_button
        """ 绘制数字按钮 """
        self.button_id: int = button_id
        """ 数字按钮的id """
        self.button_return: str = str(button_id)
        """ 按钮返回值 """
        name_draw = draw.NormalDraw()
        # print("text :",text)

        character_data = cache.character_data[self.npc_id]
        name = character_data.name
        id = str(character_data.adv).rjust(4,'0')
        scene_position = character_data.position
        scene_position_str = map_handle.get_map_system_path_str_for_list(scene_position)
        if scene_position_str[-2] == "\\" and scene_position_str[-1] == "0":
            scene_position_str = scene_position_str[:-2] + "入口"
        # scene_name = cache.scene_data[scene_position_str].scene_name
        # 输出干员名字
        now_draw_text = f"[{id}]{name}"
        # 输出跟随信息
        if character_data.sp_flag.is_follow == 1:
            now_draw_text += "*"
        # 输出地点信息
        now_draw_text += f":{scene_position_str}   "

        status_text = game_config.config_status[character_data.state].name
        # 如果是在移动，则输出目的地
        # BUG 需要查明在什么情况下会导致虽然在移动但是move_final_target为空
        if status_text == "移动" and len(character_data.behavior.move_final_target):
            now_draw_text += f"移动目的地:{character_data.behavior.move_final_target[-1]}"
        # 否则输出状态
        else:
            now_draw_text += f"正在：{status_text}"

        name_draw = draw.LeftButton(
            now_draw_text, self.button_return, self.width, cmd_func=self.see_call_list
        )
        self.draw_text = now_draw_text
        self.now_draw = name_draw
        """ 绘制的对象 """


    def draw(self):
        """绘制对象"""
        self.now_draw.draw()

    def see_call_list(self):
        """点击后进行召集"""
        # title_draw = draw.TitleLineDraw(self.text, window_width)
        return_list = []
        # title_draw.draw()
        line = draw.LineDraw("-", window_width)
        line.draw()
        character_data: game_type.Character = cache.character_data[self.npc_id]
        now_draw = draw.NormalDraw()
        if not handle_premise.handle_normal_24567(self.npc_id):
            now_draw.text = f"***{character_data.name}状态异常，无法召集***\n"
        elif character_data.sp_flag.is_follow == 0:
            if cache.debug_mode:
                character_data.sp_flag.is_follow = 1
                now_draw.text = character_data.name + "收到了博士的信息，询问了博士的位置之后开始移动\n"
            else:
                character_data.sp_flag.is_follow = 3
                now_draw.text = character_data.name + "收到了博士的信息，接下来会前往博士办公室\n"

            # 去掉其他NPC的跟随
            # if not cache.debug_mode:
            #     for npc_id in cache.npc_id_got:
            #         if npc_id != 0 and npc_id != character_id:
            #             other_character_data = cache.character_data[npc_id]
            #             if other_character_data.sp_flag.is_follow:
            #                 other_character_data.sp_flag.is_follow = 0
            #                 now_draw.text += other_character_data.name + "退出跟随模式\n"
        elif character_data.sp_flag.is_follow == 1 and cache.debug_mode:
            character_data.sp_flag.is_follow = 3
            now_draw.text = character_data.name + "收到了博士的信息，接下来会前往博士办公室\n"

        else:
            character_data.sp_flag.is_follow = 0
            now_draw.text = character_data.name + "退出跟随模式\n"
        now_draw.width = 1
        now_draw.draw()
        # back_draw = draw.CenterButton(_("[返回]"), _("返回"), window_width)
        # back_draw.draw()
        # line_feed.draw()
        # return_list.append(back_draw.return_text)
        # yrn = flow_handle.askfor_all(return_list)
        # if yrn == back_draw.return_text:
        #     break
