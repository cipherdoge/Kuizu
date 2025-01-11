from . import redis_client

def background_task(data):
    redis_client.set('last_task', data)
    return {'status': 'completed', 'data': data}
