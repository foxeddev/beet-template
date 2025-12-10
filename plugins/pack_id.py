from beet import Context, Mcmeta


def beet_default(ctx: Context):
    for pack in ctx.data, ctx.assets:
        pack.mcmeta.merge(Mcmeta({"id": ctx.project_id}))
