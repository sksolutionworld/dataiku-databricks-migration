"""Deterministic PySpark transformations generated from the Dataiku flow."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def prepare_titanic(df: DataFrame) -> DataFrame:
    family_size = F.col("SibSp") + F.col("Parch") + F.lit(1)
    return (
        df.withColumn("Name", F.regexp_replace(F.col("Name"), r"[\x20\t\r\n]+$", ""))
        .withColumn("HasCabin", F.when(F.col("Cabin").isNull() | (F.trim("Cabin") == ""), 0).otherwise(1))
        .withColumn("Age", F.coalesce(F.col("Age"), F.lit(28.0)))
        .withColumn("Embarked", F.coalesce(F.col("Embarked"), F.lit("UNKNOWN")))
        .withColumn("Cabin", F.coalesce(F.col("Cabin"), F.lit("NO_CABIN")))
        .withColumn("FamilySize", family_size)
        .withColumn("IsAlone", F.when(F.col("FamilySize") == 1, 1).otherwise(0))
        .withColumn("FarePerPerson", F.col("Fare") / F.col("FamilySize"))
    )


def distinct_rows(df: DataFrame) -> DataFrame:
    return df.distinct()


def split_survival(df: DataFrame) -> tuple[DataFrame, DataFrame]:
    return df.filter(F.col("Survived") == 1), df.filter(F.col("Survived") == 0)


def stack_survival(survived: DataFrame, not_survived: DataFrame) -> DataFrame:
    return survived.unionByName(not_survived)


def summarize_by_sex_and_class(df: DataFrame) -> DataFrame:
    return df.groupBy("Sex", "Pclass").agg(
        F.count("PassengerId").alias("PassengerId_count"),
        F.avg("Survived").alias("Survived_avg"),
        F.avg("Age").alias("Age_avg"),
        F.avg("Fare").alias("Fare_avg"),
        F.avg("FarePerPerson").alias("FarePerPerson_avg"),
    )


def pivot_survival_by_class(df: DataFrame) -> DataFrame:
    """Match Dataiku pivot: rows=Sex, columns=Pclass, content=average Survived."""
    pivoted = df.groupBy("Sex").pivot("Pclass", [1, 2, 3]).agg(F.avg("Survived"))
    return (
        pivoted.withColumnRenamed("1", "1_Survived_avg")
        .withColumnRenamed("2", "2_Survived_avg")
        .withColumnRenamed("3", "3_Survived_avg")
    )


def join_summary(passengers: DataFrame, summary: DataFrame) -> DataFrame:
    return passengers.join(summary, on=["Sex", "Pclass"], how="left")


def add_fare_rank(df: DataFrame) -> DataFrame:
    window = Window.partitionBy("Pclass").orderBy(F.col("Fare").desc(), F.col("PassengerId").asc())
    return df.withColumn("FareRankWithinClass", F.row_number().over(window))


def select_final_columns(df: DataFrame) -> DataFrame:
    return df.select(
        "PassengerId", "Name", "Sex", "Pclass", "Survived", "Age", "SibSp", "Parch",
        "FamilySize", "IsAlone", "Ticket", "Fare", "FarePerPerson", "Cabin", "HasCabin",
        "Embarked", "FareRankWithinClass",
        F.col("PassengerId_count").alias("SexClassPassengerCount"),
        F.col("Survived_avg").alias("SexClassSurvivalRate"),
        F.col("Age_avg").alias("SexClassAverageAge"),
        F.col("Fare_avg").alias("SexClassAverageFare"),
        F.col("FarePerPerson_avg").alias("SexClassAverageFarePerPerson"),
    )
