KEEP TRACK OF RESULTS OF FINAL TRAINING RUNS
- Local or GPU
- DeepSeg or Modified
  - Simple or Advanced Antenna Selection
- What Users
- Which Test
- Fixed or Random Seed
- Window Size
  - Stride/Pool sizes


<!--     DeepSeg | -                 | All      | 3             | 31288432   | 120        | 4,2     | 4,2     | 6,6      | -->
# 04 Segmentation
| Model    | Antenna Selection | Users    | Test Sequence | Seed       | Window Size | Stride1 | Stride2 | Pool Size | Accuracy |
| -------- | ----------------- | -------- | ------------- | ---------- | ----------- | ------- | ------- | --------- | -------- |
| DeepSeg  | -                 | All      | 6             | given (10) | 120         | 4,2     | 4,2     | 6,6       | 97.7%    |
| DeepSeg  | -                 | All      | 5             | given (10) | 120         | 4,2     | 4,2     | 6,6       | 33.0%    |
| DeepSeg  | -                 | All      | 3             | given (10) | 120         | 4,2     | 4,2     | 6,6       | 34.9%    |
| DeepSeg  | -                 | All      | 6             | 31288432   | 120         | 4,2     | 4,2     | 6,6       | 97.7%    |
| DeepSeg  | -                 | user1    | 6             | 31288432   | 120         | 4,2     | 4,2     | 6,6       | 56.4%    |
| DeepSeg  | -                 | user1    | 3             | 31288432   | 120         | 4,2     | 4,2     | 6,6       | 69.9%    |
|          |                   |          |               |            |             |         |         |           |          |
| Modified | Simple            | ownUser1 | 6             | fixed (10) | 60          | 2,2     | 4,2     | 6,6       | 90.1%    |
| Modified | Simple            | ownUser1 | 3             | fixed (10) | 60          | 2,2     | 4,2     | 6,6       | 46.4%    |
| Modified | Simple            | ownUser1 | 5             | fixed (10) | 60          | 2,2     | 4,2     | 6,6       | 88.8%    |
|          |                   |          |               |            |             |         |         |           |          |
| Modified | Advanced          | EXT      | 6             | fixed (10) | 60          | 2,2     | 4,2     | 6,6       | 88.7%    |
| Modified | Advanced          | EXT      | 3             | fixed (10) | 60          | 2,2     | 4,2     | 6,6       | 61.6%    |
| Modified | Advanced          | EXT      | 5             | fixed (10) | 60          | 2,2     | 4,2     | 6,6       | 85.8%    |

# 06 Classification
| Model    | Antenna Selection | Users    | Test Sequence | Seed       | Window Size | Stride1 | Stride2 | Pool Size | Accuracy |
| -------- | ----------------- | -------- | ------------- | ---------- | ----------- | ------- | ------- | --------- | -------- |
| DeepSeg  | -                 | All      | 6             | given (10) | 200         | 5,2     | 5,2     | 6,6       | 76.7%    |
| DeepSeg  | -                 | All      | 5             | given (10) | 200         | 5,2     | 5,2     | 6,6       | 75.6%    |
| DeepSeg  | -                 | All      | 3             | given (10) | 200         | 5,2     | 5,2     | 6,6       | 62.0%    |
| DeepSeg  | -                 | All      | 6             | 31288432   | 200         | 5,2     | 5,2     | 6,6       | 72.2%    |
| DeepSeg  | -                 | All      | 3             | 31288432   | 200         | 5,2     | 5,2     | 6,6       | 59.5%    |
| DeepSeg  | -                 | user1    | 6             | 31288432   | 200         | 5,2     | 5,2     | 6,6       | 48.6%    |
| DeepSeg  | -                 | user1    | 3             | 31288432   | 200         | 5,2     | 5,2     | 6,6       | 48.0%    |
|          |                   |          |               |            |             |         |         |           |          |
| Modified | Simple            | ownUser1 | 5             | 31288432   | 100         | 3,2     | 4,2     | 7,6       | 60.1%    |
| Modified | Simple            | ownUser1 | 3             | 31288432   | 100         | 3,2     | 4,2     | 7,6       | 22.92%   |
|          |                   |          |               |            |             |         |         |           |          |
| Modified | Advanced          | EXT      | 5             | fixed (10) | 100         | 3,2     | 4,2     | 7,6       | 60.4%    |
| Modified | Advanced          | EXT      | 3             | fixed (10) | 100         | 3,2     | 4,2     | 7,6       | 72.0%    |
|          |                   |          |               |            |             |         |         |           |          |
| Modified | Advanced          | EXT      | 3             | fixed (10) | 100         | 2,2     | 5,2     | 8,6       | 87.7%    |

