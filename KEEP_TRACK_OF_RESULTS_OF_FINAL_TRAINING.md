KEEP TRACK OF RESULTS OF FINAL TRAINING RUNS
- Local or GPU
- DeepSeg or Modified
  - Simple or Advanced Antenna Selection
- What Users
- Which Test
- Fixed or Random Seed
- Window Size
  - Stride/Pool sizes


# 04 Segmentation
| Model    | Antenna Selection | Users     | Test_Sequence | Seed   | WindowSize | Stride1 | Stride2 | PoolSize | FileName |
| -------- | ----------------- | --------- | ------------- | ------ | ---------- | ------- | ------- | -------- | -------- |
| DeepSeg  | -                 | All       | 6             | fixed  | 200        |         |         |          |          |
| DeepSeg  | -                 | All       | 5             | fixed  | 200        |         |         |          |          |
| DeepSeg  | -                 | All       | 3             | fixed  | 200        |         |         |          |          |
| DeepSeg  | -                 | All       | 6             | random | 200        |         |         |          |          |
| DeepSeg  | -                 | All       | 3             | random | 200        |         |         |          |          |
| DeepSeg  | -                 | user1     | 6             | random | 200        |         |         |          |          |
| DeepSeg  | -                 | user1     | 3             | random | 200        |         |         |          |          |
|          |                   |           |               |        |            |         |         |          |          |
| Modified | Simple            | ownUser1  | 6             | fixed  | ??????     | ??????  | ??????  | ??????   | ??????   |
| Modified | Simple            | ownUser1  | 3             | fixed  | ??????     | ??????  | ??????  | ??????   | ??????   |
| Modified | Advanced          | ownUser1* | 6             | fixed  | ??????     | ??????  | ??????  | ??????   | ??????   |
| Modified | Advanced          | ownUser1* | 3             | fixed  | ??????     | ??????  | ??????  | ??????   | ??????   |

# 06 Classification
| Model    | Antenna Selection | Users     | Test_Sequence | Seed   | WindowSize | Stride1 | Stride2 | PoolSize | FileName |
| -------- | ----------------- | --------- | ------------- | ------ | ---------- | ------- | ------- | -------- | -------- |
| DeepSeg  | -                 | All       | 6             | fixed  | 200        |         |         |          |          |
| DeepSeg  | -                 | All       | 5             | fixed  | 200        |         |         |          |          |
| DeepSeg  | -                 | All       | 3             | fixed  | 200        |         |         |          |          |
| DeepSeg  | -                 | All       | 6             | random | 200        |         |         |          |          |
| DeepSeg  | -                 | All       | 3             | random | 200        |         |         |          |          |
| DeepSeg  | -                 | user1     | 6             | random | 200        |         |         |          |          |
| DeepSeg  | -                 | user1     | 3             | random | 200        |         |         |          |          |
|          |                   |           |               |        |            |         |         |          |          |
| Modified | Simple            | ownUser1  | 6             | fixed  | ??????     | ??????  | ??????  | ??????   | ??????   |
| Modified | Simple            | ownUser1  | 3             | fixed  | ??????     | ??????  | ??????  | ??????   | ??????   |
| Modified | Advanced          | ownUser1* | 6             | fixed  | ??????     | ??????  | ??????  | ??????   | ??????   |
| Modified | Advanced          | ownUser1* | 3             | fixed  | ??????     | ??????  | ??????  | ??????   | ??????   |

