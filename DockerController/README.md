# Docker Controller

## Functions:


* ## **docker_client()**

    Create a docker client for ommunicating with a docker server.
    
    **Example:**
    ```python
    >>> from DockerController import dockerController
    >>> dockerClient = dockerController.docker_Client(ip='10.10.81.100', port='2375')
    ```
    **Parameters**
    *   ip: IP address of the docker server.
    *   port: Port number of the docker server.
    
* ## **all_Containers()**

    List containers.
    
    **Parameters**
    *   dcli: Docker client just created.
    *   all(*bool*): List all containers. It's True by default. If it is False, only running containers will be listed.
    
    **Returns**
    *   list of **Containers**
    
    **Raises**
    *   **CONNECTION ERROR** - If no route to the host.
    
