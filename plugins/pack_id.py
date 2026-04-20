"""Adds an id field to pack.mcmeta files of data and resource pack as specified in https://docs.smithed.dev/conventions/pack-ids/"""

__all__ = ["PackIdOptions", "pack_id"]


from typing import Optional

from beet import Context, PluginOptions, configurable, Mcmeta


class PackIdOptions(PluginOptions):
    id: Optional[str] = None


def beet_default(ctx: Context):
    pack_id(ctx)


@configurable(validator=PackIdOptions)
def pack_id(ctx: Context, opts: PackIdOptions):
    """Adds an id field to pack.mcmeta files of data and resource pack as specified in https://docs.smithed.dev/conventions/pack-ids/"""

    id = opts.id or ctx.project_id

    for pack in ctx.data, ctx.assets:
        pack.mcmeta.merge(Mcmeta({"id": id}))
