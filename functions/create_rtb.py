def create_rtb():
    composer = {
        "memcached": {"image": "memcached:latest", "ports":['11211:11211']},
        "webapp":{"build":"./RootTheBox/", "ports":["8888:8888"], "volumes": ["./RootTheBox/files:/opt/rtb/files:rw"],"environment":["COMPOSE_CONVERT_WINDOWS_PATHS=1"]}}
    return composer