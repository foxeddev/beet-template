"""Plugin that compresses and outputs the data pack and the resource pack folders to a local directory as a zip archive."""

__all__ = ["OutputZipOptions", "output_zip"]


from typing import Optional
from pathlib import Path

from beet import Context, PluginOptions, configurable
from shutil import make_archive


class OutputZipOptions(PluginOptions):
    directory: Optional[Path] = None


def beet_default(ctx: Context):
    ctx.require(output_zip)


@configurable(validator=OutputZipOptions)
def output_zip(ctx: Context, opts: OutputZipOptions):
    """Plugin that compresses and outputs the data pack and the resource pack folders to a local directory as a zip archive."""

    path = opts.directory or ctx.output_directory or ctx.directory
    data = path / f"{ctx.project_id}_{ctx.project_version}_data_pack"
    assets = path / f"{ctx.project_id}_{ctx.project_version}_resource_pack"

    for src in (data, assets):
        if src.exists() and src.is_dir():
            make_archive(
                str(src),
                "zip",
                root_dir=str(src),
                base_dir=".",
            )
