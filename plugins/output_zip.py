"""Plugin that outputs the data pack and the resource pack in a local directory as a folder and zip archive."""

__all__ = [
    "OutputOptions",
    "output",
]


from typing import Optional
from pathlib import Path

from beet import Context, PluginOptions, configurable


class OutputOptions(PluginOptions):
    directory: Optional[Path] = None


def beet_default(ctx: Context):
    ctx.require(output)


@configurable(validator=OutputOptions)
def output(ctx: Context, opts: OutputOptions):
    """Plugin that outputs the data pack and the resource pack in a local directory as a folder and zip archive."""

    path = opts.directory or ctx.output_directory or ctx.directory

    ctx.data.save(
        path=path / f"{ctx.project_id}_{ctx.project_version}_data_pack.zip",
        overwrite=True,
    )
    ctx.assets.save(
        path=path / f"{ctx.project_id}_{ctx.project_version}_resource_pack.zip",
        overwrite=True,
    )

    ctx.data.save(
        path=path / f"{ctx.project_id}_{ctx.project_version}_data_pack",
        overwrite=True,
    )
    ctx.assets.save(
        path=path / f"{ctx.project_id}_{ctx.project_version}_resource_pack",
        overwrite=True,
    )
