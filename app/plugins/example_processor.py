import datetime

def process_writes(influxdb3_local, table_batches, args=None):
    # Log the provided arguments
    if args:
        for key, value in args.items():
            influxdb3_local.info(f"{key}: {value}")

    # Process each table batch
    for table_batch in table_batches:
        table_name = table_batch["table_name"]
        influxdb3_local.info(f"Processing table: {table_name}")

        # Skip processing a specific table if needed
        if table_name == "exclude_table":
            continue

        # Analyze each row
        for row in table_batch["rows"]:
            influxdb3_local.info(f"Row: {row}")

            # Standardize sensor names (lowercase, no spaces)
            sensor_name = row.get("sensor", "unknown").lower().replace(" ", "_")
            influxdb3_local.info(f"Standardized sensor name: {sensor_name}")

            # Standardize location and other tags by replacing spaces with underscores
            location = row.get("location", "unknown").lower().replace(" ", "_")

            # Add enriched field (e.g., timestamp)
            line = LineBuilder(table_name)
            line.tag("sensor", sensor_name)
            line.tag("location", location)
            line.float64_field("temperature_c", row.get("temperature", 0))
            line.string_field("processed_at", datetime.datetime.utcnow().isoformat())

            # Write the enriched data to a different database
            influxdb3_local.write_to_db("unified_sensor_data", line)

    influxdb3_local.info("Processing completed")
