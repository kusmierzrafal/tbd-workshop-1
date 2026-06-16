import time
from pyspark.sql import SparkSession, functions as F

spark = (
    SparkSession.builder
    .appName("TBD_phase_2_task_5")
    .getOrCreate()
)

EVENTS_PATH = "gs://tbd-2026l-5-data/events.parquet"
DIMENSION_PATH = "gs://tbd-2026l-5-data/dimension.parquet"

def q1_pyspark(events_path=EVENTS_PATH):
    df = spark.read.parquet(events_path)
    return (
        df
        .filter(
            (F.col("event_date") >= F.lit("2026-01-15")) &
            (F.col("event_date") < F.lit("2026-03-01"))
        )
        .groupBy("event_date", "country", "device")
        .agg(
            F.count("*").alias("impressions"),
            F.sum("was_clicked").alias("clicks"),
            (F.sum("was_clicked") / F.count("*")).alias("ctr"),
            F.sum("impression_cost").alias("total_cost"),
            F.avg("conversion_value").alias("avg_conversion_value"),
        )
        .orderBy("event_date", "country", "device")
    )

def q2_pyspark(events_path=EVENTS_PATH):
    df = spark.read.parquet(events_path)
    return (
        df
        .groupBy("campaign_id")
        .agg(
            F.count("*").alias("impressions"),
            F.sum("was_clicked").alias("clicks"),
            (F.sum("was_clicked") / F.count("*")).alias("ctr"),
            F.sum("was_converted").alias("conversions"),
            F.sum("impression_cost").alias("total_cost"),
            F.sum("conversion_value").alias("total_conversion_value"),
        )
        .orderBy(F.col("impressions").desc())
        .limit(100)
    )

def q3_pyspark(events_path=EVENTS_PATH, dimension_path=DIMENSION_PATH):
    events_df = spark.read.parquet(events_path)
    dimension_df = spark.read.parquet(dimension_path)
    return (
        events_df
        .join(dimension_df, on="campaign_id", how="inner")
        .groupBy("campaign_type", "target_segment", "bid_strategy")
        .agg(
            F.count("*").alias("impressions"),
            F.sum("was_clicked").alias("clicks"),
            (F.sum("was_clicked") / F.count("*")).alias("ctr"),
            F.sum("was_converted").alias("conversions"),
            F.sum("impression_cost").alias("total_cost"),
            F.sum("conversion_value").alias("total_conversion_value"),
        )
        .orderBy(F.col("impressions").desc())
    )

def calc_time(name, func):
    try:
        p = func()
        start = time.time()
        p.count()
        duration = time.time() - start
        print(f"Name={name}, Execution Time={duration} [s]")
        return duration
    except Exception as e:
        print(f"[Error: {e}]")
        return None

q1_time = calc_time("Q1", q1_pyspark)
q2_time = calc_time("Q2", q2_pyspark)
q3_time = calc_time("Q3", q3_pyspark)