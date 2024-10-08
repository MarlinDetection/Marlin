# Marlin Data Docker Image

This minimal Docker image contains the data that we collected while evaluating our tool. Accordingly, there is no hardware or software-defined radio libraries required for it.

```bash
# Build the container
docker build -t marlin-data .
# Start and attach to a container
docker run -it marlin-data
```

From within the container, you can access our main script directly.

```bash
# From the working directory of the container
./python3 <script>.py
```
