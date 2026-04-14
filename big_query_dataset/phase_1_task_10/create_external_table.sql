CREATE OR REPLACE EXTERNAL TABLE `tbd-2026l-5.shakespeare.phase_1_task_10`
OPTIONS (
  format = "ORC",
  uris = ["gs://tbd-2026l-5-data/data/shakespeare/*.orc"]
);