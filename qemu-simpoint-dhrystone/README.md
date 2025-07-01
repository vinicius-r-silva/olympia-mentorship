# QEMU + SimPoint + Dhrystone

This activity demonstrates a containerized workflow to perform architecture-level simulation and program analysis using:

- **QEMU** for running Dhrystone compiled for RISC-V.
- **SimPoint** for analyzing program execution behavior through Basic Block Vectors (BBVs).

## Dependencies

- Docker (check this script [`install_docker_ubuntu.sh`](./others/install_docker_ubuntu.sh) or the [`official guide`](https://docs.docker.com/engine/install) for installing it

## Project Structure

```bash
qemu-simpoint-dhrystone/
├── Dockerfile               # Defines environment with QEMU, SimPoint, Dhrystone
├── run_in_docker.sh         # Runs the experiment inside the container
├── build_docker.sh          # Builds the Docker image
├── build_and_run.sh         # Shortcut: builds the image and runs the workflow
```

## Usage

 - Run the build_and_run script to both create the docker image and execute dhrystone bbv generation and simpointing
```bash
./build_and_run.sh
```

## Results

All results gerenated are saved in the simpoint_output folder once the build_and_run.sh or the run_in_docker.sh scripts are executed