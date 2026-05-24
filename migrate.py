import duckdb
from pathlib import Path


con = duckdb.connect("complaints.duckdb")

# con.execute("""
# CREATE TABLE complaints AS
# SELECT *
# FROM read_csv_auto('rows.csv', SAMPLE_SIZE=-1, header=True)
# """)


con.execute("""
CREATE OR REPLACE TABLE complaints AS
SELECT
    "Date received"                AS date_received,
    "Product"                      AS product,
    "Issue"                        AS issue,
    "Company"                      AS company,
    "State"                        AS state,
    "Submitted via"                AS channel,
    "Company response to consumer" AS response,
    "Complaint ID"                 AS complaint_id,
    "Date sent to company"         AS date_sent,

    CASE WHEN "Timely response?" THEN 'Yes' ELSE 'No' END AS timely,
    NULLIF("Consumer disputed?", 'N/A') AS disputed,
    DATE_DIFF('day', "Date received", "Date sent to company") AS days_to_resolve
FROM read_csv_auto('rows.csv', SAMPLE_SIZE=-1, header=True)
WHERE "Date received" IS NOT NULL
""")


# index improve query
for col in ["date_received", "product", "state", "channel", "company"]:
    con.execute(f"CREATE INDEX idx_{col} ON complaints({col})")


print(con.execute("SELECT COUNT(*) FROM complaints").fetchone())
con.close()