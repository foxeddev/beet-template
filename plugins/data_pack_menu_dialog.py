"""Adds a dialog as a datapack options menu as specified in https://docs.smithed.dev/conventions/data-pack-menu/"""

from typing import Optional

from beet import Context, Dialog, DialogTag, PluginOptions, configurable


class DataPackMenuDialogOptions(PluginOptions):
    namespace: Optional[str] = None
    pack_dialog: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    website_url: Optional[str] = None
    issues_url: Optional[str] = None
    config_function: Optional[str] = None


def beet_default(ctx: Context):
    data_pack_menu_dialog(ctx)


@configurable(validator=DataPackMenuDialogOptions)
def data_pack_menu_dialog(ctx: Context, opts: DataPackMenuDialogOptions):
    """Adds a dialog as a datapack options menu as specified in https://docs.smithed.dev/conventions/data-pack-menu/"""

    namespace = opts.namespace or ctx.project_id
    root_dialog = "smithed:data_packs"
    pause_screen_dialog_tag = "minecraft:pause_screen_additions"
    data_packs_dialog_tag = "smithed:data_packs"
    pack_dialog = opts.pack_dialog or f"{namespace}:about"
    name = opts.name or ctx.project_name
    description = opts.description or str(ctx.project_description)
    version = opts.version or ctx.project_version
    author = opts.author or ctx.project_author

    ctx.data.dialogs[root_dialog] = create_root_dialog()

    if not ctx.data.dialogs_tags.get(pause_screen_dialog_tag):
        ctx.data[pause_screen_dialog_tag] = DialogTag()
    ctx.data.dialogs_tags[pause_screen_dialog_tag].merge(
        create_pause_screen_dialog_tag()
    )

    if not ctx.data.dialogs_tags.get(data_packs_dialog_tag):
        ctx.data[data_packs_dialog_tag] = DialogTag()
    ctx.data.dialogs_tags[data_packs_dialog_tag].merge(
        create_data_packs_dialog_tag(pack_dialog=pack_dialog)
    )

    ctx.data.dialogs[pack_dialog] = create_pack_dialog(
        name=name,
        description=description,
        version=version,
        author=author,
        website_url=opts.website_url,
        issues_url=opts.issues_url,
        config_function=opts.config_function,
        root_dialog=root_dialog,
    )


# Functions


def create_root_dialog():
    return Dialog(
        {
            "type": "minecraft:dialog_list",
            "external_title": {
                "translate": "menu.smithed.data_packs",
                "fallback": "%s...",
                "with": [{"translate": "selectWorld.dataPacks"}],
            },
            "title": {
                "translate": "menu.smithed.data_packs.title",
                "fallback": "%s",
                "with": [{"translate": "selectWorld.dataPacks"}],
            },
            "dialogs": "#smithed:data_packs",
            "exit_action": {"label": {"translate": "gui.back"}, "width": 200},
        }
    )


def create_pause_screen_dialog_tag():
    return DialogTag({"values": [{"id": "smithed:data_packs", "required": False}]})


def create_data_packs_dialog_tag(pack_dialog: str):
    return DialogTag({"values": [{"id": pack_dialog, "required": False}]})


def create_pack_dialog(
    name: str,
    description: str,
    version: str,
    author: str,
    website_url: Optional[str],
    issues_url: Optional[str],
    config_function: Optional[str],
    root_dialog: str,
):
    actions = []

    if website_url:
        actions.append(
            {
                "label": "Website",
                "action": {"type": "open_url", "url": website_url},
            }
        )

    if issues_url:
        actions.append(
            {
                "label": "Issues",
                "action": {"type": "open_url", "url": issues_url},
            }
        )

    if config_function:
        actions.append(
            {
                "label": "Config..",
                "action": {
                    "type": "minecraft:run_command",
                    "command": f"function {config_function}",
                },
            }
        )

    dialog_data = {
        "type": "minecraft:multi_action" if actions else "minecraft:dialog_list",
        "title": name,
        "body": [
            {
                "type": "minecraft:plain_message",
                "contents": description,
                "width": 300,
            },
            {
                "type": "minecraft:plain_message",
                "contents": {"text": f"v{version}\nby {author}", "color": "gray"},
                "width": 300,
            },
        ],
        "exit_action": {
            "action": {"type": "show_dialog", "dialog": root_dialog},
            "label": {"translate": "gui.back"},
            "width": 200,
        },
    }

    if actions:
        dialog_data["actions"] = actions
    else:
        dialog_data["dialogs"] = []

    return Dialog(dialog_data)
