import json
from pathlib import Path

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register


@register(
    "mo_cai_query",
    "sakikosunchaser",
    "魔裁群与活动查询插件，支持地区简称查询和活动查询",
    "2.0.0"
)
class MoCaiQueryPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

        base_dir = Path(__file__).parent
        data_dir = base_dir / "data"

        self.groups_file = data_dir / "groups.json"
        self.activities_file = data_dir / "activities.json"

        self.group_data = self._load_json(self.groups_file, {})
        self.activity_data = self._load_json(self.activities_file, [])

        self.alias_map = self.group_data.get("aliases", {})
        self.regions = self.group_data.get("regions", {})

    def _load_json(self, file_path: Path, default):
        if not file_path.exists():
            return default
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default

    def format_all_groups(self):
        msg = ["全国魔裁群群号：", ""]
        for region, groups in self.regions.items():
            if len(groups) == 1:
                msg.append(f"{region}：{groups[0]}")
            else:
                msg.append(f"{region}：")
                for idx, group_id in enumerate(groups, start=1):
                    msg.append(f"{idx}群：{group_id}")
        return "\n".join(msg)

    def format_one_group(self, region: str):
        groups = self.regions.get(region)
        if not groups:
            return "未找到该地区信息。"

        if len(groups) == 1:
            return f"{region}魔裁群群号：\n{groups[0]}"

        msg = [f"{region}魔裁群群号："]
        for idx, group_id in enumerate(groups, start=1):
            msg.append(f"{idx}群：{group_id}")
        return "\n".join(msg)

    def format_all_activities(self):
        if not self.activity_data:
            return "目前暂无已记录的魔裁活动。"

        msg = ["当前有计划的魔裁活动：", ""]
        for item in self.activity_data:
            name = item.get("name", "未命名活动")
            group_id = item.get("group", "未知群号")
            msg.append(f"{name}：{group_id}")
        return "\n".join(msg)

    @filter.command("魔裁查询")
    async def query_group(self, event: AstrMessageEvent):
        text = event.message_str.strip()

        if text.startswith("/魔裁查询"):
            keyword = text.replace("/魔裁查询", "", 1).strip()
        else:
            keyword = text.replace("魔裁查询", "", 1).strip()

        if not keyword:
            yield event.plain_result(self.format_all_groups())
            return

        region = self.alias_map.get(keyword, keyword if keyword in self.regions else None)
        if not region:
            yield event.plain_result(
                "未找到对应地区。\n"
                "示例：/魔裁查询 北京\n"
                "示例：/魔裁查询 京\n"
                "示例：/魔裁查询 鲁\n"
                "不带参数可查看全部。"
            )
            return

        yield event.plain_result(self.format_one_group(region))

    @filter.command("魔裁活动查询")
    async def query_activity(self, event: AstrMessageEvent):
        yield event.plain_result(self.format_all_activities())