import influxdb_client_3 as InfluxDBClient3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import os

def main():
    # Get token from environment variable with a default for testing
    token = os.getenv("INFLUX_TOKEN", "default-token")

    client = InfluxDBClient3.InfluxDBClient3(
        host="http://127.0.0.1:8181",
        token=token,
        org="",  # empty string since it was empty in working config
        database="test",
        auth_scheme="Bearer"  # add this parameter
        )

    # Generate sample data
    end_time = end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)
    dates = pd.date_range(start=start_time, end=end_time, freq='5min')

    # Create sample DataFrame
    df = pd.DataFrame(
        np.random.randn(len(dates), 3),
        index=dates,
        columns=['Temperature', 'Humidity', 'Pressure']
    )
    df['location'] = 'sensor-1'

    try:
        # Write data to InfluxDB
        print("Writing data to InfluxDB...")
        client.write(
            df, 
            data_frame_measurement_name='environmental_data',
            data_frame_tag_columns=['location']
        )
        print("Write successful!")

        # Query back the data
        print("\nQuerying written data...")
        query_df = client.query(
            query='SELECT * FROM "environmental_data"',
            language="sql",
            mode="pandas"
        )
        print("\nQuery Results:")
        print(query_df.head())

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    main()