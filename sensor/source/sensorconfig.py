from kombu import Queue

broker_url = 'amqp://guest:guest@rabbitmq:5672/'
result_backend = "rpc://"

task_queues = [
    Queue('sensor', queue_arguments={'x-queue-mode': 'lazy'}),
]
task_routes = ([
    ('tasks.*', {'queue': 'sensor'}),
],)

beat_schedule = {
    'generate-vibration-every-30-seconds': {
        'task': 'tasks.generate_vibration',
        'schedule': 30.0,
    },
}
timezone = 'UTC'