# QEMU + SimPoint + Dhrystone

This activity demonstrates a containerized workflow to perform architecture-level simulation and program analysis using:

- **QEMU** for running Dhrystone compiled for RISC-V.
- **SimPoint** for analyzing program execution behavior through Basic Block Vectors (BBVs).

The two main tasks for this activity are:
- Create a Dockfile responsible to generate a docker image that contains:
  - QEMU with RISC-V and BBV generation capabilities
  - Dhrystone
  - SimPoint
- Create support scripts to generate the Docker image and execute the SimPoint analysis

## Dependencies

- Docker (check this script [`install_docker_ubuntu.sh`](/others/install_docker_ubuntu.sh) or the [`official guide`](https://docs.docker.com/engine/install) for installation)

## Project Structure

```bash
qemu-simpoint-dhrystone/
├── Dockerfile               # Creates a docker image with QEMU, SimPoint, Dhrystone
├── run_in_docker.sh         # Runs the experiment inside the container
├── build_docker.sh          # Builds the Docker image
├── build_and_run.sh         # Executes both build_docker and run_in_docker scripts
```

## Usage

 - Run the build_and_run.sh script to create the Docker image and execute Dhrystone, BBV generation, and simpointing
```bash
./build_and_run.sh
```
All generated results are saved in the simpoint_output folder once the build_and_run.sh or the run_in_docker.sh scripts are executed.

## Tasks

### Dockerfile creation
The Dockerfile creation is divided into four parts:
1. **Dependencies installation.** Install all dependencies to compile QEMU, as listed in [`this wiki`](https://wiki.qemu.org/Hosts/Linux), to garantee maximum code coverage during the build. Some listed dependencies can be removed since they do not contribute for the QEMU RISC-V binaries compilation.

1. **QEMU compilation.** 
    1. Compile QEMU, 
    1. Add the generated riscv64 and riscv32 QEMU binaries to /usr/local/bin 
    1. Create the QEMU_PLUGINS enviroment variable to simplify access to TCG plugins, such as the libbbv plugin used for bbvs generation later

1. **Simpoint compilation.** 
    1. Compile SimPoint, 
    1. Add the SimPoint’s binary folder to the PATH enviroment variable so that the `simpoint` command is globally accessible

1. **Dhrystone compilation.** 
    1. Compile Dhrystone using the `riscv64-linux-gnu-gcc` compiler
    1. Create the DHRYSTONE environment variable pointing to the generated Dhrystone binary

### Support scripts
Three support scripts were creted:
1. **build_docker.sh**. Builds the docker image with IMAGE_NAME variable representing its name
1. **run_in_docker.sh**. Runs the BBV generation and SimPoint analysis for Dhrystone. The script is configured using this four variables:

    * **IMAGE_NAME**. Must be the same image named used in the build_docker script
    * **OUTPUT_DIR**. The BBVs and SimPoint analisys output folder
    * **INTERVAL**. BBV interval (instructions per basic block sample)
    * **MAX_K**. Max number of clusters for SimPoint
1. **build_and_run.sh**. Executes both build_docker and run_in_docker scripts
