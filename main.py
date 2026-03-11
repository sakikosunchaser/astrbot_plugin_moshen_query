from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register


@register(
    "mo_cai_query",
    "sakikosunchaser",
    "魔裁群查询插件，支持地区简称查询",
    "1.0.2"
)
class MoCaiQueryPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

        self.group_data = {
            "辽宁沈阳": ["912500562"],
            "江浙沪": ["1064268361"],
            "北京": ["864946063", "983416136"],
            "山西": ["468266719"],
            "西南": ["1044753946"],
            "广东": ["1091203810"],
            "川渝": ["754903463"],
            "广西": ["1081063516"],
            "福建": ["1058911737"],
        }

        self.alias_map = {
            "北京": "北京",
            "京": "北京",

            "辽宁": "辽宁沈阳",
            "辽": "辽宁沈阳",
            "沈阳": "辽宁沈阳",
            "辽沈": "辽宁沈阳",

            "江浙沪": "江浙沪",
            "江苏": "江浙沪",
            "苏": "江浙沪",
            "浙江": "江浙沪",
            "浙": "江浙沪",
            "上海": "江浙沪",
            "沪": "江浙沪",

            "山西": "山西",
            "晋": "山西",

            "西南": "西南",
            "重庆": "西南",
            "渝": "西南",
            "四川": "西南",
            "川": "西南",
            "贵州": "西南",
            "黔": "西南",
            "云南": "西南",
            "云": "西南",
            "滇": "西南",
            "西藏": "西南",
            "藏": "西南",

            "广东": "广东",
            "粤": "广东",

            "川渝": "川渝",

            "广西": "广西",
            "桂": "广西",

            "福建": "福建",
            "闽": "福建",
        }

    def format_all(self):
        msg = ["全国魔裁群群号：", ""]
        for region, groups in self.group_data.items():
            if region == "北京":
                msg.append(f"{region}：")
                msg.append(f"1群：{groups[0]}")
                msg.append(f"2群：{groups[1]}")
            else:
                msg.append(f"{region}：{' / '.join(groups)}")
        return "\n".join(msg)

    def format_one(self, region: str):
        groups = self.group_data.get(region)
        if not groups:
            return "未找到该地区信息。"

        if region == "北京":
            return f"{region}魔裁群群号：\n1群：{groups[0]}\n2群：{groups[1]}"
        return f"{region}魔裁群群号：\n" + "\n".join(groups)

    @filter.command("魔裁查询")
    async def query(self, event: AstrMessageEvent):
        text = event.message_str.strip()

        if text.startswith("/魔裁查询"):
            keyword = text.replace("/魔裁查询", "", 1).strip()
        else:
            keyword = text.replace("魔裁查询", "", 1).strip()

        if not keyword:
            yield event.plain_result(self.format_all())
            return

        region = self.alias_map.get(keyword)
        if not region:
            yield event.plain_result(
                "未找到对应地区。\n"
                "示例：/魔裁查询 北京\n"
                "示例：/魔裁查询 京\n"
                "示例：/魔裁查询 闽\n"
                "不带参数可查看全部。"
            )
            return

        yield event.plain_result(self.format_one(region))