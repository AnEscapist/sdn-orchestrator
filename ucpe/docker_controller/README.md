# Docker Controller

## Functions:


* ## **docker_client()**

    Create a docker client for ommunicating with a docker server.
    
    **Example:**
    ```python
    >>> from DockerController import dockerController as dc
    >>> dockerClient = dc.docker_Client(ip='10.10.81.100', port='2375')
    ```
    **Parameters**
    *   ip(*str*): IP address of the docker server.
    *   port(*str*): Port number of the docker server.
    
* ## **open_sftp()**
 
    Open an sftp session on the docker server.
    
    **Example**
    ```python
    >>>sftp = dc.open_sftp(ip='10.10.81.100', username='potato', password='potato')
    ```
    **Parameters**
    *   ip(*str*): IP address of the docker server.
    *   username(*str*): User name of the docker server.
    *   password(*str*): Password if the docker server.
    
    **Returns**
    *   a new **paramiko.sftp_client.SFTPClient** session object.
    
    **Raises**
    * **Connection Error** - If no route to the server.
    * **SSH Exception** - If no existing session.
    
* ## **all_Containers()**

    List containers.
    
    **Parameters**
    *   dcli: Docker client created by **docker_client()**.
    *   all(*bool*): List all containers. It's True by default. If it is False, only running containers will be listed.
    
    **Returns**
    *   list of **Containers**
    
    **Raises**
    *   **Connection Error** - If no route to the host.

* ## **all_Images()**

    List all images.
    
    **Parameters**
    *   dcli: Docker client created by **docker_client()**.
    *   name(*str*): Only show images belonging to the repository name.
    
    **Returns**
    *   list of **Images**
    
    **Raises**
    *   **Connection Error** -If no route to the host.
    
