# Chandigarh calibration evidence

These files contain published historical observations and derived traffic indicators that can be used as calibration/validation targets. They are NOT represented as 2026 live measurements.

- `traffic_rides_2011.csv`: RITES primary survey values reproduced from Chandigarh Metro DPR traffic-demand chapter.
- `v2_traffic_peak_2018.csv`: published MetroCount/Radar-Gun study peak-hour observations and V/C/LOS values.
- `speed_reference_2018.csv`: published average 85th-percentile speeds for six Chandigarh V-2 roads.
- `../air_quality/cpcb_no2_2017.csv`: CPCB published annual NO2 monitoring values at five Chandigarh stations.

Use these for historical calibration/validation and clearly label the study year in the UI. They should not be used as current live traffic conditions without an explicit temporal adjustment model.
