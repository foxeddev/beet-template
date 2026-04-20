"""Automatically runs functions on load, tick, installed and uninstall, with support for creating and removing scoreboard objectives."""

__all__ = [
    "TaggedFunctionsOptions",
    "tagged_functions",
]

from typing import List, Optional

from beet import Context, Function, FunctionTag, PluginOptions, configurable


class TaggedFunctionsOptions(PluginOptions):
    namespace: Optional[str] = None
    load_function: Optional[str] = None
    tick_function: Optional[str] = None
    install_function: Optional[str] = None
    uninstall_function: Optional[str] = None
    scoreboard_objectives: List[str] = []


def beet_default(ctx: Context):
    ctx.require(tagged_functions)


@configurable(validator=TaggedFunctionsOptions)
def tagged_functions(ctx: Context, opts: TaggedFunctionsOptions):
    """Automatically run a function on load, tick, installed and uninstall, with support for creating and removing scoreboard objectives."""

    namespace = opts.namespace or ctx.project_id
    load_function_tag = "minecraft:load"
    tick_function_tag = "minecraft:tick"
    load_function = opts.load_function or f"{namespace}:load"
    tick_function = opts.tick_function or f"{namespace}:tick"
    install_function = opts.install_function or f"{namespace}:install"
    uninstall_function = opts.uninstall_function or f"{namespace}:uninstall"
    scoreboard_objectives = [f"{namespace}", *opts.scoreboard_objectives]
    data_pack_folder = f"{ctx.project_id}_{ctx.project_version}_data_pack"

    ctx.data.function_tags.setdefault(load_function_tag, FunctionTag()).append(
        FunctionTag({"values": [load_function]})
    )
    ctx.data.function_tags.setdefault(tick_function_tag, FunctionTag()).append(
        FunctionTag({"values": [tick_function]})
    )
    ctx.data.functions.setdefault(load_function, Function()).append(
        create_load_function(
            namespace=namespace,
            install_function=install_function,
        )
    )
    ctx.data.functions.setdefault(install_function, Function()).append(
        create_install_function(
            namespace=namespace,
            scoreboard_objectives=scoreboard_objectives,
        )
    )
    ctx.data.functions.setdefault(uninstall_function, Function()).append(
        create_uninstall_function(
            scoreboard_objectives=scoreboard_objectives,
            data_pack_folder=data_pack_folder,
        )
    )


# Functions


def create_load_function_tag(functions: str):
    return FunctionTag({"values": functions})


def create_tick_function_tag(functions: str):
    return FunctionTag({"values": functions})


def create_load_function(namespace: str, install_function: str):
    return Function(
        f"""scoreboard objectives add {namespace} dummy
execute unless score $installed {namespace} matches 1 run function {install_function}
"""
    )


def create_install_function(namespace: str, scoreboard_objectives: List[str]):
    fn = Function()

    for objective in scoreboard_objectives:
        fn.append(f"scoreboard objectives add {objective} dummy")

    fn.append(f"scoreboard players set $installed {namespace} 1")

    return fn


def create_uninstall_function(scoreboard_objectives: List[str], data_pack_folder: str):
    fn = Function()

    for objective in scoreboard_objectives:
        fn.append(f"scoreboard objectives remove {objective}")

    fn.append(
        f"""datapack disable "file/{data_pack_folder}"
datapack disable "file/{data_pack_folder}.zip"
"""
    )

    return fn
