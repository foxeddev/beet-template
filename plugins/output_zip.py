"""Plugin that outputs the data pack and the resource pack in a local directory as a zip archive."""

__all__ = [
    "OutputOptions",
    "output",
]


from typing import Optional
from pathlib import Path

from beet import Context, PluginOptions, configurable
import shutil


class OutputOptions(PluginOptions):
    directory: Optional[Path] = None


def beet_default(ctx: Context):
    ctx.require(output)


@configurable(validator=OutputOptions)
def output(ctx: Context, opts: OutputOptions):
    """Plugin that outputs the data pack and the resource pack in a local directory as a zip archive."""

    path = opts.directory or ctx.output_directory or ctx.directory
    data_path = path / f"{ctx.project_id}_{ctx.project_version}_data_pack"
    assets_path = path / f"{ctx.project_id}_{ctx.project_version}_resource_pack"

    for src in (data_path, assets_path):
        if src.exists() and src.is_dir():
            shutil.make_archive(
                str(src),
                "zip",
                root_dir=str(src),
                base_dir=".",
            )
