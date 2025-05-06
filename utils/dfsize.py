import polars
df = polars.DataFrame(
    {
        "x": list(reversed(range(1_000_000))),
        "y": [v / 1000 for v in range(1_000_000)],
        "z": [str(v) for v in range(1_000_000)],
    },
    schema=[("x", polars.UInt32), ("y", polars.Float64), ("z", polars.String)],
)
print(df.estimated_size("mb"))
print(df.height)